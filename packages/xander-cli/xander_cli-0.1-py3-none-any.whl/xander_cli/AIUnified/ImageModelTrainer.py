import tensorflow as tf
from tensorflow import keras
from keras import layers, models, callbacks, regularizers
from tensorflow.keras.utils import image_dataset_from_directory
import os
import zipfile
import queue
import keras_tuner as kt

class ImageModelTrainer:
    def __init__(self, dataset_url, model_name, hyperparameters=None):
        physical_devices = tf.config.list_physical_devices('GPU')
        if physical_devices:
            print("GPU(s) detected:", len(physical_devices))
            for device in physical_devices:
                try:
                    tf.config.experimental.set_memory_growth(device, True)
                    tf.config.set_logical_device_configuration(
                        device,
                        [tf.config.LogicalDeviceConfiguration(memory_limit=1024 * 9)]
                    )
                    print(f"Memory configuration set for GPU device: {device}")
                except RuntimeError as e:
                    print(f"Error configuring GPU device {device}: {e}")
        else:
            print("No GPU devices detected. Running on CPU.")
            
        self.dataset_url = dataset_url
        self.model_name = model_name
        self.task = 'image'
        self.hyperparameters = hyperparameters or {}
        self.epoch_info_queue = queue.Queue()
        self.data_dir = "extracted_files"
        self.img_height = 150
        self.img_width = 150
        self.epoch_data = []
        self.model_path = f"{model_name}.keras"
        self.directory_path = "models"
        self.complete_path = os.path.join(self.directory_path, self.model_path)
        self.train_ds = None
        self.val_ds = None
        self.num_classes = 0
        self.download_and_extract_data()
        self.prepare_datasets()

    def download_and_extract_data(self):
        with zipfile.ZipFile(self.dataset_url, "r") as zip_ref:
            zip_ref.extractall(self.data_dir)
        self.data_dir = os.path.join(self.data_dir, os.listdir(self.data_dir)[0])
        print(f"Files extracted to: {self.data_dir}")

    def prepare_datasets(self):
        train_ds = image_dataset_from_directory(
            self.data_dir,
            validation_split=0.2,
            subset="training",
            seed=123,
            image_size=(self.img_height, self.img_width),
            batch_size=self.hyperparameters.get("batch_size", 32),
        )
        val_ds = image_dataset_from_directory(
            self.data_dir,
            validation_split=0.2,
            subset="validation",
            seed=123,
            image_size=(self.img_height, self.img_width),
            batch_size=self.hyperparameters.get("batch_size", 32),
        )

        AUTOTUNE = tf.data.AUTOTUNE
        self.class_names = train_ds.class_names
        self.num_classes = len(self.class_names)
        print(f"Class names: {self.class_names}")

        self.train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
        self.val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    def model_builder(self, hp):
        model = keras.Sequential()
        conv_activation = hp.Choice('conv_activation', values=['relu', 'tanh', 'leaky_relu'])
        dense_activation = hp.Choice('dense_activation', values=['relu', 'tanh', 'leaky_relu'])
        regularizer_choice = hp.Choice('regularizer', values=['l1', 'l2', 'l1_l2'])

        def get_regularizer():
            if regularizer_choice == 'l1':
                return regularizers.l1(hp.Float('l1', 1e-6, 1e-2, sampling='log'))
            elif regularizer_choice == 'l2':
                return regularizers.l2(hp.Float('l2', 1e-6, 1e-2, sampling='log'))
            return regularizers.l1_l2(
                l1=hp.Float('l1', 1e-6, 1e-2, sampling='log'),
                l2=hp.Float('l2', 1e-6, 1e-2, sampling='log'),
            )

        model.add(layers.Rescaling(1.0 / 255, input_shape=(self.img_height, self.img_width, 3)))

        for i in range(hp.Int('num_conv_layers', 1, 4)):
            model.add(layers.Conv2D(
                filters=hp.Int(f'conv_{i}_filters', 32, 128, step=32),
                kernel_size=(3, 3),
                activation=conv_activation,
                kernel_regularizer=get_regularizer()
            ))
            model.add(layers.MaxPooling2D(pool_size=(2, 2)))

        model.add(layers.Flatten())

        for i in range(hp.Int('num_dense_layers', 1, 3)):
            model.add(layers.Dense(
                units=hp.Int(f'dense_{i}_units', 64, 256, step=64),
                activation=dense_activation,
                kernel_regularizer=get_regularizer()
            ))
            model.add(layers.Dropout(hp.Float(f'dropout_{i}', 0.1, 0.5, step=0.15)))

        model.add(layers.Dense(self.num_classes))

        model.compile(
            optimizer=keras.optimizers.Adam(hp.Float('learning_rate', 1e-4, 1e-2, sampling='log')),
            loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy']
        )

        return model

    def tune_hyperparameters(self):
        tuner = kt.Hyperband(
            self.model_builder,
            objective='val_accuracy',
            max_epochs=20,
            factor=3,
            directory='tuned_models',
            project_name=self.model_name
        )

        early_stopping = callbacks.EarlyStopping(monitor="val_accuracy", patience=5, restore_best_weights=True)

        tuner.search(
            self.train_ds,
            validation_data=self.val_ds,
            epochs=20,
            callbacks=[early_stopping]
        )

        best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]
        print(f"Best hyperparameters: {best_hps.values}")

        return best_hps

    def build_and_train_final_model(self, best_hps):
        self.model = self.model_builder(best_hps)
        early_stopping = callbacks.EarlyStopping(monitor="val_accuracy", patience=5, restore_best_weights=True)

        history = self.model.fit(
            self.train_ds,
            validation_data=self.val_ds,
            epochs=self.hyperparameters["epochs"],
            callbacks=[early_stopping],
            verbose=1
        )

        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path)
        self.model.save(self.complete_path)
        print(f"Model saved to {self.complete_path}")

        return history

    def execute(self):
        best_hps = self.tune_hyperparameters()
        history = self.build_and_train_final_model(best_hps)
        
        interference_code = f'''
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import requests
from io import BytesIO

# Load model from local storage
def load_model_from_local(model_path):
    return load_model(model_path)

# Prepare image for prediction
def prepare_image(img, img_height=120, img_width=120):
    img = img.resize((img_width, img_height))
    img_array = image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    return img_array

# Make predictions
def make_predictions(model, img_array):
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    return tf.argmax(score), tf.reduce_max(score)

def load_image(image_path=None, image_url=None):
    if image_path:
        return Image.open(image_path)
    elif image_url:
        response = requests.get(image_url)
        return Image.open(BytesIO(response.content))
    else:
        raise ValueError("Please provide either an image path or an image URL")

def infer(input_data, model_name, class_names):
    try:
        # Setup model path and load model
        model_path = model_name
        model = load_model_from_local(model_path)
        
        if model:
            # Handle image input
            if isinstance(input_data, dict):
                image_path = input_data.get('image_path')
                image_url = input_data.get('image_url')
                
                if not image_path and not image_url:
                    raise ValueError("Please provide either an image path or an image URL")
                
                # Load and prepare image
                img = load_image(image_path, image_url)
                img_array = prepare_image(img)
                
                # Get predictions
                class_idx, class_prob = make_predictions(model, img_array)
                
                # Prepare output
                return {{
                    "prediction": [
                        {{"predicted_class": class_names[int(class_idx)]}},
                        {{"probability": float(class_prob)}}
                    ]
                }}
            else:
                raise ValueError("Input data should be a dictionary with 'image_path' or 'image_url'")
        else:
            raise ValueError("Failed to load model.")
            
    except Exception as e:
        raise Exception(f"Error during inference: {{str(e)}}")

if __name__ == "__main__":
    input_data = {{
        'image_path': '',  
        'image_url': ''  
    }}
    model_name = '{self.complete_path}'
    class_names = {self.class_names}
    
    result = infer(input_data, model_name, class_names)
    print(result)
        '''
        with open(f'inference_{self.model_name}.py', 'w') as file:
            file.write(interference_code)
        return history

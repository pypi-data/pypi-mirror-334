import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, Callback
from tensorflow.keras.utils import to_categorical
import nltk
import os
import pickle
import queue
import itertools
import chardet

class TextModel:
    def __init__(self, dataset_url, model_name, default_hyperparameters=None, target_col="", encoding=""):
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
        self.epochs = default_hyperparameters["epochs"]
        self.default_hyperparameters = default_hyperparameters or {
            "batch_size": 32,
            "epochs": 10,
            "embedding_dim": 100,
            "lstm_units": 128,
            "dropout_rate": 0.5,
            "learning_rate": 0.001,
        }
        self.best_hyperparameters = self.default_hyperparameters
        self.epoch_info_queue = queue.Queue()
        self.directory_path = "models"
        self.current_val_acc = 0
        self.epoch_data = []
        self.model_path = os.path.join(self.directory_path, f'{self.model_name}.h5')
        self.tokenizer_path = os.path.join(self.directory_path, f'tokenizer_{self.model_name}.pkl')
        self.label_encoder_path = os.path.join(self.directory_path, f'label_encoder_{self.model_name}.pkl')
        self.target_col = target_col
        self.encoding = encoding
        self.load_data()
        self.preprocess_data()

    def load_data(self):
        with open(self.dataset_url, 'rb') as file:
            result = chardet.detect(file.read())
            encoding = result['encoding']
        
        self.df = pd.read_csv(self.dataset_url, encoding=encoding)        
        self.df = self.df.dropna()

    def preprocess_data(self):
        target_idx = self.df.columns.get_loc(self.target_col)
        
        text_cols = self.df.drop(columns=[self.target_col])
        self.text_columns = text_cols.apply(lambda x: ' '.join(x.astype(str)), axis=1)
        
        self.category_column = self.target_col
        
        self.label_encoder = LabelEncoder()
        self.df[self.category_column] = self.label_encoder.fit_transform(self.df[self.category_column])
        self.num_classes = len(np.unique(self.df[self.category_column]))
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.text_columns, self.df[self.category_column], test_size=0.2, random_state=42
        )
        
        self.max_num_words = 20000
        self.max_sequence_length = 100
        self.tokenizer = Tokenizer(num_words=self.max_num_words)
        self.tokenizer.fit_on_texts(self.X_train)
        self.X_train_seq = self.tokenizer.texts_to_sequences(self.X_train)
        self.X_test_seq = self.tokenizer.texts_to_sequences(self.X_test)
        self.X_train_pad = pad_sequences(self.X_train_seq, maxlen=self.max_sequence_length)
        self.X_test_pad = pad_sequences(self.X_test_seq, maxlen=self.max_sequence_length)
        
        self.y_train_cat = to_categorical(self.y_train, self.num_classes)
        self.y_test_cat = to_categorical(self.y_test, self.num_classes)
        
    def create_model(self, hyperparameters):
        model = Sequential()
        model.add(Embedding(
            input_dim=self.max_num_words,
            output_dim=hyperparameters["embedding_dim"],
            input_length=self.max_sequence_length
        ))
        model.add(Bidirectional(LSTM(
            units=hyperparameters["lstm_units"],
            dropout=hyperparameters["dropout_rate"],
            recurrent_dropout=hyperparameters["dropout_rate"],
            return_sequences=False
        )))
        model.add(Dropout(hyperparameters["dropout_rate"]))
        model.add(Dense(
            units=self.num_classes,
            activation='softmax',
            kernel_regularizer=l2(0.01)
        ))

        optimizer = tf.keras.optimizers.Adam(learning_rate=hyperparameters["learning_rate"])
        model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def train_model(self, hyperparameters, testing=False):
        model = self.create_model(hyperparameters)
        batch_size = hyperparameters["batch_size"]
        epochs = hyperparameters["epochs"]
        
        if testing == False:
            self.current_val_acc = 0
            
        print(self.current_val_acc)
        class CustomCallback(Callback):
            def __init__(self, outer_instance):
                super().__init__()
                self.outer_instance = outer_instance

            def on_epoch_end(self, epoch, logs=None):
                test_acc = logs.get('val_accuracy')
                epoch_info = {
                    "epoch": epoch + 1,
                    "train_loss": logs.get('loss'),
                    "train_acc": logs.get('accuracy'),
                    "test_loss": logs.get('val_loss'),
                    "test_acc": logs.get('val_accuracy'),
                }
                print(epoch_info)
                self.outer_instance.epoch_data.append(epoch_info)
                self.outer_instance.epoch_info_queue.put(epoch_info)

                if test_acc > self.outer_instance.current_val_acc and testing == False:
                    self.outer_instance.save_model(model)
                    self.outer_instance.current_val_acc = test_acc
                    print(f"New best model saved with validation accuracy: {test_acc:.4f}")
                elif test_acc > self.outer_instance.current_val_acc and testing == True:
                    self.outer_instance.current_val_acc = test_acc

        custom_callback = CustomCallback(self)

        final_epochs = 0
        
        if testing:
            final_epochs = epochs
        else:
            final_epochs = self.epochs
            
        history = model.fit(
            self.X_train_pad, self.y_train_cat,
            batch_size=batch_size,
            epochs=final_epochs,
            validation_split=0.2,
            callbacks=[custom_callback],
            verbose=0
        )
        return history.history["val_accuracy"][-1]

    def tune_hyperparameters(self, param_grid):
        print(param_grid)
        param_names = list(param_grid.keys())
        param_combinations = list(itertools.product(*param_grid.values()))

        best_val_acc = 0
        best_params = None

        for i in range(0, len(param_combinations)):
            hyperparameters = dict(zip(param_names, param_combinations[i]))
            print(f"Testing hyperparameters {i}/{len(param_combinations)}: {hyperparameters}")
            val_acc = self.train_model(hyperparameters, testing=True)
            if val_acc >= best_val_acc:
                best_val_acc = val_acc
                best_params = hyperparameters
                self.best_hyperparameters = hyperparameters
                print(f"New best hyperparameters found: {best_params} with accuracy {best_val_acc:.4f}")

        print(f"Best hyperparameters: {best_params}")
        return best_params

    def save_model(self, model):
        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path)

        model_path = os.path.join(self.directory_path, f'{self.model_name}.h5')
        tokenizer_path = os.path.join(self.directory_path, f'tokenizer_{self.model_name}.pkl')
        label_encoder_path = os.path.join(self.directory_path, f'label_encoder_{self.model_name}.pkl')

        model.save(model_path)

        with open(tokenizer_path, 'wb') as f:
            pickle.dump(self.tokenizer, f)

        with open(label_encoder_path, 'wb') as f:
            pickle.dump(self.label_encoder, f)

    def execute(self):
        nltk.download('punkt')
        param_grid = {
            "batch_size": [32],
            "epochs": [3],
            "embedding_dim": [50, 100, 150],
            "lstm_units": [64, 128, 192],
            "dropout_rate": [0.1, 0.3, 0.5],
            "learning_rate": [0.01, 0.001],
        }
        # param_grid = {
        #     "batch_size": [32],
        #     "epochs": [2],
        #     "embedding_dim": [50],
        #     "lstm_units": [64],
        #     "dropout_rate": [0.1],
        #     "learning_rate": [0.01, 0.001, 0.0001],
        # }
        params = self.tune_hyperparameters(param_grid)
        print('----training begins----')
        self.train_model(params, testing=False)
            
        interference_code = f'''
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib

# Load necessary components from local storage
def load_model_from_local(model_path):
    return load_model(model_path)

def load_tokenizer(tokenizer_path):
    return joblib.load(tokenizer_path)

def load_label_encoder(label_encoder_path):
    return joblib.load(label_encoder_path)

# Preprocess input text
def preprocess_text(text, tokenizer, max_sequence_length):
    sequences = tokenizer.texts_to_sequences([text])
    padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length)
    return padded_sequences

# Make predictions
def make_predictions(model, preprocessed_text):
    predictions = model.predict(preprocessed_text)
    return predictions

def infer(input_data, model_name, tokenizer_name, label_encoder_name):
    model_path = model_name
    tokenizer_path = tokenizer_name
    label_encoder_path = label_encoder_name
    
    # Load model and preprocessing components
    model = load_model_from_local(model_path)
    tokenizer = load_tokenizer(tokenizer_path)
    label_encoder = load_label_encoder(label_encoder_path)
    
    if model and tokenizer and label_encoder:
        # Set maximum sequence length for padding
        max_sequence_length = 100  # Adjust this based on your model's requirements
        
        # Preprocess the input text
        preprocessed_text = preprocess_text(input_data, tokenizer, max_sequence_length)
        
        # Get predictions
        predictions_proba = make_predictions(model, preprocessed_text)
        predicted_class = tf.argmax(predictions_proba, axis=1)
        predicted_label = label_encoder.inverse_transform(predicted_class)
        
        # Prepare output
        return {{
            "prediction": [
                {{"predicted_class": predicted_label[0]}},
                {{"probabilities": predictions_proba[0].tolist()}}
            ]
        }}
    else:
        raise ValueError("Failed to load model, tokenizer, or label encoder.")

if __name__ == "__main__":
    input_data = 'test'  # Your input text here
    model_name = '{self.model_path}'
    tokenizer_name = '{self.tokenizer_path}'
    label_encoder_name = '{self.label_encoder_path}'
    
    result = infer(input_data, model_name, tokenizer_name, label_encoder_name)
    print(result)
        '''
        with open(f'inference_{self.model_name}.py', 'w') as file:
            file.write(interference_code)
        yield 'Done'


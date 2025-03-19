import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, LSTM, Attention, Input
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import Callback
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import requests
import os
import uuid
import queue
import threading
import random
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelEncoder
from itertools import product

class RegressionDL:
    def __init__(self, dataset_url, architecture, hyperparameters, model_name, target_col, encoding):
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
        self.architecture = architecture
        self.hyperparameters = hyperparameters
        self.task_type = 'regression'
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = f'{model_name}.h5'
        self.scaler_path = f'scaler_{model_name}.pkl'
        self.label_encoder_path = f'label_encoder_{model_name}.pkl'
        self.directory_path = "models"
        self.complete_model_path = os.path.join(self.directory_path, self.model_path)
        self.complete_scaler_path = os.path.join(self.directory_path, self.scaler_path)
        self.complete_label_encoder_path = os.path.join(self.directory_path, self.label_encoder_path)
        self.epoch_info_queue = queue.Queue()
        self.model_name = model_name
        self.target_col = target_col
        self.encoding = encoding
        self.current_epoch_info = None
        self.epoch_data = []
        self.current_val_loss = float('inf')
        self.data, self.label_encoder = self.load_and_prepare_data()

    def apply_preprocessing(self, value, data):
        uni = list(set(data))
        return uni.index(value)

    def load_and_prepare_data(self):
        df = pd.read_csv(self.dataset_url, encoding=self.encoding)
        df = df.dropna()
        df = df.iloc[:25000]
        
        label_encoders = {}
        
        for column_name in df.columns:
            if df[column_name].dtype in ['object']:
                le = LabelEncoder()
                df[column_name] = le.fit_transform(df[column_name])
                label_encoders[column_name] = le
                print(f"Label encoding applied to column '{column_name}'.")
        
        return df, label_encoders

    def build_model(self, params=None):
        if tf.config.list_physical_devices('GPU'):
            tf.keras.mixed_precision.set_global_policy('float32')
            print("Mixed precision policy enabled for GPU training")
            
        input_shape = (self.data.shape[1] - 1,)
        if params and 'layers' in params:
            self.model = self.build_dense_model(
                input_shape=input_shape,
                layers=params['layers'],
                activation=params.get('activation', 'relu'),
                learning_rate=params.get('learning_rate', 0.0005)
            )
        else:
            self.model = self.build_dense_model(input_shape=input_shape)

    def build_dense_model(self, input_shape, layers=[256, 128, 64, 32], 
                         activation='relu', output_activation=None, learning_rate=0.0005):
        model = Sequential()
        model.add(Dense(layers[0], input_shape=input_shape, activation=activation, 
                       kernel_regularizer=tf.keras.regularizers.l2(0.01)))
        model.add(tf.keras.layers.Dropout(0.4))
        
        for layer in layers[1:]:
            model.add(Dense(layer, activation=activation, 
                          kernel_regularizer=tf.keras.regularizers.l2(0.01)))
            model.add(tf.keras.layers.Dropout(0.4))
        
        model.add(Dense(1, activation=output_activation))
        
        optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        model.compile(optimizer=optimizer, loss='mean_absolute_error', metrics=['mae'])
        
        return model

    def train_model(self, params=None, testing=False):
        # if params:
        #     self.hyperparameters.update(params)
        
        y = self.data[self.target_col]
        X = self.data.drop(columns=[self.target_col])
        # target_idx = self.data.columns.get_loc(self.target_col)
        # X = self.data.iloc[:, :target_idx]  
        # y = self.data.iloc[:, target_idx]
        
        X = self.scaler.fit_transform(X)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)

        class CustomCallback(Callback):
            def __init__(self, outer_instance):
                super().__init__()
                self.outer_instance = outer_instance

            def on_epoch_end(self, epoch, logs=None):
                test_loss = logs.get('val_loss')
                train_loss = logs.get('loss')
                epoch_info = {
                    "epoch": epoch + 1,
                    "train_loss": train_loss,
                    "test_loss": test_loss
                }
                
                self.outer_instance.epoch_data.append(epoch_info)
                self.outer_instance.current_epoch_info = epoch_info
                self.outer_instance.epoch_info_queue.put(epoch_info)

                if test_loss < self.outer_instance.current_val_loss and testing == False:
                    self.outer_instance.save_model()
                    self.outer_instance.current_val_loss = test_loss
                    print(f"New best model saved with validation loss: {test_loss:.4f}")
                elif test_loss < self.outer_instance.current_val_loss and testing == True:
                    self.outer_instance.current_val_loss = test_loss

        custom_callback = CustomCallback(self)
        
        final_epochs = 0
        
        if testing == False:
            final_epochs = self.hyperparameters["epochs"]
        else:
            final_epochs = params["epochs"]
        
        history = self.model.fit(
            X_train, 
            y_train,
            validation_data=(X_test, y_test),
            epochs=final_epochs,
            batch_size=32,
            callbacks=[custom_callback],
            verbose=0
        )
        
        self.X_test, self.y_test = X_test, y_test
        return history

    def hyperparameter_tuning(self, param_grid):
        best_loss = float('inf')
        best_params = None
        
        param_combinations = list(product(*param_grid.values()))
        total_combinations = len(param_combinations)
        
        print(f"Starting hyperparameter tuning with {total_combinations} combinations")
        
        for i, params in enumerate(param_combinations, 1):
            params_dict = dict(zip(param_grid.keys(), params))
            print(f"\nTraining combination {i}/{total_combinations}:")
            print(params_dict)
            
            # Reset model and build with current parameters
            self.model = None
            self.build_model(params_dict)
            
            # Train model and get results
            self.train_model(params_dict, testing=True)
            current_loss = self.current_val_loss
            
            if current_loss < best_loss:
                best_loss = current_loss
                best_params = params_dict
                print(f"New best MAE loss: {best_loss:.4f}")
        
        print(f"\nTuning completed!")
        print(f"Best MAE loss: {best_loss:.4f}")
        print(f"Best parameters: {best_params}")
        return best_params

    def evaluate_model(self):
        results = self.model.evaluate(self.X_test, self.y_test, verbose=0)
        return results

    def save_model(self):
        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path)
        
        self.model.save(self.complete_model_path)
        joblib.dump(self.scaler, self.complete_scaler_path)
        joblib.dump(self.label_encoder, self.complete_label_encoder_path)

    def execute_with_tuning(self):
        param_grid = {
            'batch_size': [32, 64],
            'epochs': [3],
            'layers': [
                [256, 128, 64, 32],
                [512, 256, 128, 64],
                [1024, 512, 256, 128, 64],
                [128, 64, 32]
            ],
            'activation': ['relu', 'leaky_relu'],
            'learning_rate': [0.01, 0.001, 0.0005]
        }
        # param_grid = {
        #     'epochs': [3],
        #     'layers': [
        #         [256, 128, 64, 32],
        #         [512, 256, 128, 64, 32],
        #     ],
        #     'activation': ['relu'],
        #     'learning_rate': [0.001]
        # }
        
        print("Starting hyperparameter tuning process...")
        best_params = self.hyperparameter_tuning(param_grid)
        
        print("\nTraining final model with best parameters...")
        self.model = None
        self.build_model(best_params)
        history = self.train_model(best_params)
        
        final_loss = self.evaluate_model()
        print(f"Final model MAE loss: {final_loss[0]:.4f}")
        
        return history

    def execute(self):
        self.build_model()
        training_thread = threading.Thread(target=self.execute_with_tuning)
        training_thread.start()

        epochs_completed = 0
        while epochs_completed < int(self.hyperparameters['epochs']):
            try:
                epoch_info = self.epoch_info_queue.get(timeout=1)
                yield epoch_info
                epochs_completed += 1
            except queue.Empty:
                if not training_thread.is_alive():
                    break

        training_thread.join()
        
        data = list(self.data.drop(columns=[self.target_col]).values)[0] 
        
        formatted_dat = [f"'{item}'" if isinstance(
            item, str) else str(item) for item in data]
        
#         interference_code = f'''import os
# import pandas as pd
# import numpy as np
# import joblib
# from tensorflow.keras.models import load_model

# # Load necessary components from local storage
# def load_model_from_local(model_path):
#     return load_model(model_path)

# def load_scaler_from_local(scaler_path):
#     return joblib.load(scaler_path)

# def load_label_encoders_from_local(label_encoder_path):
#     return joblib.load(label_encoder_path)

# # Preprocess input data
# def preprocess_input(data, scaler, label_encoders, column_names):
#     df = pd.DataFrame([data], columns=column_names)
#     for column, le in label_encoders.items():
#         if column in df.columns:
#             df[column] = le.transform(df[column])
#     df = pd.get_dummies(df, columns=df.select_dtypes(include=['object']).columns, drop_first=True)
#     df = df.reindex(columns=scaler.feature_names_in_, fill_value=0)
#     data_scaled = scaler.transform(df)
#     return data_scaled

# # Make predictions
# def make_predictions(model, data_scaled):
#     predictions = model.predict(data_scaled)
#     return predictions

# def infer(input_data, model_name, scaler_name, label_encoder_name, dataset_path):
#     model_path = model_name
#     scaler_path = scaler_name
#     label_encoder_path = label_encoder_name
    
#     model = load_model_from_local(model_path)
#     scaler = load_scaler_from_local(scaler_path)
#     label_encoders = load_label_encoders_from_local(label_encoder_path)
    
#     if model and scaler:
#         df = pd.read_csv(dataset_path, encoding='{self.encoding}')
#         column_names = df.columns.drop(['{self.target_col}']).tolist()
#         data_scaled = preprocess_input(input_data, scaler, label_encoders, column_names)
#         predictions = make_predictions(model, data_scaled)
        
#         # For regression, return the predicted values directly
#         return {{
#             "prediction": [
#                 {{"predicted_value": float(predictions[0][0])}}
#             ]
#         }}
#     else:
#         raise ValueError("Failed to load model or scaler.")

# if __name__ == "__main__":
#     input_data = [{', '.join(formatted_dat)}]
#     model_name = '{self.complete_model_path}'
#     scaler_name = '{self.complete_scaler_path}'
#     label_encoder_name = '{self.complete_label_encoder_path}'
#     dataset_url = '{self.dataset_url}'
    
#     result = infer(input_data, model_name, scaler_name, label_encoder_name, dataset_url)
#     print(result)
#         '''
        interference_code  = f'''
import numpy as np
import pandas as pd
import tensorflow as tf
import joblib
import os

def make_prediction(input_data, model_path, scaler_path, label_encoder_path, dataset_url):
    model = tf.keras.models.load_model(model_path)
    scaler = joblib.load(scaler_path)
    label_encoders = joblib.load(label_encoder_path)
    
    df_original = pd.read_csv(dataset_url, encoding='{self.encoding}')
    
    feature_columns = df_original.columns.drop(['{self.target_col}']).tolist()
    
    if len(input_data) != len(feature_columns):
        raise ValueError(f"Input data must have {{len(feature_columns)}} features. Got {{len(input_data)}} instead.")
    
    input_df = pd.DataFrame([input_data], columns=feature_columns)
    
    for column, encoder in label_encoders.items():
        if column in input_df.columns: 
            try:
                input_df[column] = encoder.transform(input_df[column])
            except ValueError:
                most_frequent_category = encoder.classes_[0]
                input_df[column] = input_df[column].map(lambda x: x if x in encoder.classes_ else most_frequent_category)
                input_df[column] = encoder.transform(input_df[column])
    
    scaled_data = scaler.transform(input_df)
    
    prediction = model.predict(scaled_data)
    
    return {{
            "prediction": [
                {{"predicted_value": float(prediction[0][0])}}
            ]
        }}

if __name__ == "__main__":
    input_data = [{', '.join(formatted_dat)}]
    model_name = '{self.complete_model_path}'
    scaler_name = '{self.complete_scaler_path}'
    label_encoder_name = '{self.complete_label_encoder_path}'
    dataset_url = '{self.dataset_url}'
    
    result = make_prediction(input_data, model_name, scaler_name, label_encoder_name, dataset_url)
    print(result)        
        '''
        
        with open(f'inference_{self.model_name}.py', 'w') as file:
            file.write(interference_code)
        
        yield 'Done'
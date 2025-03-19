import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.metrics import mean_absolute_error
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import joblib
import os
import uuid
import queue
import requests
import re

class Forecaster:
    def __init__(self, dataset_url, hasChanged, task, mainType, archType, architecture, hyperparameters, userId):
        self.dataset_url = dataset_url
        self.hasChanged = hasChanged
        self.task = task
        self.mainType = mainType
        self.archType = archType
        self.architecture = architecture
        self.hyperparameters = hyperparameters
        self.userId = userId
        self.api_url = 'https://apiv3.xanderco.in/core/store/'
        self.model_path = f'bestmodel{str(uuid.uuid4())}.pkl'
        self.scaler_path = f'scaler{str(uuid.uuid4())}.pkl'
        self.label_encoder_path = f'label_encoder{str(uuid.uuid4())}.pkl'
        self.directory_path = "models"
        self.complete_model_path = os.path.join(self.directory_path, self.model_path)
        self.complete_scaler_path = os.path.join(self.directory_path, self.scaler_path)
        self.complete_label_encoder_path = os.path.join(self.directory_path, self.label_encoder_path)
        self.date_regex = r'^\d{2,4}[-/]\d{1,2}[-/]\d{1,2}$'
        self.label_encoders = {}
        self.time_step = 60
        
        self.load_data()
        self.preprocess_data()
        
    def is_date_like(self, column):
        return any(re.match(self.date_regex, str(value)) for value in column)
    
    def convert_to_seconds(self, date_column):
        date_column = pd.to_datetime(date_column, format='%d/%m/%y', errors='coerce')
        seconds = (date_column - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
        return seconds

    def create_dataset(self, data, time_step=60):
        X, y = [], []
        for i in range(len(data) - time_step - 1):
            X.append(data[i:(i + time_step), 1:])
            y.append(data[i + time_step, len(self.df.columns) - 1])
        return np.array(X), np.array(y)

    def load_data(self):
        self.df = pd.read_csv(self.dataset_url)
        self.df = self.df.dropna()

        date_like_columns = [col for col in self.df.columns if self.is_date_like(self.df[col])]
        for column in date_like_columns:
            self.df[column] = self.convert_to_seconds(self.df[column])

        for column in self.df.select_dtypes('object').columns:
            le = LabelEncoder()
            self.df[column] = le.fit_transform(self.df[column])
            self.label_encoders[column] = le

    def preprocess_data(self):
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.scaled_data = self.scaler.fit_transform(self.df)
        
        self.X, self.y = self.create_dataset(self.scaled_data, self.time_step)
        self.X = self.X.reshape(self.X.shape[0], -1)
        
        train_size = int(len(self.X) * 0.8)
        self.X_train = self.X[:train_size]
        self.X_test = self.X[train_size:]
        self.y_train = self.y[:train_size]
        self.y_test = self.y[train_size:]

    def create_future_prediction(self, model, last_sequence, steps=60):
        future_predictions = []
        current_sequence = last_sequence.copy()
        
        for _ in range(steps):
            next_pred = model.predict(current_sequence.reshape(1, -1))[0]
            future_predictions.append(next_pred)
            current_sequence = np.roll(current_sequence, -1)
            current_sequence[-1] = next_pred
        
        return future_predictions

    def create_smooth_curve(self, x, y, num_points=300):
        x_smooth = np.linspace(x.min(), x.max(), num_points)
        spl = make_interp_spline(x, y, k=3)
        y_smooth = spl(x_smooth)
        return x_smooth, y_smooth

    def plot_training_results(self):
        time_steps = np.arange(len(self.y_test))
        x_actual_smooth, y_actual_smooth = self.create_smooth_curve(time_steps, self.y_test)
        x_pred_smooth, y_pred_smooth = self.create_smooth_curve(time_steps, self.predictions)

        plt.figure(figsize=(12, 6))
        plt.grid(True, linestyle='-', alpha=0.2)
        plt.plot(x_actual_smooth, y_actual_smooth, '-', color='#4472C4', label='Actual', linewidth=2)
        plt.plot(x_pred_smooth, y_pred_smooth, '-', color='#ED7D31', label='Predicted', linewidth=2)

        plt.title('Growth Curve Forecast', pad=20, fontsize=12)
        plt.xlabel('Time Steps', labelpad=10)
        plt.ylabel('Values', labelpad=10)
        plt.legend()

        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_alpha(0.5)
        ax.spines['bottom'].set_alpha(0.5)

        plt.tight_layout()
        plt.show()

    def plot_future_predictions(self):
        future_steps = np.arange(len(self.y_test), len(self.y_test) + 60)
        x_future_smooth, y_future_smooth = self.create_smooth_curve(future_steps, np.array(self.future_predictions))

        plt.figure(figsize=(12, 6))
        plt.plot(x_future_smooth, y_future_smooth, '-', color='#A5A5A5', label='Next 60 Steps', linewidth=2)

        plt.title('Future 60-Step Forecast', pad=20, fontsize=12)
        plt.xlabel('Time Steps', labelpad=10)
        plt.ylabel('Values', labelpad=10)
        plt.legend()

        plt.grid(True, linestyle='-', alpha=0.2)
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_alpha(0.5)
        ax.spines['bottom'].set_alpha(0.5)

        plt.tight_layout()
        plt.show()

    def create_model(self):
        self.model = XGBRegressor()

    def train_model(self):
        self.epoch_data = []
        self.current_val_acc = 0
        self.epoch_info_queue = queue.Queue()

        self.model.fit(self.X_train, self.y_train)
        self.predictions = self.model.predict(self.X_test)
        self.predictions_train = self.model.predict(self.X_train)
        
        last_sequence = self.X_test[-1]
        self.future_predictions = self.create_future_prediction(self.model, last_sequence)
        
        mae_test = mean_absolute_error(self.y_test, self.predictions)
        mae_train = mean_absolute_error(self.y_train, self.predictions_train)
        print(f"Mean Absolute Error: {mae_test}")
        print(f"Mean Absolute Error: {mae_train}")

        epoch_info = {
            "epoch": 1,
            "train_loss": mae_train,
            "test_loss": mae_test,
        }
        
        self.epoch_data.append(epoch_info)
        
        # self.plot_training_results()
        # self.plot_future_predictions()

    def save_model(self):
        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path)
        
        joblib.dump(self.model, self.complete_model_path)
        joblib.dump(self.scaler, self.complete_scaler_path)
        joblib.dump(self.label_encoders, self.complete_label_encoder_path)

    def upload_files_to_api(self):
        print(os.path.getsize(self.complete_model_path) / (1024 ** 3))
        try:
            file = {
                'file': open(self.complete_model_path, 'rb')
            }
            response_model = requests.post(self.api_url, files=file)
            response_data_model = response_model.json()
            model_url = response_data_model.get('file_url')

            if model_url:
                print(f"Model uploaded successfully. URL: {model_url}")
            else:
                print(
                    f"Failed to upload model. Error: {response_data_model.get('error')}")

            file = {
                'file': open(self.complete_scaler_path, 'rb')
            }

            response_scaler = requests.post(self.api_url, files=file)
            response_data_scaler = response_scaler.json()
            scaler_url = response_data_scaler.get('file_url')

            if scaler_url:
                print(f"Scaler uploaded successfully. URL: {scaler_url}")
            else:
                print(
                    f"Failed to upload scaler. Error: {response_data_scaler.get('error')}")
                return model_url, None
            
            file = {
                'file': open(self.complete_label_encoder_path, 'rb')
            }

            response_label = requests.post(self.api_url, files=file)
            response_data_label = response_label.json()
            label_url = response_data_label.get('file_url')

            if label_url:
                print(f"label uploaded successfully. URL: {label_url}")
            else:
                print(
                    f"Failed to upload label. Error: {response_data_label.get('error')}")
            
            print(model_url, scaler_url, label_url)
            return model_url, scaler_url, label_url

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {str(e)}")
            return None, None

    def execute(self):
        self.create_model()
        self.train_model()
        self.save_model()
        
        model_url, scaler_url, label_url = self.upload_files_to_api()
        
        _id = str(uuid.uuid4())
        
        model_obj = {
            "modelUrl": model_url if model_url and scaler_url else "",
            "size": os.path.getsize(self.complete_model_path) / (1024 ** 3) if model_url and scaler_url else 0,
            "id": _id if model_url and scaler_url else "",
            "helpers": [{"scaler": scaler_url}, {"label_encoders": label_url}] if model_url and scaler_url else [],
            "modelArch": self.architecture,
            "hyperparameters": self.hyperparameters,
            "epoch_data": self.epoch_data,
            "task": self.task,
            "datasetUrl": self.dataset_url
        }
        print(model_obj)
        return model_obj if model_url and scaler_url else None

# forecaster = Forecaster("https://xanderco-storage.s3-accelerate.amazonaws.com/train5109f33b-7226-4142-ab3c-2c7cc7a57d68.csv", False, "", "", "", {}, {}, "84")

# model = forecaster.execute()
# print(model)
from .AIUnified.RegressionDL import RegressionDL
from .AIUnified.ClassificationDL import ClassificationDL
from .AIUnified.ClassificationDL import ClassificationDL
from .AIUnified.ImageModelTrainer import ImageModelTrainer
from .AIUnified.TextModel import TextModel
import numpy as np
import os
import pandas as pd
import zipfile
import json
import chardet

class Xander:
    def  __init__(self, dataset_path="", model_name="v0", hyperparameters={}, target_col=None, task=""):
        self.hyperparameters = hyperparameters
        self.task = task
        self.dataset_path = dataset_path
        self.architecture = {}
        self.df = None
        self.data_dir = 'extracted_files'
        self.model_name = model_name
        self.target_col = target_col
        self.encoding = ''
        
        self.load()
        
    def remove_whitespace(self, filename):
        return ''.join(filename.split())
    
    def returnArch(self, data, task, mainType, archType):
        current_task = data[task]

        for i in current_task:
            if i["type"] == mainType and i["archType"] == archType:
                return i["architecture"], i["hyperparameters"]
            
    def isText(self, df, columns):
        text = []
        avg_sentence_length_check = []

        for column in columns:
            if df[column].dtype == object:
                text.append(True)
                avg_sentence_length = df[column].dropna().apply(lambda x: len(str(x).split())).mean()
                avg_sentence_length_check.append(avg_sentence_length > 4)
            else:
                text.append(False)
                avg_sentence_length_check.append(False)

        if all(text) and any(avg_sentence_length_check):
            return True
        else:
            return False

    def textToNum(self, finalColumn, x):
        arr = finalColumn.unique()
        indices = np.where(arr == x)[0]
        if indices.size > 0:
            index = indices[0]
            return index
        else:
            return -1
    
    def load(self):
        with open(self.dataset_path, 'rb') as file:
            result = chardet.detect(file.read())
            self.encoding = result['encoding']
        if self.dataset_path.endswith('.csv'):
            self.df = pd.read_csv(self.dataset_path, encoding=self.encoding)
        elif self.dataset_path.endswith('.xlsx'):
            self.df = pd.read_excel(self.dataset_path, encoding=self.encoding)
        elif self.dataset_path.endswith('.zip'):
            self.task ='image'

    def train(self):
        if self.task == 'classification':
            model_trainer = ClassificationDL(
                self.dataset_path, self.architecture, self.hyperparameters, self.model_name, self.target_col
            )
            executor = model_trainer.execute()

            for epoch_info in executor:
                if isinstance(epoch_info, dict) and 'epoch' in epoch_info:
                    print(epoch_info)
                else:
                    print(epoch_info)
                    break
                
        if self.task == 'regression':
            model_trainer = RegressionDL(
                self.dataset_path, self.architecture, self.hyperparameters, self.model_name, self.target_col, self.encoding
            )
            executor = model_trainer.execute()

            for epoch_info in executor:
                if isinstance(epoch_info, dict) and 'epoch' in epoch_info:
                    print(epoch_info)
                else:
                    print(epoch_info)
                    break
                
        if self.task == 'text':
            model_trainer = TextModel(
                self.dataset_path, self.model_name, self.hyperparameters, self.target_col, self.encoding
            )
            for result in model_trainer.execute():
                print(result)

        if self.task == 'image':
            model_trainer = ImageModelTrainer(
                self.dataset_path, self.model_name, self.hyperparameters
            )
            executor = model_trainer.execute()
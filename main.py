from Thyroid_Detection.logger import logging
from Thyroid_Detection.exception import ThyroidException
from  Thyroid_Detection.utils import get_collection_as_dataframe
import os,sys
from  Thyroid_Detection.entity import config_entity
from Thyroid_Detection.components.data_ingestion import DataIngestion
from Thyroid_Detection.components.data_validation import DataValidation
from Thyroid_Detection.components.data_transformation import DataTransformation
from Thyroid_Detection.components.model_trainer import ModelTrainer
from Thyroid_Detection.pipeline.training_pipeline import start_training_pipeline
from Thyroid_Detection.pipeline.batch_prediction import start_batch_prediction
from Thyroid_Detection.predictor import ModelResolver
file_path="hypothyroid_data.csv"

if __name__=="__main__":
    try:
        start_training_pipeline()
        #start_training_pipeline()
        output_file=start_batch_prediction(input_file_path=file_path)
        print(output_file)
    except Exception as e:
        print(e)
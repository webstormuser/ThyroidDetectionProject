from Thyroid_Detection.logger import logging
from Thyroid_Detection.exception import ThyroidException
from  Thyroid_Detection.utils import get_collection_as_dataframe
import os,sys
from  Thyroid_Detection.entity import config_entity
from Thyroid_Detection.components.data_ingestion import DataIngestion
from Thyroid_Detection.components.data_validation import DataValidation
from Thyroid_Detection.components.data_transformation import DataTransformation
from Thyroid_Detection.components.model_trainer import ModelTrainer
from Thyroid_Detection.components.model_evaluation import ModelEvaluation 
from Thyroid_Detection.components.model_pusher import ModelPusher
from Thyroid_Detection.config import TARGET_COLUMN

def start_training_pipeline():
    try:
        training_pipeline_config = config_entity.TrainingPipelineConfig()

        #data ingestion
        data_ingestion_config  = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        
        #data validation
        data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config,
                                        data_ingestion_artifact=data_ingestion_artifact)

        data_validation_artifact = data_validation.initiate_data_validation()



        
        #data transformation
        data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config, 
                                                data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()


        
        #model trainer
        model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainig()
        
        
        
        #model evaluation

        model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
        model_eval  = ModelEvaluation(model_eval_config=model_eval_config,
                                    data_ingestion_artifact=data_ingestion_artifact,
                                    data_transformation_artifact=data_transformation_artifact,
                                    model_trainer_artifact=model_trainer_artifact)
        model_eval_artifact = model_eval.initiate_model_evaluation()
        
        
        
        #Model pusher 
        
        model_pusher_config=config_entity.ModelPusherConfig(training_pipeline_config=training_pipeline_config)
        model_pusher=ModelPusher(model_pusher_config=model_pusher_config,
                                data_transformation_artifact=data_transformation_artifact,
                                model_trainer_artifact=model_trainer_artifact)
        model_pusher_artifact=model_pusher.initiate_model_pusher()
        

        
       
         
    except Exception as e :
        raise ThyroidException(e,sys)
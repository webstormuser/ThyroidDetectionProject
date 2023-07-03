from Thyroid_Detection.entity import artifact_entity,config_entity
from Thyroid_Detection.exception import ThyroidException
from Thyroid_Detection.logger import logging
from Thyroid_Detection.components.data_validation import DataValidation
from typing import Optional
import os,sys 
from sklearn.pipeline import Pipeline
import pandas as pd
from Thyroid_Detection import utils
import numpy as np
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from sklearn.compose import ColumnTransformer
from imblearn.over_sampling import RandomOverSampler
from imblearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from Thyroid_Detection.config import TARGET_COLUMN
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import RFECV
from sklearn.model_selection import StratifiedKFold
from sklearn.impute import SimpleImputer


class DataTransformation:


    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise ThyroidException(e, sys)

    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            Categorical_Features=['sex', 'on_thyroxine', 'query_on_thyroxine','on_antithyroid_medication', 'sick', 'pregnant', 'I131_treatment',
                        'tumor', 'hypopituitary', 'psych']
            Numerical_Features=['age','TSH','T3','TT4','T4U','FTI']
            categorical_transformer = Pipeline(steps=[
                        ('imputer', SimpleImputer(strategy='most_frequent')),
                        ('onehot', OneHotEncoder(drop='first',handle_unknown='ignore'))])
            numeric_transformer =Pipeline(steps=[
                        ('imputer',SimpleImputer(strategy='median',missing_values=np.nan)),
                        ('robust_scaler',RobustScaler())])
            preprocessor = ColumnTransformer([
                            ('num',numeric_transformer,Numerical_Features),
                            ('cat', categorical_transformer, Categorical_Features)])
            pipeline=Pipeline([('preprocessor',preprocessor)])
            return pipeline
        except Exception as e:
            raise ThyroidException(e, sys)



    
    def initiate_data_transformation(self,) -> artifact_entity.DataTransformationArtifact:
        try:
            #reading training and testing file
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            
            #selecting input feature for train and test dataframe
            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)

            #selecting target feature for train and test dataframe
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            label_encoder = LabelEncoder()
            label_encoder.fit(target_feature_train_df)

            #transformation on target columns
            target_feature_train_arr = label_encoder.transform(target_feature_train_df)
            target_feature_test_arr = label_encoder.transform(target_feature_test_df)

            transformation_pipleine = DataTransformation.get_data_transformer_object()
            transformation_pipleine.fit(input_feature_train_df)

            #transforming input features
            input_feature_train_arr = transformation_pipleine.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipleine.transform(input_feature_test_df)

            

            random_over_sample = RandomOverSampler(random_state=42)
            logging.info(f"Before resampling in training set Input: {input_feature_train_arr.shape} Target:{target_feature_train_arr.shape}")
            input_feature_train_arr, target_feature_train_arr = random_over_sample.fit_resample(input_feature_train_arr, target_feature_train_arr)
            logging.info(f"After resampling in training set Input: {input_feature_train_arr.shape} Target:{target_feature_train_arr.shape}")
            
            logging.info(f"Before resampling in testing set Input: {input_feature_test_arr.shape} Target:{target_feature_test_arr.shape}")
            input_feature_test_arr, target_feature_test_arr = random_over_sample.fit_resample(input_feature_test_arr, target_feature_test_arr)
            logging.info(f"After resampling in testing set Input: {input_feature_test_arr.shape} Target:{target_feature_test_arr.shape}")

            #target encoder
            train_arr = np.c_[input_feature_train_arr, target_feature_train_arr ]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]


            #save numpy array
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path,
                                        array=train_arr)

            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path,
                                        array=test_arr)


            utils.save_object(file_path=self.data_transformation_config.transform_object_path,
             obj=transformation_pipleine)

            utils.save_object(file_path=self.data_transformation_config.target_encoder_path,
            obj=label_encoder)



            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path,
                target_encoder_path = self.data_transformation_config.target_encoder_path

            )

            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise ThyroidException(e, sys)
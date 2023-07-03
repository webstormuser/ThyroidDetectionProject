from Thyroid_Detection.exception import ThyroidException
from Thyroid_Detection.logger import logging
from Thyroid_Detection.predictor import ModelResolver
import pandas as pd
from Thyroid_Detection.utils import load_object
import os,sys
from datetime import datetime

class PredictPipeline:
    '''
     This class predict either the patient has Thyroid or not 
    '''
    def __init__(self):pass

    def predict(self,features):
        try:
            '''model_resolver = ModelResolver(model_registry="saved_models")
            transformer = load_object(file_path=model_resolver.get_latest_transformer_path())
            model = load_object(file_path=model_resolver.get_latest_model_path())
            data_scaled=transformer.transform(features)
            prediction = model.predict(data_scaled)
            target_encoder = load_object(file_path=model_resolver.get_latest_target_encoder_path())
            result = target_encoder.inverse_transform(prediction.astype(int))
            return result'''
            transformer_path = 'saved_models/0/transformer/transformer.pkl'
            model_path = 'saved_models/0/model/model.pkl'
            transformer = load_object(file_path = transformer_path)
            model = load_object(file_path = model_path)
            target_encoder_path ='saved_models/0/target_encoder/target_encoder.pkl'
            target_encoder = load_object(file_path = target_encoder_path)
            data_scaled = transformer.transform(features)
            prediction = model.predict(data_scaled)
            cat_prediction = target_encoder.inverse_transform(prediction.astype(int))
            return cat_prediction           
        except Exception as e :
            raise ThyroidException(e,sys)
        
        
class CustomData:
    def __init__(self, sex:str, on_thyroxine:str, query_on_thyroxine:str,
                       on_antithyroid_medication:str, sick:str, pregnant:str, I131_treatment:str,
                       tumor:str,hypopituitary:str,psych:str,
                       age:int,TSH:float,T3:float,TT4:float,T4U:float,FTI:float):
                        self.age=age
                        self.sex=sex
                        self.on_thyroxine=on_thyroxine
                        self.query_on_thyroxine=query_on_thyroxine
                        self.on_antithyroid_medication=on_antithyroid_medication
                        self.sick=sick
                        self.pregnant=pregnant
                        self.I131_treatment=I131_treatment
                        self.tumor=tumor
                        self.hypopituitary=hypopituitary
                        self.psych=psych
                        self.TSH=TSH
                        self.T3=T3
                        self.TT4=TT4
                        self.T4U=T4U
                        self.FTI=FTI
    def get_data_as_data_frame(self):
        try:
            custom_data_as_input_dict={
                "age":[self.age],
                "sex":[self.sex],
                "on_thyroxine":[self.on_thyroxine],
                "query_on_thyroxine":[self.query_on_thyroxine],
                "on_antithyroid_medication":[self.on_antithyroid_medication],
                "sick":[self.sick],
                "pregnant":[self.pregnant],
                "I131_treatment":[self.I131_treatment],
                "tumor":[self.tumor],
                "hypopituitary":[self.hypopituitary],
                "psych":[self.psych],
                "TSH":[self.TSH],
                "T3":[self.T3],
                "TT4":[self.TT4],
                "T4U":[self.T4U],
                "FTI":[self.FTI]
                
            }
            return pd.DataFrame(custom_data_as_input_dict)

        except Exception as e:
                raise ThyroidException(e,sys)
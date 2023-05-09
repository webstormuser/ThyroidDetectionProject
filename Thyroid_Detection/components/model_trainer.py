from Thyroid_Detection.entity import artifact_entity,config_entity
from Thyroid_Detection.exception import ThyroidException
from Thyroid_Detection.logger import logging
from typing import Optional
import os,sys 
from sklearn.tree import DecisionTreeClassifier
from Thyroid_Detection import utils
from sklearn.metrics import f1_score,recall_score


class ModelTrainer:

    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact

        except Exception as e:
            raise ThyroidException(e, sys)

    def train_model(self,x,y):
        try:
            clf=DecisionTreeClassifier()
            clf.fit(x,y)
            return clf
        except Exception as e:
            raise ThyroidException(e,sys)


    def initiate_model_trainig(self,)->artifact_entity.ModelTrainerArtifact:
        try:
            logging.info("loading train and test numpy array for model training ")
            train_arr=utils.load_num_array(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr=utils.load_num_array(file_path=self.data_transformation_artifact.transformed_test_path)


            logging.info(f"Splitting input and target feature from both train and test arr.")
            x_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test = test_arr[:,:-1],test_arr[:,-1]

            logging.info(f"Train the model")
            model = self.train_model(x=x_train,y=y_train)

            logging.info(f"Calculating f1 train score")
            yhat_train = model.predict(x_train)
            f1_train_score  =f1_score(y_true=y_train, y_pred=yhat_train,average='macro')   

            logging.info(f"Calculating recall train score")
            recall_train_score=recall_score(y_true=y_train,y_pred=yhat_train,average='macro')


            logging.info(f" Calculating f1 test score ")
            yhat_test=model.predict(x_test)
            f1_test_score=f1_score(y_true=y_test,y_pred=yhat_test,average='macro')


            logging.info(f" Calculating recall test score")
            recall_test_score=recall_score(y_true=y_test,y_pred=yhat_test,average='macro')


            logging.info(f"train score:{recall_train_score} and tests score {recall_test_score}")
            #check for overfitting or underfiiting or expected score
            logging.info(f"Checking if our model is underfitting or not")
            if recall_test_score<self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it is not able to give \
                expected accuracy: {self.model_trainer_config.expected_score}: model actual score: {recall_test_score}")

            logging.info(f"Checking if our model is overfiiting or not")
            diff = abs(recall_train_score-recall_test_score)
            if diff>self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and test score diff: {diff} is more than overfitting threshold {self.model_trainer_config.overfitting_threshold}")



             #save the trained model
            logging.info(f"Saving mode object")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)


             #prepare artifact
            logging.info(f"Prepare the artifact")
            model_trainer_artifact  = artifact_entity.ModelTrainerArtifact(
                model_path=self.model_trainer_config.model_path, 
                recall_train_score=recall_train_score, 
                recall_test_score=recall_test_score,
                f1_train_score=f1_train_score,
                f1_test_score=f1_test_score)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise ThyroidException(e, sys)
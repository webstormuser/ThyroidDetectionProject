from Thyroid_Detection.entity import artifact_entity,config_entity
from Thyroid_Detection.exception import ThyroidException
from Thyroid_Detection.logger import logging
from scipy.stats import ks_2samp
from scipy.stats import chi2_contingency
from typing import Optional
import os,sys 
import pandas as pd
from Thyroid_Detection import utils
import numpy as np
from Thyroid_Detection.config import TARGET_COLUMN

class DataValidation:


    def __init__(self,
                    data_validation_config:config_entity.DataValidationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.validation_error=dict()
        except Exception as e:
            raise ThyroidException(e, sys)

    def drop_missing_values_columns(self,df:pd.DataFrame,report_key_name:str)->Optional[pd.DataFrame]:
        """
        This function will drop column which contains missing value more than specified threshold
        df: Accepts a pandas dataframe
        threshold: Percentage criteria to drop a column
        =====================================================================================
        returns Pandas DataFrame if atleast a single column is available after missing columns drop else None
        """
        try:
            
            threshold = self.data_validation_config.missing_threshold
            null_report = df.isna().sum()/df.shape[0]
            #selecting column name which contains null
            logging.info(f"selecting column name which contains null above to {threshold}")
            drop_column_names = null_report[null_report>threshold].index

            logging.info(f"Columns to drop: {list(drop_column_names)}")
            self.validation_error[report_key_name]=list(drop_column_names)
            df.drop(list(drop_column_names),axis=1,inplace=True)

            #return None no columns left
            if len(df.columns)==0:
                return None
            return df
        except Exception as e:
            raise ThyroidException(e, sys)

    def drop_unrelevant_columns(self,df:pd.DataFrame,column_list:list,report_key_name:str)->Optional[pd.DataFrame]:
        '''This function drops the unrelevant columns from the dataset both from train and test '''
        try:
            unrelevant_columns=self.data_validation_config.unrelevant_columns
            #droppping unrelevant columns which are not usefull for model bulding 
            logging.info(f" Dropping unrelevant columns from train and test file")
            logging.info(f" Columns to drop :{unrelevant_columns}")
            df.drop(unrelevant_columns,axis=1,inplace=True)
            #return None no columns left
            if len(df.columns)==0:
                return None
            return df
        except Exception as e:
            raise ThyroidException(e, sys)



    def is_required_columns_exists(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:
        try:
           
            base_columns = base_df.columns
            current_columns = current_df.columns

            missing_columns = []
            for base_column in base_columns:
                if base_column not in current_columns:
                    logging.info(f"Column: [{base} is not available.]")
                    missing_columns.append(base_column)

            if len(missing_columns)>0:
                self.validation_error[report_key_name]=missing_columns
                return False
            return True
        except Exception as e:
            raise ThyroidException(e, sys)
        
        
        
    def check_data_drift_categorical(self,base_df:pd.DataFrame, current_df:pd.DataFrame, feature):
        """
        Checks data drift for a categorical feature using the chi-square test.

        Args:
            data1 (list or array): First dataset containing the feature.
            data2 (list or array): Second dataset containing the feature.
            feature (str): Name of the categorical feature.

        Returns:
            drift (bool): True if there is significant data drift, False otherwise.
            p_value (float): The p-value of the chi-square test.
        """
        # Create frequency tables for the feature in both datasets
        table1 = np.unique(base_df, return_counts=True)
        table2 = np.unique(current_df, return_counts=True)

        # Combine the two tables into a single table
        all_values = set(table1[0]).union(set(table2[0]))
        combined_table = {val: [0, 0] for val in all_values}

        for val, count in zip(table1[0], table1[1]):
            combined_table[val][0] = count

        for val, count in zip(table2[0], table2[1]):
            combined_table[val][1] = count

        # Convert the combined table into an array
        contingency_table = np.array(list(combined_table.values())).T

        # Perform chi-square test
        _, p_value, _, _ = chi2_contingency(contingency_table)

        # Determine if there is data drift based on the p-value
        drift = p_value < 0.05

        return drift, p_value
        
        

    
    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        try:
            drift_report=dict()
            categorical_cols_base_df = base_df.select_dtypes(include=['object']).columns
            categorical_cols_current_df=current_df.select_dtypes(include=['object']).columns
            base_columns_num= base_df.select_dtypes(include=['number']).columns
            current_columns_num= current_df.select_dtypes(include=['number']).columns

            #Checking data drift for numerical Features
            for base_column in base_columns_num:
                base_data,current_data = base_df[base_column],current_df[base_column]
                #Null hypothesis is that both column data drawn from same distrubtion
                
                logging.info(f"Hypothesis {base_column}: {base_data.dtype}, {current_data.dtype} ")
                same_distribution =ks_2samp(base_data,current_data)

                if same_distribution.pvalue>0.05:
                    #We are accepting null hypothesis
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution": True
                    }
                else:
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution":False
                    }
                    #different distribution
                           
            #Checking data drift for categorical features 
            for col in categorical_cols_base_df:
                base_data,current_data=base_df[col],current_df[col]
                logging.info(f"Hypothesis {col}: {base_data.dtype}, {current_data.dtype} ")
                drift, p_value = self.check_data_drift_categorical(categorical_cols_base_df,categorical_cols_current_df ,'features')  
                if drift:
                    drift_report[col]={
                        "p_values":float(p_value),
                        "same_distribution":False
                    }               
                else:
                    drift_report[col]={
                        "p_values":float(p_value),
                        "same_distribution":True
                    }            

            self.validation_error[report_key_name]=drift_report
        except Exception as e:
            raise ThyroidException(e, sys)
    
    
    
    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            unrelevant_columns=self.data_validation_config.unrelevant_columns

            logging.info(f"Reading base dataframe")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            #base_df has na as null
            logging.info(f"Drop null values colums from base df")
            base_df=self.drop_missing_values_columns(df=base_df,report_key_name="missing_values_within_base_dataset")

            logging.info(f"Reading train dataframe")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info(f"Reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            
          
            logging.info(f"Drop null values colums from train df")
            train_df = self.drop_missing_values_columns(df=train_df,report_key_name="missing_values_within_train_dataset")
            logging.info(f"Drop null values colums from test df")
            test_df = self.drop_missing_values_columns(df=test_df,report_key_name="missing_values_within_test_dataset")

            logging.info(f"Selected features from Feature selection technique Using REFCV are sex, on_thyroxine,query_on_thyroxine,on_antithyroid_medication,sick,pregnant,I131_treatment,tumor,hypopituitary,psych,TSH,T3,TT4, T4U,FTI")
            
            logging.info(f"Dropping unrelevent columns from base df")
            base_df=self.drop_unrelevant_columns(df=base_df,column_list=unrelevant_columns,report_key_name="dropping_unrelevent_columns_from_base_df")
            
            logging.info(f" Dropping unrelevent columns from train_df")
            train_df=self.drop_unrelevant_columns(df=train_df,column_list=unrelevant_columns,report_key_name="dropping_unrelevent_columns_frombase_df")

            logging.info(f" Dropping unrelevent columns from test_df")
            test_df=self.drop_unrelevant_columns(df=test_df,column_list=unrelevant_columns,report_key_name="dropping_unrelevent_columns_frombase_df")

            


            logging.info(f"Is all required columns present in train df")
            train_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=train_df,report_key_name="missing_columns_within_train_dataset")
            logging.info(f"Is all required columns present in test df")
            test_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=test_df,report_key_name="missing_columns_within_test_dataset")


            if train_df_columns_status:
                logging.info(f"As all column are available in train df hence detecting data drift")
            self.data_drift(base_df=base_df, current_df=train_df,report_key_name="data_drift_within_train_dataset")
            if test_df_columns_status:
                logging.info(f"As all column are available in test df hence detecting data drift")
            self.data_drift(base_df=base_df, current_df=test_df,report_key_name="data_drift_within_test_dataset")


            #write the report
            logging.info("Write reprt in yaml file")
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path,
                                data=self.validation_error)
            logging.info(f"{base_df.columns}")
            logging.info(f"{train_df.columns}")
            logging.info(f"{test_df.columns}")

            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path,)
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise ThyroidException(e,sys)
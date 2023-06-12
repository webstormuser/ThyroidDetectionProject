import pymongo
import pandas as pd
import json
from dataclasses import dataclass
# Provide the mongodb localhost url to connect python to mongodb.
import os
@dataclass
class EnvironmentVariable:
    mongo_db_url:str = os.getenv("MONGO_DB_URL")
    aws_access_key_id:str = os.getenv("AWS_ACCESS_KEY_ID")
    aws_access_secret_key:str = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region:str=os.getenv("AWS_REGION")
    bucket_name:str=os.getenv("BUCKET_NAME")
    aws_ecr_login_uri:str=os.getenv("AWS_ECR_LOGIN_URI")
    ecr_repository_name:str=os.getenv("ECR_REPOSITORY_NAME")
    


env_var = EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN = "Class"
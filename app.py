from flask import Flask ,request,render_template
from flask_cors import CORS,cross_origin
from Thyroid_Detection.exception import ThyroidException
import os,sys
import os
import pandas as pd 
import numpy as np
from sklearn.preprocessing import StandardScaler
from Thyroid_Detection.predictor import ModelResolver
#from Insurance_Prediction.pipeline.training_pipeline import start_training_pipeline
from Thyroid_Detection.pipeline.batch_prediction import CustomData,start_batch_prediction,PredictPipeline
from Thyroid_Detection.utils import load_object
from dotenv import load_dotenv
load_dotenv()

application= Flask(__name__)
app=application

model_resolver = ModelResolver(model_registry="saved_models")
@app.route('/', methods=['GET'])  # route to display the Home page
@cross_origin()
def home():
    return render_template('home.html')

@app.route('/prediction',methods=['GET','POST'])
def predict_data():
    if request.method=='GET':
        return render_template('home.html')
    else:
        data=CustomData(
            age=int(request.form.get('age')),
            sex=request.form.get('sex'),
            on_thyroxine=request.form.get('on_thyroxine'),
            query_on_thyroxine=request.form.get('query_on_thyroxine'),
            on_antithyroid_medication=request.form.get('on_antithyroid_medication'),
            sick=request.form.get('sick'),
            pregnant=request.form.get('pregnant'),
            tumor=request.form.get('tumor'),
            hypopituitary=request.form.get('hypopituitary'),
            I131_treatment=request.form.get('I131_treatment'),
            psych=request.form.get('psych'),
            TSH=float(request.form.get('TSH')),
            T3=float(request.form.get('T3')),
            TT4=float(request.form.get('TT4')),
            T4U=float(request.form.get('T4U')),
            FTI=float(request.form.get('FTI'))      
            
        )
        pred_df=data.get_data_as_data_frame()
        print(pred_df)
        predict_pipeline=PredictPipeline()
        prediction=predict_pipeline.predict(pred_df)
        result=prediction
        return render_template('home.html',result=result[0])

if __name__ == '__main__': 
    try:
        app.run(host='0.0.0.0',port=5002,debug=True)
        #app.run(host='0.0.0.0')
    except Exception as e:
        raise ThyroidException(e,sys)
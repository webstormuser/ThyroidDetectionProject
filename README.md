# Thyroid Disease Detection

Thyroid disease is a very common problem in India, more than one crore people are suffering with the disease every year. Thyroid disorder can speed up or slow down the metabolism of the body.

The main objective of this project is to predict if a person is having compensated hypothyroid, primary hypothyroid, secondary hypothyroid or negative (no thyroid) with the help of Machine Learning. Classification algorithms such as Random Forest, XGBoost and KNN Model have been trained on the thyroid dataset, UCI Machine Learning repository. After hyperparameter tuning XGBoost model has performed well with better accuracy, precision and recall. Application has deployed on Heroku with the help of flask framework.
 


# Technical Aspects: 

*  Python 3.7 and more

*  Important Libraries: sklearn, pandas, numpy, matplotlib & seaborn

*  Front-end: HTML, CSS

*  Back-end: Flask framework

*  IDE: Jupyter Notebook, Pycharm or  VSCode

*  Database: MongoDB

*  Deployment: Heroku or  AWS

# How to run this app :

* Code is written in Python 3.9.7 and more. If you don't have python installed on your system, click here https://www.python.org/downloads/ to install. 

*  Create virtual environment - conda create -n myenv python=3.9.7
      
*  Activate the environment - conda activate myenv

*  Install the packages - pip install -r requirements.txt
      
*  Run the app - python run app.py

# Work Flow of Project:

# Data Collection :
            Thyroid Disease Data Set from UCI Machine Learning Repository.
                  Link:https://archive.ics.uci.edu/ml/datasets/thyroid+disease

*  Data Cleaning and Preprocessing :

1. Removing unwanted spaces in column names 

2. Detecting null values and handling by SimpleImputer for Categorical and Numerical data 

3. Categorical Features handling by onehot encoding

4. Encoding Target column by label encoding 

5. Feature scaling by StandardScaling 

6. Handling imbalanced dataset 

7. Selecting best features and dropping useless features 


# Model Creation and Evaluation
Various classification algorithms like Random Forest, Decision Tree Classifier ,XGBoost, KNN etc tested.
Decision Tree and Random Forest  performed well. Decision Tree Classiifier  chosen for the final model training and testing.

  curl -fsSL https://get.docker.com -o get-docker.sh
  
      sudo sh get-docker.sh
  
      sudo usermod -aG docker ubuntu
  
      newgrp docker



   Credentials required to Run hosted runner using github actions 
   
   
    **AWS_ACCESS_KEY_ID=
    
    **AWS_SECRET_ACCESS_KEY=
    
    **AWS_REGION=
    
    **AWS_ECR_LOGIN_URI=
    
    **ECR_REPOSITORY_NAME=
    
    **BUCKET_NAME=
    
    **MONGO_DB_URL=

# Demo 
[![Project Demo](https://drive.google.com/file/d/1cqu37oxR8wZfpl3X7gywF-9LOV15sgrx/view?usp=drive_link)](https://drive.google.com/file/d/1cqu37oxR8wZfpl3X7gywF-9LOV15sgrx/view?usp=drive_link)


# Deployment Webpage Link 
[!Deployement Web link](http://thyroiddetection-env.eba-pbzqihkx.us-east-1.elasticbeanstalk.com/)



# Output 

![UserInput](Capture.PNG)

![Prediction](Capture2.PNG)
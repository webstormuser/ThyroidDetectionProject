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

* Data Collection :
            Thyroid Disease Data Set from UCI Machine Learning Repository.
                  Link:https://archive.ics.uci.edu/ml/datasets/thyroid+disease

* Data Cleaning and Preprocessing :
      *  Removing unwanted spaces in column names 
      *  Detecting null values and handling by SimpleImputer for Categorical and Numerical data 
      *  Categorical Features handling by onehot encoding 
      *  Encoding Target column by label encoding 
      *  Feature scaling by StandardScaling 
      *  Handling imbalanced dataset 
      *  Selecting best features and dropping useless features 


# Model Creation and Evaluation
      Various classification algorithms like Random Forest, Decision Tree Classifier ,XGBoost, KNN etc tested.
      Decision Tree and Random Forest  performed well. Decision Tree Classiifier  chosen for the final model training and testing.


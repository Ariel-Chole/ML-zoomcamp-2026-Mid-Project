#importing required packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb

from IPython import display

#Import the dataset 
df = pd.read_csv("C:\\Users\\User\\Documents\\GitHub\\ML-zoomcamp-2026-Homeworks\\mid_term\\Life Expectancy Data.csv")

#re-formatting the column names into a consistent format
df.columns = df.columns.str.strip().str.lower().str.replace(" ","_")

#As my target life_expectancy has missing values, I will drop them. 
df.dropna(subset=["life_expectancy"],inplace=True)

#my target feature
target = "life_expectancy"

#preparing dataset for model training
X_train = df.drop(columns=[target]).reset_index(drop=True)
y_train = df[[target]].reset_index(drop=True)


#filling missing values with "0"
X_train =X_train.fillna(0)

#Building DictVectorizer Transformer
dv = DictVectorizer(sparse=False)
train_dicts = X_train.to_dict(orient="records")

train_encod = dv.fit_transform(train_dicts)

#I need to create DMatrix to use xgboost
features = list(dv.get_feature_names_out())

dtrain = xgb.DMatrix(train_encod,label=y_train,feature_names=features)

#The final choice XGBoost Model 
xgb_params = {
    'eta': 0.1, 
    'max_depth': 6,
    'min_child_weight': 1,
    
    'objective': 'reg:squarederror',
    'nthread': 8,
    
    'seed': 1,
    'verbosity': 1,
}

model = xgb.train(xgb_params,dtrain,num_boost_round = 251)

#building a pipeline
pipeline = {
    "model":model,
    "dv" : dv
}

# Save the model
import pickle

output_file = f"life-expectancy-model.bin"

with open(output_file,"wb") as f_out:
    pickle.dump(pipeline,f_out)
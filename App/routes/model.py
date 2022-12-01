#!/usr/local/bin/python
import pandas as pd 
import plotly.express as px 
import seaborn as sns 
import matplotlib.pyplot as plt
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.ensemble import RandomForestRegressor

X = pd.read_csv('X_veloc.csv')

print(X)
y = pd.read_csv('y_veloc.csv')
print(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

categorial = ['weather', 'week','month', 'hours', 'workingday', 'holiday']
continuous = ['temp','humidity', 'windspeed']

preprocessor = make_column_transformer((OneHotEncoder(),categorial), (StandardScaler(), continuous), remainder='passthrough')

model = make_pipeline(preprocessor,RandomForestRegressor(
    warm_start=True, oob_score=True, 
    min_samples_split=2, min_impurity_decrease=0.001, 
    max_features='auto', 
    criterion='squared_error', ccp_alpha=0.001))


model.fit(X_train, y_train)
print('R2: ',model.score(X_test, y_test))
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print(y_test.isna().sum())
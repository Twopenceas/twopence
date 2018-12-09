# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 10:13:02 2018

@author: twope
"""

import pandas as pd
import numpy as np
import re
import json
import time
from pandas.io.json import json_normalize
from sklearn.preprocessing import LabelEncoder 
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
import lightgbm as lgb

url_train = r'D:\DATA\python files\kaggle_kernel\google_revenue_prediction\train_v2.csv'
url_test = r'D:\DATA\python files\kaggle_kernel\google_revenue_prediction\test_v2.csv'
url_train = re.sub(r'\\',r'/',url_train)
url_test = re.sub(r'\\',r'/',url_test)

def single2double(x):
    x = re.sub(r'\'',r'"',x)
    json.loads(x)
    x = re.sub(r'"',r'',x)
    return x

def load_df(csv_path= url_train , nrows=None):
    starttime = time.time()
    chunks = []
    loop = True
    chunk_size = 1000
    
    columns_use = ['channelGrouping',
                    'customDimensions',
                    'date',
                    'device', 
                    'fullVisitorId',
                    'geoNetwork',
                    'socialEngagementType',
                    'totals',
                    'trafficSource',
                    'visitId',
                    'visitNumber',
                    'visitStartTime']
    data = pd.read_csv(csv_path,
                       converters={'customDimensions':single2double,
                                   'device':json.loads,
                                   'geoNetwork':json.loads,
                                   'totals':json.loads,
                                   'trafficSource':json.loads},
                       dtype={'fullVisitorId': 'str'},                                    
                       usecols = columns_use,
                       iterator =True)

                      
    while loop:
        try:
            chunk = data.get_chunk(chunk_size)
            chunks.append(chunk)
        except StopIteration:
            loop = False
            print('Iteration is stopped')   
    sample = pd.concat(chunks,axis = 0)

    time_use = time.time() - starttime
    print(f'use {time_use}s')
    return sample

train_df = load_df()
test_df = load_df(url_test)

def json_split(df):
    JSON_COLUMNS = ['device','geoNetwork','totals','trafficSource']
    for column in JSON_COLUMNS:
        columns_as_df = json_normalize(df[column].values.tolist())
        columns_as_df.columns = [f"{column}_{subcolumn}" for subcolumn in columns_as_df.columns]
        df = df.drop(column, axis=1).merge(columns_as_df, right_index=True, left_index=True)
    return df

train_df = json_split(train_df)
test_df =json_split(test_df)
def customer(df):
    starttime = time.time()
    df.loc[df['customDimensions'] == '[]','customDimensions'] = '[{index: notknow, value: notknow}]'
    df['customDimensions'] = df['customDimensions'].apply(lambda x: re.findall(r'(?<={).+(?=})',x)[0])
    column_cus = df['customDimensions'].str.split(',',expand = True)
    column_cus = column_cus.applymap(lambda x:re.findall(r'(?<=\: ).+',x)[0])
    column_cus.rename(columns = {0:'customDimensions_index',
                                 1:'customDimensions_value'},
                      inplace = True)
    df = df.drop('customDimensions',axis = 1).merge(column_cus,
                                                    right_index = True,
                                                    left_index = True)
    time_use = time.time() - starttime
    print('use %ss'%time_use)
    return df
train_df = customer(train_df)
test_df = customer(test_df)

#date列



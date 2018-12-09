# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 22:43:48 2018

@author: twope
"""
def date_split(df):
    df['date'] = pd.to_datetime(df['visitStartTime'], unit='s')
    df["day"] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['weekday'] = df['date'].dt.weekday
    df['weekofyear'] = df['date'].dt.weekofyear
    return df
    
train_df = date_split(train_df)
test_df = date_split(test_df)


train_df.drop(['trafficSource_referralPath', 'trafficSource_source'], axis=1, inplace=True)
test_df.drop(['trafficSource_referralPath', 'trafficSource_source'], axis=1, inplace=True)

dropcol1 = [col for col in train_df.columns if train_df[col].nunique(dropna = False) == 1]
print(f'the name of the droped features {dropcol1}')
train_df.drop(dropcol1,axis = 1,inplace = True)
train_df.drop('trafficSource_campaignCode',axis = 1,inplace = True)#test里面没有

dropcol2 = [col for col in test_df.columns if test_df[col].nunique(dropna = False) == 1]
print(f'the name of the droped features {dropcol2}')
test_df.drop(dropcol2,axis = 1,inplace = True)

def process_totals(data_df):
    data_df['totals_transactionRevenue'] = train_df['totals_transactionRevenue'].astype('float')
    data_df['totals_pageviews']=train_df['totals_pageviews'].astype('float')
    data_df['totals_hits']=train_df['totals_hits'].astype('float')
    data_df['visitNumber'] = np.log1p(data_df['visitNumber'])
    data_df['totals_hits'] = np.log1p(data_df['totals_hits'])
    data_df['totals_pageviews'] = np.log1p(data_df['totals_pageviews'].fillna(0))
    data_df['totals_pageviews_mean'] = data_df.groupby(['fullVisitorId'])['totals_pageviews'].transform('mean')
    data_df['totals_pageviews_max'] = data_df.groupby(['fullVisitorId'])['totals_pageviews'].transform('max')
    data_df['totals_pageviews_min'] = data_df.groupby(['fullVisitorId'])['totals_pageviews'].transform('min')
    data_df['totals_hits_mean'] = data_df.groupby(['fullVisitorId'])['totals_hits'].transform('mean')
    data_df['totals_hits_max'] = data_df.groupby(['fullVisitorId'])['totals_hits'].transform('max')
    data_df['totals_hits_min'] = data_df.groupby(['fullVisitorId'])['totals_hits'].transform('min')
    return data_df

train_df = process_totals(train_df)  
test_df = process_totals(test_df)
test_df.shape
test_df.info()

def one_hot_feature(df):
    one_hot_features = ['day','month','weekday']    
    
    
    for i in one_hot_features:
        print("Process feature =====>"+str(i))
        df["one_hot_feature"] = df[i]
        df["one_hot_feature"] =  str(i) + "." + df["one_hot_feature"].astype('str')
        one_hot_combine = pd.get_dummies(df["one_hot_feature"])
        print(one_hot_combine.shape)
        df = df.join(one_hot_combine)
        del df["one_hot_feature"]
        del df[i]
        del one_hot_combine
        print(df.shape)

    return df


    
    

train_df = one_hot_feature(train_df)
train_df.shape
train_df.info()
test_df = one_hot_feature(test_df)      
test_df.info()
test_df.shape
test_df['date']

excluded_features = [
    'date','fullVisitorId', 'sessionId','classfication_target','totals_transactionRevenue','totals_totalTransactionRevenue',
    'visitId', 'visitStartTime', 'vis_date', 'nb_sessions', 'max_visits','next_session_1','next_session_2'
]
categorical_features = [
    _f for _f in train_df.columns
    if (_f not in excluded_features) & (train_df[_f].dtype == 'object')
]
categorical_features_test = [
    _f for _f in test_df.columns
    if (_f not in excluded_features) & (test_df[_f].dtype == 'object')
]


for f in categorical_features:
    train_df[f], indexer = pd.factorize(train_df[f])
    
for f in categorical_features_test:
    test_df[f], indexer = pd.factorize(test_df[f])




train_period_1 = train_df[(train_df['date']<=pd.datetime(2017,1,15)) & (train_df['date']>=pd.datetime(2016,8,1))]
train_predict_preiod_1 = train_df[(train_df['date']<=pd.datetime(2017,4,30)) & (train_df['date']>=pd.datetime(2017,3,1))]
train_period_2 = train_df[(train_df['date']<=pd.datetime(2017,11,15)) & (train_df['date']>=pd.datetime(2017,6,1))]
train_predict_preiod_2 = train_df[(train_df['date']<=pd.datetime(2018,2,28)) & (train_df['date']>=pd.datetime(2018,1,1))]
valid_period = train_df[(train_df['date']<=pd.datetime(2017,10,15)) & (train_df['date']>=pd.datetime(2017,5,1))]
valid_predict_preiod = train_df[(train_df['date']<=pd.datetime(2018,1,31)) & (train_df['date']>=pd.datetime(2017,12,1))]


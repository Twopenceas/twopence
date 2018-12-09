# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 19:45:42 2018

@author: twope
"""

'''
加入一个新feature
'''
def future_revenue(df):
    period_future = df.groupby('fullVisitorId')['totals_transactionRevenue'].sum()
    period_future = period_future.reset_index()
    period_future.rename(columns = {'totals_transactionRevenue':'feature_revenue'},
                         inplace = True)
    period_future['feature_revenue'] = np.log1p(period_future['feature_revenue'])
    return period_future

period1_future_revenue = future_revenue(train_predict_preiod_1)
period2_future_revenue = future_revenue(train_predict_preiod_2)
valid_future_revenue = future_revenue(valid_predict_preiod)

def fill(train_period,target_period):
    
    train_period['totals_totalTransactionRevenue'] = train_period['totals_totalTransactionRevenue'].fillna(0).astype('float64')
    target_period['totals_totalTransactionRevenue'] =target_period['totals_totalTransactionRevenue'].fillna(0).astype('float64')
    train_period['totals_transactionRevenue'] = train_period['totals_transactionRevenue'].fillna(0).astype('float64')
    target_period['totals_transactionRevenue'] = target_period['totals_transactionRevenue'].fillna(0).astype('float64')
    revenue_train = train_period.groupby('fullVisitorId')['totals_transactionRevenue'].sum().values
    revenue_target = target_period.groupby('fullVisitorId')['totals_transactionRevenue'].sum().values
    target_pd = target_period.groupby('fullVisitorId').mean().reset_index()
    target_pd['totals_transactionRevenue'] = revenue_target
    train_pd = train_period.groupby('fullVisitorId').mean().reset_index()
    train_pd['totals_transactionRevenue'] = revenue_train
    #target_pd=target_period
    #Find the visitors those back puchased in future period
    train_visitors = train_pd['fullVisitorId'].unique()
    train_predict_visitors = target_pd['fullVisitorId'].unique()
    same_visitors = np.intersect1d(train_visitors, train_predict_visitors)
    back_user = target_pd[(target_pd['fullVisitorId'].isin(same_visitors)) & (target_pd['totals_transactionRevenue'] > 0)]
    back_user = back_user[['fullVisitorId','totals_transactionRevenue']]
    print(f'numbers of back users is {len(same_visitors)}')
    print('we have',len(back_user['fullVisitorId'].value_counts()),'visitors back to purchase at target periods')
    
    train_pd['classfication_target'] = train_pd['fullVisitorId'].map(lambda x: 1 if x in list(back_user['fullVisitorId']) else 0)
    train_pd['totals_totalTransactionRevenue'] = np.log1p(train_pd['totals_totalTransactionRevenue'])
    train_pd['totals_transactionRevenue'] = np.log1p(train_pd['totals_transactionRevenue'])
    print (train_pd.shape)
    return train_pd

train_pd_1= fill(train_period_1,train_predict_preiod_1)#对应 train_period_1
train_pd_2= fill(train_period_2,train_predict_preiod_2)#对应 train_period_2
valid_pd = fill(valid_period,valid_predict_preiod)#就是valid_period

#把符合长度的feature_revenue做出来
train_pd_1['feature_revenue'] = 0
train_pd_1 = pd.merge(train_pd_1,period1_future_revenue,
                      on = 'fullVisitorId',
                      how = 'left')
train_pd_1.info()
train_pd_1['feature_revenue_y'].fillna(0,inplace = True)
train_pd_1.drop('feature_revenue_x',axis = 1,inplace = True)
train_pd_1.rename(columns = {'feature_revenue_y':'feature_revenue'},
                  inplace = True)


train_pd_2['feature_revenue'] = 0
train_pd_2 = pd.merge(train_pd_2,period2_future_revenue,
                      on = 'fullVisitorId',
                      how = 'left')
train_pd_2.info()
train_pd_2['feature_revenue_y'].fillna(0,inplace = True)
train_pd_2.drop('feature_revenue_x',axis = 1,inplace = True)
train_pd_2.rename(columns = {'feature_revenue_y':'feature_revenue'},
                  inplace = True)

valid_pd['feature_revenue'] = 0
valid_pd = pd.merge(valid_pd,valid_future_revenue,
                        on = 'fullVisitorId',
                        how = 'left')
valid_pd.info()
valid_pd['feature_revenue_y'].fillna(0,inplace = True)
valid_pd.drop('feature_revenue_x',axis = 1,inplace = True)
valid_pd.rename(columns = {'feature_revenue_y':'feature_revenue'},
                    inplace = True)


train_set = pd.concat([train_pd_1,train_pd_2], axis=0)
excluded_features = [
    'date','fullVisitorId', 'sessionId','classfication_target','feature_revenue',
    'visitId', 'visitStartTime', 'vis_date', 'nb_sessions', 'max_visits','next_session_1','next_session_2'
]
train_features = [_f for _f in train_set.columns if _f not in excluded_features ]


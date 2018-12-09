# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 09:49:34 2018

@author: twope
"""

    
test_df['totals_totalTransactionRevenue'] = test_df['totals_totalTransactionRevenue'].fillna(0).astype('float64')
test_df['totals_transactionRevenue'] = test_df['totals_transactionRevenue'].fillna(0).astype('float64')
revenue_test = test_df.groupby('fullVisitorId')['totals_transactionRevenue'].sum().values
test_df = test_df.groupby('fullVisitorId').mean().reset_index()
test_df['totals_transactionRevenue'] = revenue_test
test_df['totals_totalTransactionRevenue'] = np.log1p(test_df['totals_totalTransactionRevenue'])
test_df['totals_transactionRevenue'] = np.log1p(test_df['totals_transactionRevenue'])
for column in ['month.1','month.11','month.12','month.2','month.3','month.4']:
    test_df[column] = 0
    test_df[column] = test_df[column].astype('float')
set(train_set.columns).difference(set(test_df.columns))
test_df.shape


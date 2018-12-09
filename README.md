# twopence
Kggle match Google Analytics Customer Revenue Prediction
The Private LB is being calculated on the future-looking timeframe of 12/1/18 to 1/31/19 - for those same set of users in test_v2 dataset.（1）这次比赛的数据集中因为是通过Google Analytics对G-store数据的抓取，所以数据集中有一部分数据是json形式，在清洗数据时要将这部分数据转化为python可以处理的格式.主要是json.loads(),json_normalize(),ast包中的literal_eval函数.
(2)plotly 是一款非常强大的画图工具,可以在线或者离线使用，需要先编写trace，再创建fig，最后使用append_trace将plotly投到fig上

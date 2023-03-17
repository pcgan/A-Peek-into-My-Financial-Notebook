import pandas as pd
from datetime import datetime
from iFinDPy import *



thsLogin = THS_iFinDLogin("iFind账号","iFind账号密码")


index_list = ['000001.SH','399001.SZ','399006.SZ']
result = pd.DataFrame()
today =datetime.today().strftime('%Y-%m-%d')

for index in index_list: 
    data_js = THS_DateSerial(index,'ths_pre_close_index;ths_open_price_index;ths_close_price_index;ths_high_price_index',';;;',\
                             'Days:Tradedays,Fill:Previous,Interval:D,block:history','2000-01-01',today,True)
    data_df = THS_Trans2DataFrame(data_js)
    data_df['close_chg'] = data_df['ths_close_price_index'] / data_df['ths_pre_close_index'] * 100 - 100
    result_pd = data_df[(data_df['close_chg'] < -5)]
    date_list = result_pd['time'].tolist()
    print('{}收盘在-5%的交易日有{}'.format(index,str(date_list)))
    for date in date_list:
        date_after_1month = THS_DateOffset('SSE','dateType:1,period:D,offset:30,dateFormat:0,output:singledate',date)['tables']['time'][0]
        date_after_3month = THS_DateOffset('SSE','dateType:1,period:D,offset:90,dateFormat:0,output:singledate',date)['tables']['time'][0]
        date_after_1year = THS_DateOffset('SSE','dateType:1,period:D,offset:365,dateFormat:0,output:singledate',date)['tables']['time'][0]
        if date > (datetime.today() + timedelta(days=-365)).strftime('%Y-%m-%d'):
            continue
        index_close_date = THS_BasicData(index,'ths_close_price_index',date)['tables'][0]['table']['ths_close_price_index'][0]
        index_close_date_after_1month = THS_BasicData(index,'ths_close_price_index',date_after_1month)['tables'][0]['table']['ths_close_price_index'][0]
        index_close_date_after_3month = THS_BasicData(index,'ths_close_price_index',date_after_3month)['tables'][0]['table']['ths_close_price_index'][0]
        index_close_date_after_1year = THS_BasicData(index,'ths_close_price_index',date_after_1year)['tables'][0]['table']['ths_close_price_index'][0]
        result = result.append(pd.DataFrame([index,date,index_close_date,index_close_date_after_1month,index_close_date_after_3month,index_close_date_after_1year]).T)
result.columns = ['指数代码','大跌日','大跌日点数','一个月后点数','三个月后点数','一年后点数']
result = result.set_index('指数代码')
result['大跌一个月后涨跌幅'] = result['一个月后点数']/result['大跌日点数'] *100 -100
result['大跌三个月后涨跌幅'] = result['三个月后点数']/result['大跌日点数'] *100 -100
result['大跌一年后涨跌幅'] = result['一年后点数']/result['大跌日点数'] *100 -100
result
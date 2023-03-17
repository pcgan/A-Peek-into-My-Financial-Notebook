import requests
import json
import time
import pandas as pd

# 取消panda科学计数法,保留4位有效小数位.
pd.set_option('float_format', lambda x: '%.2f' % x)
# 设置中文对齐,数值等宽对齐.
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 500)

# Token accessToken 及权限校验机制
getAccessTokenUrl = 'https://quantapi.51ifind.com/api/v1/get_access_token'
# 获取refresh_token需下载Windows版本接口包解压，打开超级命令-工具-refresh_token查询
refreshtoken = '此处填写refresh_token'
getAccessTokenHeader = {"Content- Type": "application/json", "refresh_token": refreshtoken}
getAccessTokenResponse = requests.post(url=getAccessTokenUrl, headers=getAccessTokenHeader)
accessToken = json.loads(getAccessTokenResponse.content)['data']['access_token']
print(accessToken)

thsHeaders = {"Content-Type": "application/json", "access_token": accessToken}


# 高频序列：获取分钟数据
def high_frequency():
    thsUrl = 'https://quantapi.51ifind.com/api/v1/high_frequency'
    thsPara = {"codes":
                   "000001.SZ",
               "indicators":
                   "open,high,low,close,volume,amount,changeRatio",
               "starttime":
                   "2022-07-05 09:15:00",
               "endtime":
                   "2022-07-05 15:15:00"}
    thsResponse = requests.post(url=thsUrl, json=thsPara, headers=thsHeaders)
    print(thsResponse.content)


# 实时行情：循环获取最新行情数据
def real_time():
    thsUrl = 'https://quantapi.51ifind.com/api/v1/real_time_quotation'
    thsPara = {"codes": "300033.SZ", "indicators": "latest"}
    while True:
        thsResponse = requests.post(url=thsUrl, json=thsPara, headers=thsHeaders)
        data = json.loads(thsResponse.content)
        result = pd.json_normalize(data['tables'])
        result = result.drop(columns=['pricetype'])
        result = result.apply(lambda x: x.explode().astype(str).groupby(level=0).agg(", ".join))
        print(result)
        # do your thing here
        time.sleep(3)
        pass


# 历史行情：获取历史的日频行情数据
def history_quotes():
    thsUrl = 'https://quantapi.51ifind.com/api/v1/cmd_history_quotation'
    thsPara = {"codes":
                   "000001.SZ,600000.SH",
               "indicators":
                   "open,high,low,close",
               "startdate":
                   "2021-07-05",
               "enddate":
                   "2022-07-05",
               "functionpara":
                   {"Fill": "Blank"}
               }
    thsResponse = requests.post(url=thsUrl, json=thsPara, headers=thsHeaders)
    print(thsResponse.content)


# 基础数据：获取证券基本信息、财务指标、盈利预测、日频行情等数据
def basic_data():
    thsUrl = 'https://quantapi.51ifind.com/api/v1/basic_data_service'
    thsPara = {"codes":
                   "300033.SZ,600000.SH",
               "indipara":
                   [
                       {
                           "indicator":
                               "ths_regular_report_actual_dd_stock",
                           "indiparams":
                               ["104"]
                       },
                       {
                           "indicator":
                               "ths_total_shares_stock",
                           "indiparams":
                               ["20220705"]
                       }
                   ]
               }
    thsResponse = requests.post(url=thsUrl, json=thsPara, headers=thsHeaders)
    print(thsResponse.content)


# 日期序列：与基础数据指标相同，可以同时获取多日数据
def date_serial():
    thsUrl = 'https://quantapi.51ifind.com/api/v1/date_sequence'
    thsPara = {"codes":
                   "000001.SZ,600000.SH",
               "startdate":
                   "20220605",
               "enddate":
                   "20220705",
               "functionpara":
                   {"Fill": "Blank"},
               "indipara":
                   [
                       {
                           "indicator":
                               "ths_close_price_stock",
                           "indiparams":
                               ["", "100", ""]
                       },
                       {"indicator":
                            "ths_total_shares_stock",
                        "indiparams":
                            [""]
                        }
                   ]
               }
    thsResponse = requests.post(url=thsUrl, json=thsPara, headers=thsHeaders)
    data = json.loads(thsResponse.content)
    result = Trans2df(data)
    print(result)


# json结构体转dataframe
def Trans2df(data):
    df = pd.json_normalize(data['tables'])
    df2 = df.set_index(['thscode'])

    unnested_lst = []
    for col in df2.columns:
        unnested_lst.append(df2[col].apply(pd.Series).stack())

    result = pd.concat(unnested_lst, axis=1, keys=df2.columns)
    # result = result.reset_index(drop=True)
    # 设置二级索引
    result = result.reset_index()
    result = result.set_index(['thscode', 'time'])
    # 格式化,行转列
    result = result.drop(columns=['level_1'])
    result = result.reset_index()
    return (result)


# 专题报表，示例提取全部A股代码，更多报表数据使用超级命令工具查看
def data_pool():
    thsUrl = 'https://quantapi.51ifind.com/api/v1/data_pool'
    thsPara = {
        "reportname": "p03425",
        "functionpara": {
            "date": "20220706",
            "blockname": "001005010",
            "iv_type": "allcontract"
        },
        "outputpara": "p03291_f001,p03291_f002,p03291_f003,p03291_f004"
    }
    thsResponse = requests.post(url=thsUrl, json=thsPara, headers=thsHeaders)
    print(thsResponse.content)


# 经济数据库
def edb():
    thsUrl = 'https://quantapi.51ifind.com/api/v1/edb_service'
    thsPara = {"indicators":
                   "G009035746",
               "startdate":
                   "2022-04-01",
               "enddate":
                   "2022-05-01"}
    thsResponse = requests.post(url=thsUrl, json=thsPara, headers=thsHeaders)
    print(thsResponse.content)


# 日内快照：tick数据
def snap_shot():
    thsUrl = 'https://quantapi.51ifind.com/api/v1/snap_shot'
    thsPara = {
        "codes": "000001.SZ",
        "indicators": "open,high,low,latest,bid1,ask1,bidSize1,askSize1",
        "starttime": "2022-07-06 09:15:00",
        "endtime": "2022-07-06 15:15:00"
    }
    thsResponse = requests.post(url=thsUrl, json=thsPara, headers=thsHeaders)
    print(thsResponse.content)


# 公告函数
def report_query():
    thsUrl = 'https://quantapi.51ifind.com/api/v1/report_query'
    thsPara = {
        "codes": "000001.SZ,600000.SH",
        "functionpara": {
            "reportType": "901"
        },
        "beginrDate": "2021-01-01",
        "endrDate": "2022-07-06",
        "outputpara": "reportDate:Y,thscode:Y,secName:Y,ctime:Y,reportTitle:Y,pdfURL:Y,seq:Y"
    }
    thsResponse = requests.post(url=thsUrl, json=thsPara, headers=thsHeaders)
    print(thsResponse.content)


# 智能选股
def WCQuery():
    thsUrl = 'https://quantapi.51ifind.com/api/v1/smart_stock_picking'
    thsPara = {
        "searchstring": "涨跌幅",
        "searchtype": "stock"
    }
    thsResponse = requests.post(url=thsUrl, json=thsPara, headers=thsHeaders)
    print(thsResponse.content)


# 日期查询函数、日期偏移函数：根据交易所查询交易日
def date_offset():
    thsUrl = 'https://quantapi.51ifind.com/api/v1/get_trade_dates'
    thsPara = {"marketcode": "212001",
               "functionpara":
                   {"dateType": "0",
                    "period": "D",
                    "offset": "-10",
                    "dateFormat": "0",
                    "output": "sequencedate"},
               "startdate":
                   "2022-07-05"}
    thsResponse = requests.post(url=thsUrl, json=thsPara, headers=thsHeaders)
    print(thsResponse.content)


def main():
    # 实时行情
    real_time()
    # 基础数据
    # basic_data()
    # 日期序列
    # date_serial()
    # 专题报表
    # data_pool()
    # 历史行情
    # history_quotes()
    # 高频序列
    # high_frequency()
    # 经济数据库
    # edb()
    # 日内快照
    # snap_shot()
    # 公告函数
    # report_query()
    # 智能选股
    # WCQuery()
    # 日期查询函数
    # date_query()
    # 日期偏移函数
    # date_offset()


if __name__ == '__main__':
    main()

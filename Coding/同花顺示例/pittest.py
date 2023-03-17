from iFinDPy import *
import pandas as pd

pd.options.display.max_columns = None
pd.set_option('display.float_format', lambda x: '%.4f' % x)


loginResult = THS_iFinDLogin('zhanghao','mima')
print(loginResult)

def historyReportDateTest():
    # 提取股票不同日期的财报数据，避免回测财务模型受未来数据干扰
    dateList = THS_DateQuery('SSE','dateType:0,period:D,dateFormat:0','2019-10-20','2019-10-30')['tables']['time']
    for date in dateList:
        result = THS_BD('300029.SZ', 'ths_np_atoopc_pit_stock', '{},20190930,1'.format(date))
        print(date,result.data)

    # 使用日期序列函数来实现同样效果
    result = THS_DS('300029.SZ', 'ths_np_atoopc_pit_stock', '20190930,1', 'Fill:Blank', '2019-10-20', '2019-10-30')
    print(result.data)

def reportChange():
    # 使用财报变更日期指标和自定义日期序列函数提取股票的财报变更记录
    result = THS_BD('000892.SZ', 'ths_report_changedate_pit_stock', '2018-12-31,2020-11-25,604,1,20171231')
    changeDateList = result.data.iloc[0]['ths_report_changedate_pit_stock']
    print(changeDateList)

    changeRecord = THS_DS('000892.SZ', 'ths_total_assets_pit_stock', '20181231,1', 'date_sequence:{}'.format(changeDateList), '', '').data
    print(changeRecord)

def calepsttm(x):
    curDate = x['time']
    reportDateNow = x['ths_history_reportdate_pit_stock']
    year = int(reportDateNow[:4])
    datestr = reportDateNow[-4:]
    reportDateLast12 = str(year-1)+'1231'
    reportDateLastEnd = str(year-1)+datestr
    if datestr == '1231':
        np_ttm = THS_BD('300029.SZ','ths_np_atoopc_pit_stock','{},{},1'.format(curDate,reportDateNow)).data.iloc[0]['ths_np_atoopc_pit_stock']
    else:
        npThisYear = THS_BD('300029.SZ','ths_np_atoopc_pit_stock','{},{},1'.format(curDate,reportDateNow)).data.iloc[0]['ths_np_atoopc_pit_stock']
        npLastYear1 = THS_BD('300029.SZ', 'ths_np_atoopc_pit_stock', '{},{},1'.format(curDate, reportDateLast12)).data.iloc[0]['ths_np_atoopc_pit_stock']
        npLastYear2 = THS_BD('300029.SZ', 'ths_np_atoopc_pit_stock', '{},{},1'.format(curDate, reportDateLastEnd)).data.iloc[0]['ths_np_atoopc_pit_stock']
        np_ttm = npThisYear + npLastYear1 - npLastYear2
    shareNum = THS_BD('300029.SZ','ths_total_shares_stock',curDate).data.iloc[0]['ths_total_shares_stock']
    epsttm = np_ttm/shareNum
    return epsttm


def epsttm():
    # 当前ttm的提取
    result_before = THS_DS('300029.SZ', 'ths_eps_ttm_stock', '101', 'Fill:Blank', '2019-10-20', '2019-10-30')
    if result_before.errorcode != 0:
        print('error {} happen'.format(result_before.errmsg))
    else:
        print(result_before.data)
    # 使用新的时点数据自行计算ttm
    result_after = THS_DS('300029.SZ','ths_history_reportdate_pit_stock','608,1,0@104,2','Fill:Blank','2019-10-20','2019-10-30')
    if result_after.errorcode != 0:
        print('error {} happen'.format(result_after.errmsg))
    else:
        result_df = result_after.data
        result_df['epsttm'] = result_df.apply(calepsttm,axis=1)
        print(result_df)

def exceed100test():
    dateList = THS_DateQuery('SSE', 'dateType:0,period:D,dateFormat:0', '2018-10-20', '2019-10-30')['tables']['time']
    changeRecord = THS_DS('000892.SZ', 'ths_np_atoopc_pit_stock', '20171231,1',
                          'date_sequence:{}'.format(','.join(dateList)), '', '')
    print(changeRecord)

def duplicatedatetest():
    # 自定义序列函数支持不同的日期格式
    changeRecord = THS_DS('000892.SZ', 'ths_np_atoopc_pit_stock', '20171231,1',
                          'date_sequence:2018-05-01,20200601,2020-08-01', '', '')
    print(changeRecord)

def main():
    historyReportDateTest()
    # reportChange()
    # epsttm()
    # exceed100test()
    # duplicatedatetest()

if __name__ == '__main__':
    main()
## datetime库

'''
`strftime`方法可以将datetime格式化为字符串：

```python
In [108]: dt.strftime('%m/%d/%Y %H:%M')
Out[108]: '10/29/2011 20:30'
```

`strptime`可以将字符串转换成 `datetime`对象：

```python
In [109]: datetime.strptime('20091031', '%Y%m%d')
Out[109]: datetime.datetime(2009, 10, 31, 0, 0)
```

表2-5列出了所有的格式化命令。

![<span class=](http://upload-images.jianshu.io/upload_images/7178691-100f9a20c1536553.png?imageMogr2/auto-orient/strip|imageView2/2/w/1240)
'''

## pandas date
# 转格式
import pandas as pd
pd.to_datetime()
# 加一天并只显示日期
data['加一天'] = data['时间'].dt.date+pd.to_timedelta(1, unit='D')
# 加一小时
data['加一小时'] = data['时间']+pd.to_timedelta(1, unit='h')

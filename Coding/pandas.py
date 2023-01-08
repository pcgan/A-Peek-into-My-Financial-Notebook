## pandas 数据分析

## 路径变量
import os
os.getcwd()
os.chdir('C:\\Users\\h\\Desktop')
os.listdir()

## 读写存
import pandas as pd
import  numpy as np
### 读excel
df0=pd.read_csv('delivery.csv',index_col=False)
df0.head(3)
'''
读取常见问题：
1.千分位分隔符，导致无法转float  
'''


### 创建pd对象
s = pd.Series([1,3,5,np.nan,6,8])
dates = pd.date_range('20130101', periods=6)
df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
df2 = pd.DataFrame({ 'A' : 1.,
                     'B' : pd.Timestamp('20130102'),
                     'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
                     'D' : np.array([3] * 4,dtype='int32'),
                     'E' : pd.Categorical(["test","train","test","train"]),
                     'F' : 'foo' })
## 列数字格式
# style格式化
# 用字典对指定列进行格式化
df.style.format({'B': "{:0<4.0f}", 'D': '{:+.2f}'})

# map\apply结合format格式化
#对'A'列进行设置
df['A']=df_decimal['A'].map(lambda x:('%.2f')%x)
df_result['同批号库存余量'].map(lambda x:format(x,'.2f'))
#所有数字保留两位小数
df=df_decimal.applymap(lambda x:('%.2f')%x)



## 增删改查

### 排序
dates.sort_values(ascending=True)
df0.sort_values(by=['amount','date'],ascending=[True,False],inplace=False,na_position='first')
df0.sort_index(axis=1,inplace=True)

### 筛选
#### 直接条件筛选
df0['date'] = pd.to_datetime(df0['date'])
df0.dtypes
#### 日期筛选
df0[(df0['amount']<df0['amount'].mean()) & (df0['date']==pd.Timestamp('2019/1/9'))].head(2)
#### 切片loc/iloc
df0.loc[(df0['amount'].isin([100,-100])),['price']]=5
df0.loc[[1,2],['price']]
df0.iloc[[1,2],[1,2,3]]

### 删除
df0.drop(labels=None,axis=0, index=None, columns=None, inplace=False)

df = pd.DataFrame({'a': ['a0', 'a1', 'a2'],
        'b': ['b0', 'b1', 'b2'],
        'c': ['c0', 'c1', 'c2']})
# 删除第一行
df_1 = df.drop(axis=0,index=0)
# 删除第一列和第二列
df_2 = df.drop(axis=1,columns=['a','b'])
# 删除指定值
df0.drop(index = df0[(df0.ZH_Term_len == 0)].index.tolist()) #事后要reset.index

## 修改列名
data.columns = ['city','name','post','pay','request','number']
data.rename(columns={'城市': 'city','公司名称': 'name'}, inplace=True)

## 拼接与关联

## concat 数据拼接
pd.concat(
    objs: 'Iterable[NDFrame] | Mapping[Hashable, NDFrame]',
    axis=0,
    join='outer',
    ignore_index: 'bool' = False,
    keys=None,
    levels=None,
    names=None,
    verify_integrity: 'bool' = False,
    sort: 'bool' = False,
    copy: 'bool' = True,
) -> 'FrameOrSeriesUnion'

## merge 数据关联与SQL中的join基本一样

pd.merge(
    left: 'DataFrame | Series',
    right: 'DataFrame | Series',
    how: 'str' = 'inner',
    on: 'IndexLabel | None' = None,
    left_on: 'IndexLabel | None' = None,
    right_on: 'IndexLabel | None' = None,
    left_index: 'bool' = False,
    right_index: 'bool' = False,
    sort: 'bool' = False,
    suffixes: 'Suffixes' = ('_x', '_y'),
    copy: 'bool' = True,
    indicator: 'bool' = False,
    validate: 'str | None' = None,
) -> 'DataFrame'


#5 应用公式
# map
df0['amount'].map({100:1,-100:2})
def to_zero(x):
    return 1 if x>100 else 0

df0['amount'].map(to_zero)

# lambda
df0['price'].map(lambda x: 1 if x>5 else 0)

# apply

df0[['amount','price']].apply(np.sum,axis=0)
def zj(series):
    m=series['amount']
    p=series['price']
    zj=m*p
    return zj
df0[['amount','price']].apply(zj,axis=1)


# applymap


#6 数据透视表


#7 作图




#8 应用模型

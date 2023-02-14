# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 11:28:42 2023

@author: He Pengfei
"""
import datetime
import os
import math

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
from numpy.linalg import inv
from pypfopt import black_litterman, expected_returns
from pypfopt import risk_models as riskmodels
from pypfopt.black_litterman import BlackLittermanModel
from pypfopt.efficient_frontier import EfficientFrontier
from scipy.optimize import minimize

#%matplotlib inline
#editorTextFocus && !findInputFocussed && !jupyter.ownsSelection && !notebookEditorFocused && !replaceInputFocussed && editorLangId == 'python'

os.chdir(r'D:\个人笔记\Coding\数据与代码')
os.getcwd()


''' 导入并初始化数据 '''

# 资产收益率数据导入
np.set_printoptions(suppress=True)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

asset_returns_orig = pd.read_excel('assetpricedata.xlsx', sheet_name = "Status", index_col=0, parse_dates=True)
asset_returns_orig.head(10)
asset_returns_orig.describe()

# 数据处理
cols = ['Stock_Growth', 'Stock_Value', 'ConvertableBond', 'Bond', 'GovBond10Y']
asset_returns = asset_returns_orig[cols[:-1]].astype(float).dropna()
asset_returns.tail(10)
asset_returns_mean = asset_returns.mean()

asset_returns['dt']=pd.date_range('20050601','20221231',freq='1M').strftime('%Y%m')
asset_returns.head(10)

#资产收益率走势图
fig,ax=plt.subplots(1,1)
pd.options.display.notebook_repr_html=False  # 表格显示
plt.rcParams['figure.dpi'] = 75  # 图形分辨率
tick_spacing = 10
ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

                                   
#sns.set_theme(style='darkgrid')  # 图形主题
#sns.lineplot(data=asset_returns,x=asset_returns['dt'],y=asset_returns[['Stock_Growth', 'Stock_Value', 'ConvertableBond', 'Bond']])
#plt.show()
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']    # 指定默认字体：解决plot不能显示中文问题
mpl.rcParams['axes.unicode_minus'] = False               # 解决保存图像是负号'-'显示为方块的问题

plt.plot(asset_returns['dt'],asset_returns[['Stock_Growth', 'Stock_Value', 'ConvertableBond', 'Bond']])
plt.xlabel('时间',fontsize=12)
plt.xticks(rotation=90,fontsize=8)
plt.legend(['Stock_Growth', 'Stock_Value', 'ConvertableBond', 'Bond'])
plt.show()
#(asset_returns/asset_returns.iloc[0]*100).plot(figsize=(8,5))

riskfree_rate = asset_returns_orig['GovBond10Y']
riskfree_rate.head(10)


# 计算资产收益率协方差矩阵和相关系数矩阵
asset_returns_cov = asset_returns.cov()
asset_returns_corr = asset_returns.corr()
asset_returns_cov
asset_returns_corr

# 计算超额收益
excess_asset_returns = asset_returns.subtract(riskfree_rate, axis=0)
excess_asset_returns_mean = excess_asset_returns.mean()
excess_asset_returns_mean
excess_asset_returns_cov = excess_asset_returns.cov()
excess_asset_returns_corr = excess_asset_returns.corr()
excess_asset_returns_cov
excess_asset_returns_corr

# 导入资产权重数据
asset_weights = pd.read_excel('marketweights.xlsx', sheet_name = "marketweights", index_col='asset_class')
asset_weights

''' 马科维茨优化模型'''

# 计算资产组合收益率
def port_mean(W, R):
    return sum(R * W)

# 计算收益率方差
def port_var(W, C):
    return np.dot(np.dot(W, C), W)

# 结合收益率及方差
def port_mean_var(W, R, C):
    return port_mean(W, R), port_var(W, C)

# 优化求权重
def solve_weights_MaxSharp_NoShort(R, C, rf):
    def fitness(W, R, C, rf):
        mean, var = port_mean_var(W, R, C)
        util = (mean - rf) / np.sqrt(var)  # 最大化夏普比例
        if util < 0:
            utiltest = 0.01
        else:
            utiltest = util
        return 1 / utiltest
    n = len(R)
    W = np.ones([n]) / n
    b_ = [(0., 1.) for i in range(n)]
    c_ = ({'type': 'eq', 'fun': lambda W: sum(W) - 1.})
    optimized = minimize(fitness, W, (R, C, rf), method='SLSQP', constraints=c_, bounds=b_)
    return optimized.x , port_mean_var(optimized.x, R, C)

def solve_weights_MinVariance_NoShort(R, C, rf):
    def fitness(W, R, C, rf):
        mean, var = port_mean_var(W, R, C)
        util = np.sqrt(var)  # 最小化方差
        return util
    n = len(R)
    W = np.ones([n]) / n
    b_ = [(0., 1.) for i in range(n)]
    c_ = ({'type': 'eq', 'fun': lambda W: sum(W) - 1.})
    optimized = minimize(fitness, W, (R, C, rf), method='SLSQP', constraints=c_, bounds=b_)
    return optimized.x, port_mean_var(optimized.x, R, C)

def solve_weights_MaxSharp_NoBound(R, C, rf):
    def fitness(W, R, C, rf):
        mean, var = port_mean_var(W, R, C)
        util = (mean - rf) / np.sqrt(var)  # 最大化夏普比例
        if util <= 0:
            utiltest = 0.001
        else:
            utiltest = util
        return 1 / utiltest
    n = len(R)
    W = np.ones([n]) / n
    b_ = [(-1., 2.) for i in range(n)]
    c_ = ({'type': 'eq', 'fun': lambda W: sum(W) - 1.})
    optimized = minimize(fitness, W, (R, C, rf), method='SLSQP', constraints=c_, bounds=b_)
    return optimized.x , port_mean_var(optimized.x, R, C)

def solve_weights_MinVariance_NoBound(R, C, rf):
    def fitness(W, R, C, rf):
        mean, var = port_mean_var(W, R, C)
        util = np.sqrt(var)  # 最小化方差
        return util
    n = len(R)
    W = np.ones([n]) / n
    b_ = [(-1., 2.) for i in range(n)]
    c_ = ({'type': 'eq', 'fun': lambda W: sum(W) - 1.})
    optimized = minimize(fitness, W, (R, C, rf), method='SLSQP', constraints=c_, bounds=b_)
    return optimized.x, port_mean_var(optimized.x, R, C)


''' 马科维茨配置优化'''

# 最大sharp配置，分别考虑有约束和无约束情况

solve_weights_MaxSharp_NoShort(asset_returns_mean, asset_returns_cov, 0.029)
solve_weights_MaxSharp_NoShort(excess_asset_returns_mean, excess_asset_returns_cov, 0)

solve_weights_MaxSharp_NoBound(asset_returns_mean, asset_returns_cov, 0)
solve_weights_MaxSharp_NoBound(excess_asset_returns_mean, excess_asset_returns_cov, 0)

#最小方差配置，分别考虑有约束和无约束情况

solve_weights_MinVariance_NoShort(asset_returns_mean, asset_returns_cov, 0.029)
solve_weights_MinVariance_NoShort(excess_asset_returns_mean, excess_asset_returns_cov, 0)

solve_weights_MinVariance_NoBound(asset_returns_mean, asset_returns_cov, 0)
solve_weights_MinVariance_NoBound(excess_asset_returns_mean, excess_asset_returns_cov, 0)

# 使用简便公式进行验证
inverse_asset_returns_cov = pd.DataFrame(inv(asset_returns_cov.values), index=asset_returns_cov.columns, columns=asset_returns_cov.index)
MV_weights_vector = inverse_asset_returns_cov.dot(asset_returns_mean)
MV_weights_vector = MV_weights_vector/sum(MV_weights_vector)
MV_weights_vector

port_mean_var(MV_weights_vector, asset_returns_mean, asset_returns_cov)

inverse_excess_asset_returns_cov = pd.DataFrame(inv(excess_asset_returns_cov.values), index=excess_asset_returns_cov.columns, columns= excess_asset_returns_cov.index)
excess_MV_weights_vector = inverse_excess_asset_returns_cov.dot(excess_asset_returns_mean)
excess_MV_weights_vector = excess_MV_weights_vector/sum(excess_MV_weights_vector)
excess_MV_weights_vector


'''计算市场均衡隐含收益率'''

global_return = excess_asset_returns.mean().multiply(asset_weights['MarketWeights'].values).sum()
market_var = np.matmul(asset_weights.values.reshape(len(asset_weights)).T,
                                       np.matmul(excess_asset_returns_cov.values, asset_weights.values.reshape(len(asset_weights))))
print(f'The global market mean return is {global_return:.4f} and the variance is {market_var:.6}')
risk_aversion = global_return / market_var
marketsharp = global_return / math.sqrt(market_var)
risk_aversion
marketsharp

def implied_rets(risk_aversion, sigma, w):
    
    implied_rets = risk_aversion * sigma.dot(w).squeeze()
    
    return implied_rets

excess_asset_returns_cov
implied_equilibrium_returns = implied_rets(risk_aversion, excess_asset_returns_cov, asset_weights)
implied_equilibrium_returns

# 隐含收益率验证

np.dot(np.dot(0.38, excess_asset_returns_cov), asset_weights)

# 计算隐含收益率均值的协方差矩阵

tau = 0.01
implied_equilibrium_returns_cov = tau * excess_asset_returns_cov  
implied_equilibrium_returns_cov


''' 观点矩阵及后验收益率计算'''

Q = np.array([0.0772, 0.0771, 0.0789, 0.0719])

P = [
     [1, 0, 0, 0,],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
    ]

P = np.array(P)

view1_var = np.matmul(P[0].reshape(len(P[0])),np.matmul(excess_asset_returns_cov.values, P[0].reshape(len(P[0])).T))
view2_var = np.matmul(P[1].reshape(len(P[1])),np.matmul(excess_asset_returns_cov.values, P[1].reshape(len(P[1])).T))
view3_var = np.matmul(P[2].reshape(len(P[2])),np.matmul(excess_asset_returns_cov.values, P[2].reshape(len(P[2])).T))
view4_var = np.matmul(P[3].reshape(len(P[3])),np.matmul(excess_asset_returns_cov.values, P[3].reshape(len(P[3])).T))


print(f'The Variance of View 1 Portfolio is {view1_var}, and the standard deviation is {np.sqrt(view1_var):.3f}\n',\
      f'The Variance of View 2 Portfolio is {view2_var}, and the standard deviation is {np.sqrt(view2_var):.3f}\n',\
       f'The Variance of View 3 Portfolio is {view3_var}, and the standard deviation is {np.sqrt(view3_var):.3f}\n',\
            f'The Variance of View 4 Portfolio is {view4_var}, and the standard deviation is {np.sqrt(view4_var):.3f}\n')

def error_cov_matrix(sigma, tau, P):
    matrix = np.diag(np.diag(P.dot(tau * excess_asset_returns_cov).dot(P.T)))
    return matrix

omega = error_cov_matrix(excess_asset_returns_cov, tau, P)
omega    

# 计算后验收益率
sigma_scaled = excess_asset_returns_cov * tau
BL_return_vector = implied_equilibrium_returns + sigma_scaled.dot(P.T).dot(inv(P.dot(sigma_scaled).dot(P.T) + omega).dot(Q - P.dot(implied_equilibrium_returns)))    
BL_return_vector    

# 计算后验收益率（第二种写法)
sub_a = np.linalg.inv(np.dot(tau, excess_asset_returns_cov))
sub_b = np.dot(np.dot(np.transpose(P), np.linalg.inv(omega)), P)
sub_c = np.dot(np.linalg.inv(np.dot(tau, excess_asset_returns_cov)), implied_equilibrium_returns)
sub_d = np.dot(np.dot(np.transpose(P), np.linalg.inv(omega)), Q)
    
Er_pos = np.dot(np.linalg.inv(sub_a + sub_b), (sub_c + sub_d))
Er_pos

# 市场隐含收益率和后验收益率比较   
returns_table = pd.concat([implied_equilibrium_returns, BL_return_vector], axis=1) 
returns_table.columns = ['Implied Returns', 'BL Return Vector']
returns_table['Difference'] = returns_table['BL Return Vector'] - returns_table['Implied Returns']
returns_table.style.format('{:,.2f}%')    
returns_table     

''' 后验收益率协方差矩阵计算'''

excess_asset_returns_meanCov = np.linalg.inv(sub_a + sub_b)
BL_return_cov = excess_asset_returns_cov + excess_asset_returns_meanCov 

excess_asset_returns_cov
excess_asset_returns_meanCov
BL_return_cov

''' 资产配置计算及比较'''
    
solve_weights_MaxSharp_NoShort(BL_return_vector, BL_return_cov, 0)
solve_weights_MinVariance_NoShort(BL_return_vector, BL_return_cov, 0)


inverse_cov = pd.DataFrame(inv(BL_return_cov.values), index=BL_return_cov.columns, columns=BL_return_cov.index)
BL_weights_vector = inverse_cov.dot(BL_return_vector)
BL_weights_vector = BL_weights_vector/sum(BL_weights_vector)    
BL_weights_vector    


MV_weights_vector = inverse_cov.dot(excess_asset_returns.mean())
MV_weights_vector = MV_weights_vector/sum(MV_weights_vector)
MV_weights_vector

weights_table = pd.concat([BL_weights_vector, asset_weights, MV_weights_vector], axis=1)
weights_table.columns = ['BL Weights', 'Market Cap Weights', 'Mean-Var Weights']
weights_table['BL/Mkt Cap Diff'] = weights_table['BL Weights'] - weights_table['Market Cap Weights']
weights_table.style.format('{:,.2f}%')    
    
print(weights_table)    
    
    
'''显示结果'''

import matplotlib.pyplot as plt

N = BL_weights_vector.shape[0]
fig, ax = plt.subplots(figsize=(15, 7))
ax.set_title('Black-Litterman Model Portfolio Weights Recommendation vs the Market Portfolio vs Mean-Variance Weights')
ax.plot(np.arange(N)+1, MV_weights_vector, '^', c='b', label='Mean-Variance)')
ax.plot(np.arange(N)+1, asset_weights, 'o', c='g', label='Market Portfolio)')
ax.plot(np.arange(N)+1, BL_weights_vector, '*', c='r',markersize=10, label='Black-Litterman')
ax.vlines(np.arange(N)+1, 0, BL_weights_vector, lw=1)
ax.vlines(np.arange(N)+1, 0, MV_weights_vector, lw=1)
ax.vlines(np.arange(N)+1, 0, asset_weights, lw=1)
ax.axhline(0, c='m')
ax.axhline(-1, c='m', ls='--')
ax.axhline(1, c='m', ls='--')
ax.set_xlabel('Assets')
ax.set_xlabel('Portfolio Weighting')
ax.xaxis.set_ticks(np.arange(1, N+1, 1))
ax.set_xticklabels(asset_weights.index.values)
plt.xticks(rotation=90, )
plt.legend(numpoints=1, fontsize=11)
plt.show()    
    
    

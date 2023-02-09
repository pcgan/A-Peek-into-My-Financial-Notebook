library(timeSeries)
library(tseries)
library(vars)
library(car)
library(lmtest)
library(urca)
library(readxl)
library(ggplot2)
library(pastecs)
library(ggfortify)
library(scales)
library(reshape2)
library(psych)
library(mFilter)
library(rJava)
library(xlsxjars)
library(xlsx)
library(rstatix)

# Set working directory
getwd()
setwd("D:/个人笔记/Coding/数据与代码")
getwd()

### HP analysis of M2
M2 = read_xlsx("MonetaryCreditandAssets.xlsx", sheet = "M2_YoY")
attach(M2)
summary(M2)

describe(M2_YoY)

OneFactorTSDrawing_M05(M2_YoY)

M2_YoY_TS = ts(M2_YoY, start=c(2005, 6), frequency=12)
M2_YoY_TS_HPFilter = hpfilter(M2_YoY_TS,freq=14400,type=c("lambda","frequency"),drift=FALSE)

plot(M2_YoY_TS_HPFilter)

plot(M2_YoY_TS_HPFilter$cycle)

plot(M2_YoY_TS_HPFilter$trend)

describe(M2_YoY_TS_HPFilter$cycle)
describe(M2_YoY_TS_HPFilter$trend)

'''
write.xlsx(M2_YoY_TS_HPFilter$cycle, "D:/RWorking/Thesis/M2_YoY_TS_HPFilter_cycle.xlsx", sheetName="M2_YoY_TS_HPFilter_cycle", col.names=TRUE, row.names=TRUE, append=TRUE, showNA=TRUE)
write.xlsx(M2_YoY_TS_HPFilter$trend, "D:/RWorking/Thesis/M2_YoY_TS_HPFilter_trend.xlsx", sheetName="M2_YoY_TS_HPFilter_trend", col.names=TRUE, row.names=TRUE, append=TRUE, showNA=TRUE)
'''

### HP analysis of DR007
DR = read_xlsx("MonetaryCreditandAssets.xlsx", sheet = "DR007")
attach(DR)
summary(DR)

describe(DR007)

OneFactorTSDrawing_M05(DR007)

DR007_TS = ts(DR007, start=c(2014, 12), frequency=12)
DR007_TS_HPFilter = hpfilter(DR007_TS,freq=14400,type=c("lambda","frequency"),drift=FALSE)

plot(DR007_TS_HPFilter)

plot(DR007_TS_HPFilter$cycle)
plot(DR007_TS_HPFilter$trend)

describe(DR007_TS_HPFilter$cycle)
describe(DR007_TS_HPFilter$trend)

'''
write.xlsx(DR007_TS_HPFilter$cycle, "D:/RWorking/Thesis/DR007_HPFilter.xlsx", sheetName="DR007_cycle", col.names=TRUE, row.names=TRUE, append=TRUE, showNA=TRUE)
write.xlsx(DR007_TS_HPFilter$trend, "D:/RWorking/Thesis/DR007_HPFilter.xlsx", sheetName="DR007_trend", col.names=TRUE, row.names=TRUE, append=TRUE, showNA=TRUE)
'''

### HP analysis of Total Loan

Credit = read_xlsx("MonetaryCreditandAssets.xlsx", sheet = "Finance")
attach(Credit)
summary(Credit)



OneFactorTSDrawing_M05(TotalLoan)

TotalLoan_TS = ts(TotalLoan, start=c(2005, 6), frequency=12)
TotalLoan_TS_HPFilter = hpfilter(TotalLoan_TS,freq=14400,type=c("lambda","frequency"),drift=FALSE)

describe(TotalLoan)
describe(TotalLoan_TS_HPFilter$cycle)
describe(TotalLoan_TS_HPFilter$trend)

plot(TotalLoan_TS_HPFilter$cycle)
plot(TotalLoan_TS_HPFilter$trend)

write.xlsx(TotalLoan_TS_HPFilter$cycle, "D:/RWorking/Thesis/TotalLoan_HPFilter.xlsx", sheetName="TotalLoan_cycle", col.names=TRUE, row.names=TRUE, append=TRUE, showNA=TRUE)
write.xlsx(TotalLoan_TS_HPFilter$trend, "D:/RWorking/Thesis/TotalLoan_HPFilter.xlsx", sheetName="TotalLoan_trend", col.names=TRUE, row.names=TRUE, append=TRUE, showNA=TRUE)

### 所有期间收益率统计量
Asset_Price = read_xlsx("MonetaryCreditandAssets.xlsx", sheet = "Status")
attach(Asset_Price)
summary(Asset_Price)
describe(Asset_Price)
plot(Asset_Price$Stock_Growth)


Asset_Price_AllStatus = data.frame(Stock_Growth,Stock_Value,ConvertableBond,Bond, Commondity)
describe(Asset_Price_AllStatus)
cov(Asset_Price_AllStatus)
cor(Asset_Price_AllStatus)

### 各状态下收益率统计量
Asset_Price_SlackExpand_Load = read_xlsx("MonetaryCreditandAssets.xlsx", sheet = "SlackExpand")
Asset_Price_SlackExpand_Load = data.frame(Asset_Price_SlackExpand_Load)
Asset_Price_SlackExpand = Asset_Price_SlackExpand_Load[,-1]
describe(Asset_Price_SlackExpand)
cov(Asset_Price_SlackExpand)
cor(Asset_Price_SlackExpand)

Asset_Price_TightExpand_Load = read_xlsx("MonetaryCreditandAssets.xlsx", sheet = "TightExpand")
Asset_Price_TightExpand_Load = data.frame(Asset_Price_TightExpand_Load)
Asset_Price_TightExpand = Asset_Price_TightExpand_Load[,-1]
describe(Asset_Price_TightExpand)
cov(Asset_Price_TightExpand)
cor(Asset_Price_TightExpand)

Asset_Price_TightCrunch_Load = read_xlsx("MonetaryCreditandAssets.xlsx", sheet = "TightCrunch")
Asset_Price_TightCrunch_Load = data.frame(Asset_Price_TightCrunch_Load)
Asset_Price_TightCrunch = Asset_Price_TightCrunch_Load[,-1]
describe(Asset_Price_TightCrunch)
cov(Asset_Price_TightCrunch)
cor(Asset_Price_TightCrunch)

Asset_Price_SlackCrunch_Load = read_xlsx("MonetaryCreditandAssets.xlsx", sheet = "SlackCrunch")
Asset_Price_SlackCrunch_Load = data.frame(Asset_Price_SlackCrunch_Load)
Asset_Price_SlackCrunch = Asset_Price_SlackCrunch_Load[,-1]
describe(Asset_Price_SlackCrunch)
cov(Asset_Price_SlackCrunch)
cor(Asset_Price_SlackCrunch)


### 按状态划分的各状态下方差分析

### 成长股分类检验
Stock_Growth_Status = data.frame(Monetary_Credit_Status,Stock_Growth)
summary(Stock_Growth_Status)
boxplot(Stock_Growth ~ Monetary_Credit_Status, data = Stock_Growth_Status, col = "gold")
shapiro.test(Stock_Growth)
tapply(Stock_Growth_Status$Stock_Growth,Stock_Growth_Status$Monetary_Credit_Status,shapiro.test)
leveneTest(Stock_Growth ~ Monetary_Credit_Status, data = Stock_Growth_Status)
welch_anova_test(data = Stock_Growth_Status, Stock_Growth ~ Monetary_Credit_Status)
# games_howell_test (data = Stock_Growth_Status, Stock_Growth ~ Monetary_Credit_Status,conf.level = 0.95, detailed = FALSE)
kruskal.test(data = Stock_Growth_Status, Stock_Growth ~ Monetary_Credit_Status)

# 价值股分类检验
Stock_Value_Status = data.frame(Monetary_Credit_Status,Stock_Value)
summary(Stock_Value_Status)
boxplot(Stock_Value ~ Monetary_Credit_Status, data = Stock_Value_Status, col = "gold")
shapiro.test(Stock_Value)
tapply(Stock_Value_Status$Stock_Value,Stock_Value_Status$Monetary_Credit_Status,shapiro.test)
leveneTest(Stock_Value ~ Monetary_Credit_Status, data = Stock_Value_Status)
welch_anova_test(data = Stock_Value_Status, Stock_Value ~ Monetary_Credit_Status)
games_howell_test (data = Stock_Value_Status, Stock_Value ~ Monetary_Credit_Status,conf.level = 0.95, detailed = FALSE)
kruskal.test(data = Stock_Value_Status, Stock_Value ~ Monetary_Credit_Status)

# 可转债分类检验
ConvertableBond_Status = data.frame(Monetary_Credit_Status,ConvertableBond)
summary(ConvertableBond_Status)
boxplot(ConvertableBond ~ Monetary_Credit_Status, data = ConvertableBond_Status, col = "gold")
shapiro.test(ConvertableBond)
tapply(ConvertableBond_Status$ConvertableBond,ConvertableBond_Status$Monetary_Credit_Status,shapiro.test)
leveneTest(ConvertableBond ~ Monetary_Credit_Status, data = ConvertableBond_Status)
welch_anova_test(data = ConvertableBond_Status, ConvertableBond ~ Monetary_Credit_Status)
games_howell_test (data = ConvertableBond_Status, ConvertableBond ~ Monetary_Credit_Status,conf.level = 0.95, detailed = FALSE)
kruskal.test(data = ConvertableBond_Status, ConvertableBond ~ Monetary_Credit_Status)

# 债券分类检验
Bond_Status = data.frame(Monetary_Credit_Status,Bond)
summary(Bond_Status)
boxplot(Bond ~ Monetary_Credit_Status, data = Bond_Status, col = "gold")
shapiro.test(Bond)
tapply(Bond_Status$Bond,Bond_Status$Monetary_Credit_Status,shapiro.test)
leveneTest(Bond ~ Monetary_Credit_Status, data = Bond_Status)
welch_anova_test(data = Bond_Status, Bond ~ Monetary_Credit_Status)
games_howell_test (data = Bond_Status, Bond ~ Monetary_Credit_Status,conf.level = 0.95, detailed = FALSE)
kruskal.test(data = Bond_Status, Bond ~ Monetary_Credit_Status)

# 大宗商品分类检验
Commondity_Status = data.frame(Monetary_Credit_Status,Commondity)
summary(Commondity_Status)
boxplot(Commondity ~ Monetary_Credit_Status, data = Commondity_Status, col = "gold")
shapiro.test(Commondity)
tapply(Commondity_Status$Commondity,Commondity_Status$Monetary_Credit_Status,shapiro.test)
leveneTest(Commondity ~ Monetary_Credit_Status, data = Commondity_Status)
welch_anova_test(data = Commondity_Status, Commondity ~ Monetary_Credit_Status)
games_howell_test (data = Commondity_Status, Commondity ~ Monetary_Credit_Status,conf.level = 0.95, detailed = FALSE)
kruskal.test(data = Commondity_Status, Commondity ~ Monetary_Credit_Status)





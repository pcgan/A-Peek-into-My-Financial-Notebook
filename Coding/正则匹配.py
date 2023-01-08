# re.compile 预编译一个正则表达式


import re
 
s1 = 'num:12345678900,name:dgw,phone:19876543210,age:25'
s2 = 'num:12345678900,name:dgw,phone:119876543210,age:25'
 
 
ee = re.compile(r'1[3456789]\d{9}', re.S)
ff = ee.findall(s2)
print(ff)
 
gg = re.compile(r'(?<=\d)1[3456789]\d{9}', re.S) #限制了前一位非数字
hh = gg.findall(s2)

## re.search
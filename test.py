import pymannkendall as mk
import numpy as np
import csv
import scipy.stats as stats
# Generate some random data
x = np.random.rand(20)
print(x)
result = mk.original_test(x)
print(result)

# 读取data.csv文件
data = csv.reader(open('data.csv', encoding='utf-8'))
# 读取第二列文件
y = [float(row[0].split(':')[1]) for row in data]
# print(y)
# 相关性: 0.5481095181518209
# p: 0.00677475729826184
result2 = mk.original_test(y)
print(result2)
year = np.arange(2000,2023)
linear = stats.linregress(year,y)    # 线性回归
print(linear)
z = [0.1721, 0.1481, np.nan, 0.21630000000000002, 0.2005,
     0.2071, 0.1615, 0.1643, 0.1668, 0.1756, np.nan, 0.1975, 0.17200000000000001,
     0.16340000000000002, 0.2129, 0.16590000000000002, np.nan, 0.258, 0.2097, 0.2051,
     0.2223, 0.20900000000000002, 0.2232]
print(mk.original_test(z))
z = [1, 2, 3,]
print(mk.original_test(z))
print(np.count_nonzero(~np.isnan(z)))


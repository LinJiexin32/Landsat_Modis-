
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取csv文件
df = pd.read_csv('data.csv', encoding='gbk')
# 读取第一列数据
pixils = df.iloc[:, 0].values
# 读取第二列数据
year = df.iloc[:, 1].values


# 计算相关系数
print(np.corrcoef(pixils, year))

# 绘制散点图
plt.scatter(pixils, year)
plt.show()

#计算p值
from scipy import stats
print(stats.pearsonr(year, pixils))

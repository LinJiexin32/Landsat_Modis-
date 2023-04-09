
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
# 读取csv文件
df = pd.read_csv('data.csv', encoding='gbk')
# 读取第一列数据
pixels = df.iloc[:, 0].values
# 读取第二列数据
year = df.iloc[:, 1].values


# 计算相关系数
print("相关系数",np.corrcoef(pixels, year))


#计算p值
from scipy import stats
print(stats.pearsonr(year, pixels))


# 创建线性回归模型
model = LinearRegression()
model.fit(np.array(year).reshape(-1, 1), pixels)
slope = model.coef_
print(slope)


slope, intercept, r_value, p_value, std_err = stats.linregress(year, pixels)
print(slope)
print(p_value)
print(r_value)
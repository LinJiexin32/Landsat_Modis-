from osgeo import gdal
import numpy as np
from scipy.stats import pearsonr


# 读取data.csv文件
data = np.loadtxt('data.csv', delimiter=',', skiprows=0)
# 读取data.csv文件中的第一列数据
pixels = data[:, 0]
# 读取data.csv文件中的第二列数据
year = data[:, 1]
#计算year和pixels的相关系数和p值
corr, pvalue = pearsonr(year, pixels)
print(year)
print(pixels)
print('corr:',corr)
print('pvalue:',pvalue)


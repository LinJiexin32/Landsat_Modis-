from osgeo import gdal
import numpy as np
from scipy.stats import pearsonr
from scipy import stats

# 打开遥感影像文件
dataset = gdal.Open("./NDVI_Corr_P_Slope.tif")


# 读取图像大小
width = dataset.RasterXSize
height = dataset.RasterYSize
print('width:',width)
print('height:',height)
# 读取波段数
bands = dataset.RasterCount
print('bands:',bands)

# 读取遥感影像数据到 numpy 数组中
dataArray = dataset.ReadAsArray()

# 读取dataArray中元素的类型
print(dataArray.dtype)



x = 5
y = 6
# 读取x,y位置的像素值，前23波段为NDVI值，第24波段为相关系数，第25波段为p值,26波段为最小二乘斜率
ndvi = dataArray[0:23, y, x]
corr = dataArray[23, y, x]
pvalue = dataArray[24, y, x]
slope = dataArray[25, y, x]
print('ndvi:',ndvi)
print('corr:',corr)
print('pvalue:',pvalue)
print('slope',slope)

year = np.arange(2000, 2023)
year = [x for x, y in zip(year, ndvi) if not np.isnan(y)]
ndvi = [x for x in ndvi if not np.isnan(x)]
#计算year和ndvi的相关系数和p值,并和corr和pvalue进行比较
corr2, pvalue2 = pearsonr(year, ndvi)
print('corr2:',corr2)
print('pvalue2:',pvalue2)
slope2, intercept, r_value, p_value, std_err = stats.linregress(year, ndvi)

print('slope2:',slope2)


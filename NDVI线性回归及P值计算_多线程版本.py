from osgeo import gdal
import numpy as np
from scipy.stats import linregress
import time
import multiprocessing


# 计算程序运行时间
start = time.time()
# 输入遥感影像文件名
inputName = r"D:\Backup\Downloads\MODIS_00_22_ndvi_aggregated.tif"
# 输出遥感影像文件名
outputName = r"M_NDVI_Corr_P_Slope_fast.tif"
# 打开遥感影像文件
dataset = gdal.Open(inputName)

# 读取图像大小
width = dataset.RasterXSize
height = dataset.RasterYSize
print('width:', width)
print('height:', height)
# 读取波段数
bands = dataset.RasterCount
print('bands:', bands)
# 读取影像的地理信息和投影信息
proj = dataset.GetProjection()
trans = dataset.GetGeoTransform()


# 读取遥感影像数据到 numpy 数组中
dataArray = dataset.ReadAsArray()

# 读取dataArray中元素的类型
print(dataArray.dtype)

# 打印dataArray维度
print('shape:', dataArray.shape)
print('size:', dataArray.size)



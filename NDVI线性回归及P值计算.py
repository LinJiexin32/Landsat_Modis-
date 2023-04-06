from osgeo import gdal
import numpy as np
from scipy.stats import pearsonr
import time


#计算程序运行时间
start = time.time()

# 打开遥感影像文件
dataset = gdal.Open(r"E:\Landsat_Modis_NDVI_trend\Moids\V2\MODIS_00_22_ndvi_Partial_area.tif")

# 读取图像大小
width = dataset.RasterXSize
height = dataset.RasterYSize
print('width:',width)
print('height:',height)

# 读取遥感影像数据到 numpy 数组中
dataArray = dataset.ReadAsArray()

# 读取dataArray中元素的类型
print(dataArray.dtype)

# 打印dataArray维度
print('shape:',dataArray.shape)
print('size:',dataArray.size)
# 关闭数据集

# 读取影像的地理信息和投影信息
proj = dataset.GetProjection()
trans = dataset.GetGeoTransform()
del dataset




# 新影像的存储路径
corr_image_path = r"E:\Landsat_Modis_NDVI_trend\Moids\V2\MODIS_00_22_ndvi_corr_image.tif"
pvalue_image_path = r"E:\Landsat_Modis_NDVI_trend\Moids\V2\MODIS_00_22_ndvi_pvalue_image.tif"

# 创建新影像
driver = gdal.GetDriverByName('GTiff')
corr_image_dataset = driver.Create(corr_image_path, width, height, 1, gdal.GDT_Float64)
pvalue_image_dataset = driver.Create(pvalue_image_path, width, height, 1, gdal.GDT_Float64)

# 设置新影像的地理信息和投影信息
corr_image_dataset.SetProjection(proj)
corr_image_dataset.SetGeoTransform(trans)
pvalue_image_dataset.SetProjection(proj)
pvalue_image_dataset.SetGeoTransform(trans)

# 设置一个进度条
progress = gdal.TermProgress_nocb


# 计算相关系数和p值，并将结果写入新影像中
for i in range(height):
    for j in range(width):
        # 显示进度条
        progress((i * width + j) / (width * height))
        # 读取像元值
        pixel_values = dataArray[:, i, j]
        year = np.arange(2000,2023)
        # 如果在pixel_values中有nan值，那么year中对应位置的值也会被去除,同时去掉pixel_values中的nan值,保证
        year = [x for x, y in zip(year, pixel_values) if not np.isnan(y)]
        pixel_values = [x for x in pixel_values if not np.isnan(x)]

        # 如果pixel_values中元素的个数在3个以下，则将相关系数和p值都设置为nan
        if len(pixel_values) < 3:
            corr = np.array(np.nan).reshape(1, -1)
            pvalue = np.array(np.nan).reshape(1, -1)
        else:
            # 计算相关系数和p值
            corr, pvalue = pearsonr(year, pixel_values)
            # 将corr变为二维数组
            corr = np.array(corr).reshape(1, -1)
            pvalue = np.array(pvalue).reshape(1, -1)

        # 将结果写入新影像中
        corr_image_dataset.GetRasterBand(1).WriteArray(corr, j, i)
        pvalue_image_dataset.GetRasterBand(1).WriteArray(pvalue, j, i)

# 关闭数据集
del corr_image_dataset
del pvalue_image_dataset

end = time.time()
print("花了",(end - start)/60,"分钟")

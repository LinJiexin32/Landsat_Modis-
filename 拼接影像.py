#encoding=utf-8
import arcpy
from arcpy.sa import *

# 设置工作空间
arcpy.env.workspace = r"E:\Landsat_Modis_NDVI_trend\Moids\V2\clip_results"
outputFolder = r"E:\Landsat_Modis_NDVI_trend\Moids\V2"
# 获取所有.tif格式的子影像
rasters = arcpy.ListRasters("*", "tif")
print(rasters)
# 将子影像拼接成一张大影像
outRaster = arcpy.MosaicToNewRaster_management(rasters,outputFolder , pixel_type = "64_BIT",raster_dataset_name_with_extension= "mosaic2.tif", number_of_bands=3, )

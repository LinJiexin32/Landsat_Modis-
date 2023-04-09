from osgeo import gdal

# 打开遥感影像
dataset = gdal.Open(r"E:\Landsat_Modis_NDVI_trend\Slope\L_type.tif")
output_file = r'E:\Landsat_Modis_NDVI_trend\Moids\V2\clip'
# 获取遥感影像的宽度和高度
width = dataset.RasterXSize
height = dataset.RasterYSize

# 计算每个子块的宽度和高度
block_width = width // 2
block_height = height // 2

# 分割遥感影像为2x2的子块
for i in range(2):
    for j in range(2):
        # 计算子块的左上角坐标和右下角坐标
        ulx = i * block_width
        uly = j * block_height
        lrx = ulx + block_width
        lry = uly + block_height
        # 创建输出文件名
        dst_filename = output_file+'block_{}_{}.tif'.format(i, j)
        # 分割遥感影像
        gdal.Translate(dst_filename, dataset, srcWin=[ulx, uly, block_width, block_height])

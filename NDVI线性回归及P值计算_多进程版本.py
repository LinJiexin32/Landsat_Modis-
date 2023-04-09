from osgeo import gdal
import numpy as np
from scipy.stats import linregress
import time
import multiprocessing
import os

# 封装的函数
def linear_regression(inputName, outputName, progress_queue):
    # 打开遥感影像文件
    dataset = gdal.Open(inputName)

    # 读取图像大小
    width = dataset.RasterXSize
    height = dataset.RasterYSize
    # 读取波段数
    bands = dataset.RasterCount
    # 读取影像的地理信息和投影信息
    proj = dataset.GetProjection()
    trans = dataset.GetGeoTransform()
    # 读取遥感影像数据到 numpy 数组中
    dataArray = dataset.ReadAsArray()

    # 关闭数据集
    del dataset

    # 创建新影像
    driver = gdal.GetDriverByName('GTiff')
    # 创建一个新影像，1波段存相关系数，2存储P值，3存最小二乘斜率， 数据类型为Float64
    outRaster = driver.Create(outputName, width, height, 3, gdal.GDT_Float64)



    # 设置新影像的地理信息和投影信息
    outRaster.SetProjection(proj)
    outRaster.SetGeoTransform(trans)

    # 设置一个进度条
    progress = gdal.TermProgress_nocb

    # 计算相关系数和p值，并将结果写入新影像中
    for i in range(height):
        for j in range(width):
            # 显示进度条
            progress((i * width + j) / (width * height))
            # 读取像元值
            pixel_values = dataArray[:, i, j]
            year = np.arange(2000, 2023)
            # 如果在pixel_values中有nan值，那么year中对应位置的值也会被去除,同时去掉pixel_values中的nan值,保证二者长度相同
            year = [x for x, y in zip(year, pixel_values) if not np.isnan(y)]
            pixel_values = [x for x in pixel_values if not np.isnan(x)]

            # 如果pixel_values中元素的个数在3个以下，则将相关系数和p值都设置为nan
            if len(pixel_values) < 3:
                corr = np.array(np.nan).reshape(1, -1)
                pvalue = np.array(np.nan).reshape(1, -1)
                slope = np.array(np.nan).reshape(1, -1)
            else:
                # 计算相关系数和p值
                slope, intercept, corr, pvalue, std_err = linregress(year, pixel_values)
                # 将corr,pvalue,slope变为二维数组
                corr = np.array(corr).reshape(1, -1)
                pvalue = np.array(pvalue).reshape(1, -1)
                slope = np.array(slope).reshape(1, -1)

            # 将结果写入新影像中

            # 处理相关系数
            outRaster.GetRasterBand(1).WriteArray(corr, j, i)
            # 处理p值
            outRaster.GetRasterBand(2).WriteArray(pvalue, j, i)
            # 处理斜率
            outRaster.GetRasterBand(3).WriteArray(slope, j, i)

    # 关闭数据集
    del outRaster

    # 将进度条信息加入队列
    progress_queue.put(1)

# 多进程处理函数
def process_multiprocessing(inputFileList, outputFolder):
    # 创建进度条信息队列
    progress_queue = multiprocessing.Queue()
    # 开启多个进程，每个进程处理一个文件
    process_list = []
    for inputName in inputFileList:
        outputName = outputFolder + os.sep + os.path.splitext(os.path.basename(inputName))[0] + "_corr_pvalue_slope.tif"
        p = multiprocessing.Process(target=linear_regression, args=(inputName, outputName, progress_queue))
        p.start()
        process_list.append(p)
        print("Start process: " + str(p.pid))

    # 统计已完成的进程数量并显示进度条信息
    finished_process = 0
    total_process = len(process_list)
    while finished_process < total_process:
        # 从队列中取出一个元素
        item = progress_queue.get()
        if item == 1:
            # 更新完成的进程数目
            finished_process += 1
            # 打印当前的进度条信息
            progress = '{0:.2f}'.format(finished_process / total_process * 100)
            print("Progress: " + str(progress) + "%")

    # 关闭进程
    for p in process_list:
        p.join()

# 主程序
if __name__ == '__main__':
    # 计算程序运行时间
    start = time.time()
    # 输入遥感影像文件夹路径
    inputFolder = r"E:\Landsat_Modis_NDVI_trend\Moids\V2\clip"
    # 输出遥感影像文件夹路径
    outputFolder = r"E:\Landsat_Modis_NDVI_trend\Moids\V2\clip_results"

    # 获取文件夹中所有的.tif文件路径
    inputFileList = []
    for root, dirs, files in os.walk(inputFolder):
        for f in files:
            if f.endswith(".dat"):
            # if f.endswith(".tif"):
                inputFileList.append(os.path.join(root,f))

    # 创建输出文件夹
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    # 多进程处理
    process_multiprocessing(inputFileList, outputFolder)

    end = time.time()
    print("花了", (end - start) / 60, "分钟")

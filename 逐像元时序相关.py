from osgeo import gdal
import numpy as np
import time
import multiprocessing
import os
import pymannkendall as mk
from tqdm import tqdm
from scipy.stats import linregress
def err_call_back(err):
    print(f'出错啦~ error：{str(err)}')

# 封装的函数
def mk_test(inputName, outputName,results):
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
    # 创建一个新影像，1波段存 trend (increasing, decreasing or no trend):(1,-1,0)，
    # 2存储P值，3存sens斜率， 数据类型为Float64
    outRaster = driver.Create(outputName, width, height, 3, gdal.GDT_Float64)

    # 设置新影像的地理信息和投影信息
    outRaster.SetProjection(proj)
    outRaster.SetGeoTransform(trans)
    # 计算相关系数和p值，并将结果写入新影像中
    for i in tqdm(range(height), desc=inputName.split(os.sep)[-1],leave=False):
        for j in range(width):
            # 读取像元值
            pixel_values = dataArray[:, i, j]
            # 如果pixel_values中元素的非nan值在2个以下，则将trend_value\p值\sens slope都设置为nan
            if np.count_nonzero(~np.isnan(pixel_values)) < 2:
                trend_value = np.array(np.nan).reshape(1, -1)
                pvalue = np.array(np.nan).reshape(1, -1)
                slope = np.array(np.nan).reshape(1, -1)
            else:
                # 计算trend_value\p值\sens slope
                trend, h, pvalue, z, Tau, s, var_s, slope, intercept = mk.original_test(pixel_values)
                if trend == 'increasing':
                    trend_value = 1
                elif trend == 'decreasing':
                    trend_value = -1
                else:
                    trend_value = 0
                # 将trend_value\p值\sens slope变为二维数组
                trend_value = np.array(trend_value).reshape(1, -1)
                pvalue = np.array(pvalue).reshape(1, -1)
                slope = np.array(slope).reshape(1, -1)

            # 将结果写入新影像中

            # 处理trend_value
            outRaster.GetRasterBand(1).WriteArray(trend_value, j, i)
            # 处理p值
            outRaster.GetRasterBand(2).WriteArray(pvalue, j, i)
            # 处理斜率
            outRaster.GetRasterBand(3).WriteArray(slope, j, i)

    # 关闭数据集
    del outRaster
    tqdm.write(inputName + "处理完成")
    results.append(outputName)

def get_correlation(inputName1,inputName2, outputName):
    # 打开遥感影像文件
    print('inputName',inputName1)
    dataset1 = gdal.Open(inputName1)
    # 读取图像大小
    width1 = dataset1.RasterXSize
    height1 = dataset1.RasterYSize
    print('width,height',width1,height1)
    # 读取波段数
    bands = dataset1.RasterCount
    print('bands',bands)
    # 读取影像的地理信息和投影信息
    proj = dataset1.GetProjection()
    trans = dataset1.GetGeoTransform()
    # 读取遥感影像数据到 numpy 数组中
    dataArray1 = dataset1.ReadAsArray()
    print(dataArray1.shape)


    # 关闭数据集
    del dataset1
    # 打开遥感影像文件2
    print('inputName2',inputName2)
    dataset2 = gdal.Open(inputName2)
    # 读取图像大小
    width2 = dataset2.RasterXSize
    height2 = dataset2.RasterYSize
    print('width,height',width2,height2)
    # 读取遥感影像数据到 numpy 数组中
    dataArray2 = dataset2.ReadAsArray()
    print(dataArray2.shape)
    # 关闭数据集
    del dataset2
    width = min(width1,width2)
    height = min(height1,height2)
    # 创建新影像
    driver = gdal.GetDriverByName('GTiff')
    # 创建一个新影像，1波段存相关系数，2存储P值， 数据类型为Float32
    outRaster = driver.Create(outputName, width,height, 2, gdal.GDT_Float32)

    # 设置新影像的地理信息和投影信息
    outRaster.SetProjection(proj)
    outRaster.SetGeoTransform(trans)
    # 计算相关系数和p值，并将结果写入新影像中
    for i in tqdm(range(height)):
        for j in range(width):
            # 读取像元值
            ndvi1 = dataArray1[:, i, j]
            ndvi2 = dataArray2[:, i, j]

            # 如果非nan值在2个以下，则将结果的相关性和p值都设置为nan
            if np.count_nonzero(~np.isnan(ndvi1)) < 5 or np.count_nonzero(~np.isnan(ndvi2)) < 5:
                cor = np.array(np.nan).reshape(1, -1)
                pvalue = np.array(np.nan).reshape(1, -1)

            else:
                # 计算cor\p值\
                # print('ndvi1',ndvi1)
                # print('ndvi2',ndvi2)
                _, _, cor, pvalue, _ = linregress(ndvi1, ndvi2)
                cor = np.array(cor).reshape(1, -1)
                pvalue = np.array(pvalue).reshape(1, -1)
            # 将结果写入新影像中
            # 处理cor
            outRaster.GetRasterBand(1).WriteArray(cor, j, i)
            # 处理p值
            outRaster.GetRasterBand(2).WriteArray(pvalue, j, i)



# 多进程处理函数
def process_multiprocessing2(inputFileList, outputFolder):
    # 创建进程池
    pool = multiprocessing.Pool(processes=6)

    # 创建共享列表用于存储任务结果
    manager = multiprocessing.Manager()
    results = manager.list()

    # 使用tqdm包装共享列表，用于显示总体进度
    pbar = tqdm(total=len(inputFileList),desc='总体进度')

    def update(*a):
        pbar.update()

    for inputName in inputFileList:
        outputName = outputFolder + os.sep + os.path.splitext(os.path.basename(inputName))[0] + "_trend_pvalue_sens.tif"
        # 向进程池中添加要执行的任务
        # pool.apply_async(mk_test, args=(inputName, outputName, results), callback=update, error_callback=err_call_back)
        pool.apply_async(get_correlation, args=(inputName, outputName, results), callback=update, error_callback=err_call_back)
    # 先调用close关闭进程池，不能再有新任务被加入到进程池中
    pool.close()

    # 用join函数等待所有子进程结束
    pool.join()

    # 关闭tqdm进度条
    pbar.close()

    print('joined')

    return results



# 主程序
if __name__ == '__main__':
    # 计算程序运行时间
    start = time.time()
    inputfile1 = r"E:\NSW\ndvi\NSW_M_anMax_ndvi_0122-0000000000-0000000000.tif"
    inputfile2 = r"E:\NSW\ndvi\NSW_L_anMax_ndvi_0122_2.tif"
    outputfile = r"E:\NSW\cor_P.tif"
    get_correlation(inputfile1,inputfile2,outputfile)
    # # 输入遥感影像文件夹路径
    # inputFolder = r"E:\NSW\ndvi\ndvi"
    # # 输出遥感影像文件夹路径
    # outputFolder = r"E:\NSW\ndvi\ndvi"

    # 获取文件夹中所有的.tif文件路径
    # inputFileList = []
    # for root, dirs, files in os.walk(inputFolder):
    #     for f in files:
    #         if f.endswith(".dat") or f.endswith(".tif"):
    #             # if f.endswith(".tif"):
    #             get_correlation(os.path.join(root, f))
    #             # inputFileList.append(os.path.join(root, f))
    #
    # # 创建输出文件夹
    # if not os.path.exists(outputFolder):
    #     os.makedirs(outputFolder)
    #
    # # 多进程处理
    # process_multiprocessing2(inputFileList, outputFolder)

    end = time.time()
    print("花了", (end - start) / 60, "分钟")

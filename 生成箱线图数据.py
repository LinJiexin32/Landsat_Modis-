from osgeo import gdal
import numpy as np
import time
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt


# 封装的函数

def get_LaCov_Corela(inputName1, inputName2, outputName, LandcoverList):
    # 打开遥感影像文件
    print('inputName', inputName1)
    dataset1 = gdal.Open(inputName1)
    # 读取图像大小
    width1 = dataset1.RasterXSize
    height1 = dataset1.RasterYSize
    print('width,height', width1, height1)
    # 读取波段数
    bands = dataset1.RasterCount
    print('bands', bands)
    # 读取影像的地理信息和投影信息
    proj = dataset1.GetProjection()
    trans = dataset1.GetGeoTransform()
    # 读取遥感影像数据到 numpy 数组中
    dataArray1 = dataset1.ReadAsArray()
    print(dataArray1.shape)

    # 关闭数据集
    del dataset1
    # 打开遥感影像文件2
    print('inputName2', inputName2)
    dataset2 = gdal.Open(inputName2)
    # 读取图像大小
    width2 = dataset2.RasterXSize
    height2 = dataset2.RasterYSize
    print('width,height', width2, height2)
    # 读取遥感影像数据到 numpy 数组中
    dataArray2 = dataset2.ReadAsArray()
    print(dataArray2.shape)
    # 关闭数据集
    del dataset2
    width = min(width1, width2)
    height = min(height1, height2)

    result_dict = dict(LandcoverList)


# 主程序
if __name__ == '__main__':
    # 计算程序运行时间
    start = time.time()
    inputfile1 = r"E:\NSW\correlation.tif"
    inputfile2 = r"E:\NSW\igbpLandCover_2010_250m.tif"
    outputfile = r"E:\NSW\cor_P.tif"
    dataset1 = gdal.Open(inputfile1)
    dataset2 = gdal.Open(inputfile2)
    # 读取遥感影像数据到 numpy 数组中
    dataArray1 = pd.DataFrame(dataset1.ReadAsArray())
    dataArray2 = pd.DataFrame(dataset2.ReadAsArray())



    landcover_dict = {
        '1': 'ENF',
        '2': 'EBF',
        '4': 'DBF',
        '5': 'MF',
        '6': 'CS',
        '7': 'OS',
        '8': 'WS',
        '9': 'S',
        '10': 'G',
        '11': 'PW',
        '12': 'CL',
        '13': 'UBL',
        '14': 'CNVM',
        '16': 'B',
    }
    abbreviations = [
        'Evergreen\nNeedleleaf\nForests',
        'Evergreen\nBroadleaf\nForests',
        'Deciduous\nBroadleaf\nForests',
        'Mixed\nForests',
        'Closed\nShrublands',
        'Open\nShrublands',
        'Woody\nSavannas',
        'Savannas',
        'Grasslands',
        'Permanent\nWetlands',
        'Croplands',
        'Urban\nand\nBuilt-up\nLands',
        'Cropland\nNatural\nVegetation\nMosaics',
        'Barren',

    ]
    colors = [
        '#05450a',
        '#086a10',
        '#78d203',
        '#009900',
        '#c6b044',
        '#dcd159',
        '#dade48',
        '#fbff13',
        '#b6ff05',
        '#27ff87',
        '#c24f44',
        '#a5a5a5',
        '#ff6d4c',
        '#f9ffa4',
    ]

    result_dict = dict.fromkeys(landcover_dict.values(), None)

    for i in landcover_dict.keys():

        n = dataArray1[dataArray2 == int(i)]
        # 先将二维DataFrame转换为一维的数组Series,再消除Series中的NaN值，最后转换为numpy数组
        series = n.stack().dropna().to_numpy()
        result_dict[landcover_dict[i]] = series
    data = list(result_dict.values())
    labels = list(result_dict.keys())
    plt.boxplot(data, labels=abbreviations,showfliers=False,patch_artist=True)
    plt.xticks([])
    # 设置每个箱线的填充颜色
    for box, color in zip(plt.boxplot(data, showfliers=False, patch_artist=True)['boxes'], colors):
        box.set(facecolor=color)


    # 设置图标题
    plt.title('Box Plot of Correlation Coefficient over Landcovers')
    plt.show()
    print(result_dict)








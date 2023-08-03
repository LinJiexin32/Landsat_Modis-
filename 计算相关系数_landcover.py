import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# 读取csv文件
def read_csv(filename):
    data = pd.read_csv(filename)
    # 读取landcover类型
    name = filename.split('\\')[-1].split('.')[0].split('_')[-1]
    # 读取‘year’列数据
    year = data['year']
    # 读取‘correlation’列数据
    correlation = data['correlation']
    # 读取‘valid sample number’列数据
    valid_sample_number = data['valid sample number']
    year = [ int(str(i).replace(',','')) for i in year]
    valid_sample_number = [ int(str(i).replace(',','')) for i in valid_sample_number]
    mean_sample_number = int (np.mean(valid_sample_number))
    return year, correlation, mean_sample_number,name


# 读取文件夹下所有csv文件的文件名
inputFolder = r'E:\Landsat_Modis_NDVI_trend\逐年相关系数\gsMax_Landcover'
# Cropland  250,227,156
# Forest	68,111,51
# Shrub	    51,160,44
# Grassland	171,211,123
# Water	    30,105,180
# Sonw/Ice	166,206,227
# Bareland	207,189,163
colorDic = {'full':'#ff0000','Cropland':'#FAE39C','Forest':'#446f33','Shrub':'#33a02c','Grassland':'#abd18b','Water':'#1e6ee6','Sonw/Ice':'#a6cee3','Bareland':'#cfbda5'}
# 获取文件夹中所有的.csv文件路径
inputFileList = []
for root, dirs, files in os.walk(inputFolder):
    for f in files:
        if f.endswith(".csv"):
            inputFileList.append(os.path.join(root, f))
print(inputFileList)

# 将所有的csv文件的数据绘制同在一张图上
plt.figure(figsize=(26,18))
plt.xlabel('year',fontsize=10,fontweight='bold',color='black',style='italic')
plt.ylabel('correlation',fontsize=10,fontweight='bold',color='black',style='italic')
plt.title('Correlation between Landsat and Modis NDVI',fontsize=20)
for i in  inputFileList:
    year, correlation,  mean_sample_number,name = read_csv(i)
    plt.plot(year, correlation, label=name,linewidth=0.8,marker='o', markersize=3, color=colorDic[name],linestyle='-.')
    plt.text(year[21],correlation[21],name,fontsize=10,color=colorDic[name])
    plt.text(2023,correlation[21],mean_sample_number,fontsize=10,color=colorDic[name])
plt.xlim(1999,2028)
plt.ylim(-0.1,1.1)
# 图例放在右下角
plt.legend(loc='lower right',)
plt.savefig(r'E:\Landsat_Modis_NDVI_trend\逐年相关系数\gsMax_Landcover\折线图.png',dpi=300)
plt.show()




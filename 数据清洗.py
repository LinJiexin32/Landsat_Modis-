import os
import pandas as pd
import ast

def read_csv(filename):
    data = pd.read_csv(filename)
    # 读取landcover类型
    name = filename.split('\\')[-1].split('.')[0].split('_')[0]
    # 读取‘year’列数据
    year_list = data['year']
    # 读取‘Landsat NDVI List’列数据
    L_NDVI_list = data['Landsat NDVI List']
    # 读取‘Modis NDVI List’列数据
    M_NDVI_list = data['MODIS NDVI List']
    year_list = [int(year) for year in year_list]

    result_list = []
    for i in range(len(year_list)):
        dic = {}
        year = year_list[i]
        L_NDVI = ast.literal_eval(L_NDVI_list[i])
        M_NDVI = ast.literal_eval(M_NDVI_list[i])
        dic['year'] = year
        dic['ndvi'] = list(zip(L_NDVI,M_NDVI))
        dic['landcover'] = name
        result_list.append(dic)
    return result_list

inputFolder = r'E:\Landsat_Modis_NDVI_trend\NDVI_sample_points\未处理'
outputFile = r'E:\Landsat_Modis_NDVI_trend\NDVI_sample_points\数据清洗结果\resul.csv'

inputFileList = []
for root, dirs, files in os.walk(inputFolder):
    for f in files:
        if f.endswith(".csv"):
            inputFileList.append(os.path.join(root, f))
print(inputFileList)
with open(outputFile,'w') as f:
    f.write('year,L_NDVI,M_NDVI,landcover\n')
    for file in inputFileList:
        data_list = read_csv(file)
        for data in data_list:
            year = data['year']
            ndvi_list = data['ndvi']
            landcover = data['landcover']
            for ndvi in ndvi_list:
                f.write(str(year)+','+str(ndvi[0])+','+str(ndvi[1])+','+landcover+'\n')




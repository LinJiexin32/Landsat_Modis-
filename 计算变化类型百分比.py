import csv
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

csv.field_size_limit(500 * 1024 * 1024)


def read_data(filename):
    # 打开 CSV 文件
    with open(filename, 'r') as file:
        # 创建 CSV 读取器
        reader = csv.DictReader(file)
        # 用于存储所有 area 列的信息
        area_list = []
        name_list = []
        percent_list = []
        for row in reader:
            # 读取 area 列的信息
            area = row['area']
            name = row['name']
            percent = row['percent']
            # 将 area 添加到 area_list 中
            area_list.append(area)
            name_list.append(name)
            percent_list.append(percent)
    return {'area': np.array(area_list,dtype=float), 'name': name_list, 'percent': percent_list}

data  = read_data(r"E:\Landsat_Modis_NDVI_trend\变化类型及百分比\L_list.csv")
print(data)

# create a pie chart
plt.figure(figsize=(20, 6.5))
plt.pie(data['area'], labels=data['name'],labeldistance=1.5)

# add a title to the chart
plt.title('Distribution of Areas')
plt.legend()
plt.show()

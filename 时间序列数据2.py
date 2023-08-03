import csv
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
csv.field_size_limit(500 * 1024 * 1024)
month = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}
# 打开 CSV 文件
point = '109.36699, 19.64705'
with open(r"D:\Backup\Downloads\ee-chart (10).csv", 'r') as file:
    # 创建 CSV 读取器
    reader = csv.reader(file)
    next(reader) # 跳过标题行
    dates, ndvis = [], []
    for row in reader:
        if row[1] : # 仅处理有有效数据的行
            # if eval(row[1]) > 0.2:
            # row[0] = "Apr 21, 2000"
            m = row[0].strip('"').split(' ')[0]
            d = row[0].strip('"').split(' ')[1].strip(',')
            y = row[0].strip('"').split(' ')[2]
            dates.append(datetime(int(y), month[m], int(d)))
            ndvis.append(float(row[1]))
print(dates)
print(ndvis)
# 绘制图表
# 设置图像大小
plt.figure(figsize=(12, 4))
plt.plot(dates, ndvis,linewidth=0.3, marker='o', markersize=2, markerfacecolor='white',markeredgecolor='red')
plt.xlabel('Time')
plt.ylabel('NDVI')
# plt.title('NDVI over Time'+'    '+ point)

plt.show()
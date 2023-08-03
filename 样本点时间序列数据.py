import csv
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
csv.field_size_limit(500 * 1024 * 1024)
output_folder = 'C://Users//Administrator//Desktop//test//'
def read_data(data):
    # 读取data 列并将其转换成列表
    data = str(data).replace('[', '').replace(']', '').split(',')
    # 将data按照每隔5个元素分成一个列表
    data = [data[i:i + 5] for i in range(0, len(data), 5)]
    data =  np.array(data)[1:,1:]

    # 将' longitude', ' latitude', ' time', ' ndvi'字段的元素变为float类型
    for i in range(0, len(data)):
        if  data[i][3] == ' null':
            data[i][3] = np.nan
        else:
            data[i][3] = float(data[i][3])
    # 类型转换为float64
    data = np.array(data).astype(np.float64)
    return  data

class Point:
    # 定义一个类，用于存储样本点的信息
    def __init__(self, longitude, latitude,):
        self.longitude = longitude
        self.latitude = latitude
        self.L_ndviList = []
        self.L_timeList = []
        self.M_timeList = []
        self.M_ndviList = []
        self.Lmax_timeList = []
        self.Lmax_ndviList = []
        self.Mmax_timeList = []
        self.Mmax_ndviList = []
    def L_addData(self,ndvi,time):
        # 添加数据
        self.L_ndviList.append(ndvi)
        self.L_timeList.append(time)
    def M_addData(self,ndvi,time):
        # 添加数据
        self.M_ndviList.append(ndvi)
        self.M_timeList.append(time)
    def ListProcess(self):
        # 将Landsat 时间和ndvi按照时间顺序排序
        self.L_data = zip(self.L_timeList, self.L_ndviList)
        self.L_data = sorted(self.L_data, key=lambda x: x[0])
        # 去除ndvi为nan的值
        self.L_data = [x for x in self.L_data if str(x[1]) != 'nan']
        # 将时间和ndvi分别存储到列表中
        self.L_sorted_timeList = pd.to_datetime([x[0] for x in self.L_data], unit='ms')
        self.L_sorted_ndviList = [x[1] for x in self.L_data]

        # 将MODIS时间和ndvi按照时间顺序排序
        self.M_data = zip(self.M_timeList, self.M_ndviList)
        self.M_data = sorted(self.M_data, key=lambda x: x[0])
        # 去除ndvi为nan的值
        self.M_data = [x for x in self.M_data if str(x[1]) != 'nan']
        # 将时间和ndvi分别存储到列表中
        self.M_sorted_timeList = pd.to_datetime([x[0] for x in self.M_data], unit='ms')
        self.M_sorted_ndviList = [x[1] for x in self.M_data]
    def getMax(self):
        # 获取各年的最大值以及对应的时间
        self.ListProcess()
        # 获取Landsat最大值
        start_year = self.L_sorted_timeList[0].year
        end_year = self.L_sorted_timeList[-1].year
        self.L_sorted_data = list(zip(self.L_sorted_timeList, self.L_sorted_ndviList))
        for i in range(start_year, end_year + 1):
            # 获取每年的最大值
            yearList = []
            for j in range(len(self.L_sorted_data)):
                if self.L_sorted_data[j][0].year == i:
                    yearList.append(self.L_sorted_data[j])
            if len(yearList) == 0:
                continue
            maxNdvi = max(yearList, key=lambda x: x[1])[1]
            # 获取每年最大值
            self.Lmax_ndviList.append(maxNdvi)
            # 获取每年最大值对应的时间
            maxNdvi_time = max(yearList, key=lambda x: x[1])[0]
            self.Lmax_timeList.append(maxNdvi_time)

        # 获取MODIS最大值
        start_year = self.M_sorted_timeList[0].year
        end_year = self.M_sorted_timeList[-1].year
        self.M_sorted_data = list(zip(self.M_sorted_timeList, self.M_sorted_ndviList))
        for i in range(start_year, end_year + 1):
            # 获取每年的最大值
            yearList = []
            for j in range(len(self.M_sorted_data)):
                if self.M_sorted_data[j][0].year == i:
                    yearList.append(self.M_sorted_data[j])
            maxNdvi = max(yearList, key=lambda x: x[1])[1]
            # 获取每年最大值
            self.Mmax_ndviList.append(maxNdvi)
            # 获取每年最大值对应的时间
            maxNdvi_time = max(yearList, key=lambda x: x[1])[0]
            self.Mmax_timeList.append(maxNdvi_time)
    def drawNdviSeries(self):
        self.getMax()
       # 绘制ndvi时间序列图
        fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
        ax1.plot(self.L_sorted_timeList, self.L_sorted_ndviList,linewidth=0.3, marker='o', markersize=2, markerfacecolor='white',
                 markeredgecolor='blue')
        ax1.plot(self.Lmax_timeList, self.Lmax_ndviList, linewidth=1, marker='o', markersize=4, markerfacecolor='white',
                 markeredgecolor='blue')

        ax1.set_xlabel('Time',fontsize=20,fontweight='bold',color='black',style='italic')
        ax1.set_ylabel('NDVI',fontsize=20,fontweight='bold',color='black',style='italic')
        ax1.set_title('Landsat',fontsize=20,fontweight='bold',color='black',style='italic')
        ax2.plot(self.M_sorted_timeList, self.M_sorted_ndviList, linewidth=0.3,marker='o', markersize=2, markerfacecolor='white',
                 markeredgecolor='red')
        ax2.plot(self.Mmax_timeList, self.Mmax_ndviList, linewidth=1, marker='o', markersize=4, markerfacecolor='white',
                    markeredgecolor='red')
        ax2.set_xlabel('Time',fontsize=20,fontweight='bold',color='black',style='italic')
        ax2.set_title('MODIS',fontsize=20,fontweight='bold',color='black',style='italic')
        fig.suptitle('longitude: ' + str(self.longitude) +'     ' +' latitude: ' + str(self.latitude),fontsize=18)
        plt.ylim(0, 1.0)
        # 标注图例
        ax1.legend(['NDVI', 'Max NDVI of the Year'], loc='upper left', fontsize=12)
        ax2.legend(['NDVI', 'Max NDVI of the Year'], loc='upper left', fontsize=12)


        # 设置图片尺寸尽可能大并保存图片
        fig.set_size_inches(18.5, 10.5)
        fig.savefig(output_folder + str(self.longitude) + '_' + str(self.latitude) + '.png', dpi=400)
        # plt.show()
        # print('图片保存成功！')
        plt.close()
    def wirtePoints(self):
        with open(output_folder + 'points.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([self.longitude, self.latitude])


# 打开 CSV 文件
with open(r"D:\Backup\Downloads\landsat_test.csv", 'r') as file:
    # 创建 CSV 读取器
    reader = csv.DictReader(file)
    # 用于存储所有 data 字段的信息
    L_data_list = []
    # 遍历 CSV 文件中的每一行记录
    for row in reader:
        # 提取 data 字段的信息，并将其添加到列表中
        L_data_list.append(row['data'])
with open(r"D:\Backup\Downloads\MODIS_test.csv", 'r') as file:
    # 创建 CSV 读取器
    reader = csv.DictReader(file)
    # 用于存储所有 data 字段的信息
    M_data_list = []
    # 遍历 CSV 文件中的每一行记录
    for row in reader:
        # 提取 data 字段的信息，并将其添加到列表中
        M_data_list.append(row['data'])
print(len(L_data_list))
print(len(M_data_list))
# 创建一个字典，用于存储样本点的信息
point_dict = {}
for data in L_data_list:
    data = read_data(data)
    # 遍历 data 列表中的每一个元素
    for i in range(len(data)):
        # 提取经度和纬度信息
        longitude = data[i][0]
        latitude = data[i][1]
        # 如果字典中没有该经纬度信息，则创建一个 Point 类的对象
        if (longitude, latitude) not in point_dict:
            point_dict[(longitude, latitude)] = Point(longitude, latitude)
        # 将 ndvi 和 time 添加到 Point 类的对象中
        point_dict[(longitude, latitude)].L_addData(data[i][3], data[i][2])
for data in M_data_list:
    data = read_data(data)
    # 遍历 data 列表中的每一个元素
    for i in range(len(data)):
        # 提取经度和纬度信息
        longitude = data[i][0]
        latitude = data[i][1]
        # 如果字典中没有该经纬度信息，则创建一个 Point 类的对象
        if (longitude, latitude) not in point_dict:
            point_dict[(longitude, latitude)] = Point(longitude, latitude)
        # 将 ndvi 和 time 添加到 Point 类的对象中
        point_dict[(longitude, latitude)].M_addData(data[i][3] * 0.0001, data[i][2])

# 绘制样本点的 ndvi 时间序列图,并使用tqdm显示进度条
for point in tqdm(point_dict.values()):
    point.drawNdviSeries()
    point.wirtePoints()





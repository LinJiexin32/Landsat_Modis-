import os

# 获取当前工作目录
path = os.chdir(r"E:\Landsat_Modis_NDVI_trend\Landsat\V2_78\ndvi")

# 获取文件夹中所有文件和文件名
files = os.listdir(path)


# 按文件大小对文件进行排序
sorted_files = []
for file in files:
    sorted_files.append([file, os.path.getsize(file)])

sorted_files.sort(key=lambda x: x[1])
print(sorted_files)

# 重命名文件
for i in range(len(sorted_files)):
    os.rename(sorted_files[i][0], "Landsat_ndvi__"+str(i) + ".tif")  # 重命名文件
    print(sorted_files[i][0] + " has been renamed to " + "Landsat_ndvi__"+ str(i) + ".tif")   # 打印重命名信息

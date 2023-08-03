import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

#读取csv文件
df = pd.read_csv(r"E:\Landsat_Modis_NDVI_trend\NDVI_sample_points\数据清洗结果\resul.csv")

#定义颜色
colors = {"Cropland":"#fae39c", "Forest":"#446f33", "Shrub":"#33a02c",
          "Grassland":"#abd57b","Barren":"#cfbda3","Impervious":"#e24290","full":"#ff0000"}

#任务1
grouped=df.groupby('year')
year_lst=[]
NDVI_M_lst=[]
NDVI_L_lst=[]

for name,group in grouped:
    year_lst.append(name)
    NDVI_M_lst.append(group['M_NDVI'].mean())
    NDVI_L_lst.append(group['L_NDVI'].mean())
plt.plot(year_lst, NDVI_L_lst, 'g-', label='Landsat NDVI')
plt.plot(year_lst, NDVI_M_lst, 'r--', label='MODIS NDVI')
plt.xlabel('Year')
plt.ylabel('NDVI')
plt.legend()
plt.title('MODIS and Landsat NDVI Mean Over the Years')
plt.show()

#任务2
correlations = [pearsonr(group["M_NDVI"], group["L_NDVI"])[0] for _, group in grouped]
plt.plot(year_lst, correlations, 'b-')
plt.xlabel('Year')
plt.ylabel('Correlation Coefficient')
plt.title('Correlation between MODIS and Landsat NDVI Over the Years')
plt.show()

#任务3
pmres = [np.mean(np.abs((group["L_NDVI"] - group["M_NDVI"]) / group["L_NDVI"])) for _, group in grouped]
plt.plot(year_lst, pmres, 'y-')
plt.xlabel('Year')
plt.ylabel('Percent Mean Relative Error')
plt.title('PMRE between MODIS and Landsat NDVI Over the Years')
plt.show()

#任务4
biases = [np.mean(group["L_NDVI"] - group["M_NDVI"]) for _, group in grouped]
plt.plot(year_lst, biases, 'c-')
plt.xlabel('Year')
plt.ylabel('Bias')
plt.title('Bias between MODIS and Landsat NDVI Over the Years')
plt.show()

#任务5-8:

grouped_lc=df.groupby('landcover')
dic = {}
for lc_name,group_lc in grouped_lc:
    grouped_year=group_lc.groupby('year')
    year_lst=[]
    ls_ndvi_lst=[]
    mo_ndvi_lst=[]
    corr_lst=[]
    pmre_lst=[]
    bias_lst=[]
    for year_name,group_year in grouped_year:
        year_lst.append(year_name)
        ls_ndvi_lst.append(group_year['L_NDVI'].mean())
        mo_ndvi_lst.append(group_year['M_NDVI'].mean())
        corr_lst.append(pearsonr(group_year["M_NDVI"], group_year["L_NDVI"])[0])
        pmre_lst.append(np.mean(np.abs((group_year["L_NDVI"] - group_year["M_NDVI"]) / group_year["L_NDVI"])))
        bias_lst.append(np.mean(group_year["L_NDVI"] - group_year["M_NDVI"]))
    dic[lc_name]={'year_lst':year_lst,'ls_ndvi_lst':ls_ndvi_lst,'mo_ndvi_lst':mo_ndvi_lst,'corr_lst':corr_lst,
                  'pmre_lst':pmre_lst,'bias_lst':bias_lst}
# 任务5：分别统计每个landcover类型上MODIS 和 Landsat NDVI的均值在2000年到2022年的变化趋势。
plt.figure(figsize=(20, 14))

    #分两个子图，子图1绘制Landsat NDVI均值变化，子图2绘制MODIS NDVI均值变化
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

for landcover_name in list(dic.keys()):
    # 子图1绘制LandsatNDVI均值变化
    ax1.plot(dic[landcover_name]['year_lst'], dic[landcover_name]['ls_ndvi_lst'], linewidth=1.5, label='Landsat NDVI', color=colors[landcover_name], linestyle='-')
    ax2.plot(dic[landcover_name]['year_lst'], dic[landcover_name]['mo_ndvi_lst'], linewidth=1.5, label='MODIS NDVI', color=colors[landcover_name], linestyle='--')
    ax1.set_xlabel('Time', fontsize=10, fontweight='bold', color='black', style='italic')
    ax1.set_ylabel('Landsat_Mean_NDVI', fontsize=10, fontweight='bold', color='black', style='italic')
    ax2.set_xlabel('Time', fontsize=10, fontweight='bold', color='black', style='italic')
    ax2.set_ylabel('MODIS_Mean_NDVI', fontsize=10, fontweight='bold', color='black', style='italic')
#     plt.plot(dic[landcover_name]['year_lst'], dic[landcover_name]['ls_ndvi_lst'], linewidth=0.5, label='Landsat NDVI', color=colors[landcover_name], linestyle='-')
#     plt.plot(dic[landcover_name]['year_lst'], dic[landcover_name]['mo_ndvi_lst'], linewidth=0.5, label='MODIS NDVI', color=colors[landcover_name], linestyle='--')
#     # plt.plot(year_lst, corr_lst, linewidth=2, label='Correlation', color=colors[lc_name], linestyle='-.')
#     # plt.plot(year_lst, pmre_lst, linewidth=2, label='PMRE', color=colors[lc_name], linestyle=':')
#     # plt.plot(year_lst, bias_lst, linewidth=2, label='Bias', color=colors[lc_name])
plt.show()

# 任务6：分别统计每个landcover类型上MODIS 和 Landsat NDVI的相关系数在2000年到2022年的变化趋势。
plt.figure(figsize=(20, 14))
for landcover_name in list(dic.keys()):
    plt.plot(dic[landcover_name]['year_lst'], dic[landcover_name]['corr_lst'], linewidth=1.0, label='Correlation', color=colors[landcover_name], linestyle='-')
    plt.xlabel('Time', fontsize=10, fontweight='bold', color='black', style='italic')
    plt.ylabel('Correlation Coefficient', fontsize=10, fontweight='bold', color='black', style='italic')
plt.show()
# 任务7：分别统计每个landcover类型上MODIS 和 Landsat NDVI的PMRE在2000年到2022年的变化趋势。
plt.figure(figsize=(20, 14))
for landcover_name in list(dic.keys()):
    plt.plot(dic[landcover_name]['year_lst'], dic[landcover_name]['pmre_lst'], linewidth=1.0, label='PMRE', color=colors[landcover_name], linestyle='-')
    plt.xlabel('Time', fontsize=10, fontweight='bold', color='black', style='italic')
    plt.ylabel('PMRE', fontsize=10, fontweight='bold', color='black', style='italic')
plt.show()
# 任务8：分别统计每个landcover类型上MODIS 和 Landsat NDVI的Bias在2000年到2022年的变化趋势。
plt.figure(figsize=(20, 14))
for landcover_name in list(dic.keys()):
    plt.plot(dic[landcover_name]['year_lst'], dic[landcover_name]['bias_lst'], linewidth=1.0, label='Bias', color=colors[landcover_name], linestyle='-')
    plt.xlabel('Time', fontsize=10, fontweight='bold', color='black', style='italic')
    plt.ylabel('Bias', fontsize=10, fontweight='bold', color='black', style='italic')
plt.show()

# 任务9
results = []
for lc_name,group in grouped_lc:
    corr = pearsonr(group['M_NDVI'], group['L_NDVI'])[0]
    pmre = np.mean(np.abs((group["L_NDVI"] - group["M_NDVI"]) / group["L_NDVI"]))
    bias = np.mean(group["L_NDVI"] - group["M_NDVI"])
    #保留四位小数
    corr = round(corr, 4)
    pmre = round(pmre, 4)
    bias = round(bias, 4)
    results.append([lc_name, corr, pmre, bias])

# 创建表格
results_df = pd.DataFrame(results, columns=["Landcover", "Correlation", "PMRE", "Bias"])
print(results_df)

# 绘制表格
fig, ax = plt.subplots(figsize=(10, 5))
ax.axis('off')
ax.axis('tight')
table = ax.table(cellText=results_df.values, colLabels=results_df.columns, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(14)
table.scale(1, 1.5)
plt.title("Correlation, PMRE, and Bias for each Landcover")
plt.show()
import pandas as pd
import matplotlib.pyplot as plt

# 1. 从csv文件中读取数据
data = pd.read_csv(r"E:\Landsat_Modis_NDVI_trend\NDVI_sample_points\数据清洗结果\resul.csv")

# 2. 计算MODIS和Landsat NDVI均值随年份的变化情况
mean_ndvi = data.groupby("year").mean()
years = mean_ndvi.index

# 绘制折线图
plt.plot(years, mean_ndvi["L_NDVI"], label="Landsat NDVI")
plt.plot(years, mean_ndvi["M_NDVI"], linestyle="--", label="MODIS NDVI")
plt.xlabel("Year")
plt.ylabel("NDVI Mean")
plt.title("Mean NDVI Variation")
plt.legend()
plt.show()

# 3. 计算每年MODIS和Landsat NDVI的相关性
corr_ndvi = data.groupby("year").corr().loc[:, "L_NDVI"]["M_NDVI"]

# 绘制折线图
plt.plot(years, corr_ndvi)
plt.xlabel("Year")
plt.ylabel("Correlation Coefficient")
plt.title("Correlation between MODIS and Landsat NDVI")
plt.show()

# 4. 计算每年MODIS和Landsat NDVI的Percent Mean Relative Error (PMRE)
pmre_ndvi = ((data["L_NDVI"] - data["M_NDVI"]) / data["L_NDVI"]).abs().mean()

# 绘制折线图
plt.plot(years, pmre_ndvi)
plt.xlabel("Year")
plt.ylabel("PMRE")
plt.title("PMRE between MODIS and Landsat NDVI")
plt.show()

# 5. 统计每个landcover类型上MODIS和Landsat NDVI的均值在2000年到2022年的变化趋势
landcover_colors = {
    "Cropland": (250, 227, 156),
    "Forest": (68, 111, 51),
    "Shrub": (51, 160, 44),
    "Grassland": (171, 211, 123),
    "Barren": (207, 189, 163),
    "Impervious": (226, 66, 144)
}

# 提取指定landcover类型的数据
def extract_landcover_data(landcover):
    return data[data["landcover"] == landcover]

# 绘制折线图
for landcover, color in landcover_colors.items():
    landcover_data = extract_landcover_data(landcover)
    mean_ndvi_landcover = landcover_data.groupby("year").mean()
    plt.plot(years, mean_ndvi_landcover["L_NDVI"], color=color, label=landcover + " (Landsat)")
    plt.plot(years, mean_ndvi_landcover["M_NDVI"], linestyle="--", color=color, label=landcover + " (MODIS)")

plt.xlabel("Year")
plt.ylabel("NDVI Mean")
plt.title("Mean NDVI Variation by Landcover")
plt.legend()
plt.show()

# 6. 统计每个landcover类型上MODIS和Landsat NDVI的相关系数在2000年到2022年的变化趋势
# 绘制折线图
for landcover, color in landcover_colors.items():
    landcover_data = extract_landcover_data(landcover)
    corr_ndvi_landcover = landcover_data.groupby("year").corr().loc[:, "L_NDVI"]["M_NDVI"]
    plt.plot(years, corr_ndvi_landcover, color=color, label=landcover)

plt.xlabel("Year")
plt.ylabel("Correlation Coefficient")
plt.title("Correlation between MODIS and Landsat NDVI by Landcover")
plt.legend()
plt.show()

# 7. 统计每个landcover类型上MODIS和Landsat NDVI的PMRE在2000年到2022年的变化趋势
# 绘制折线图
for landcover, color in landcover_colors.items():
    landcover_data = extract_landcover_data(landcover)
    pmre_ndvi_landcover = ((landcover_data["L_NDVI"] - landcover_data["M_NDVI"]) / landcover_data["L_NDVI"]).abs().mean()
    plt.plot(years, pmre_ndvi_landcover, color=color, label=landcover)

plt.xlabel("Year")
plt.ylabel("PMRE")
plt.title("PMRE between MODIS and Landsat NDVI by Landcover")
plt.legend()
plt.show()

# 8. 统计每个landcover类型上MODIS和Landsat NDVI的Bias在2000年到2022年的变化趋势
# 绘制折线图
for landcover, color in landcover_colors.items():
    landcover_data = extract_landcover_data(landcover)
    bias_ndvi_landcover = landcover_data["L_NDVI"] - landcover_data["M_NDVI"]
    plt.plot(years, bias_ndvi_landcover, color=color, label=landcover)

plt.xlabel("Year")
plt.ylabel("Bias")
plt.title("Bias between MODIS and Landsat NDVI by Landcover")
plt.legend()
plt.show()

# 9. 统计每个landcover类型上MODIS和Landsat NDVI的相关系数、PMRE、Bias的情况
landcover_stats = pd.DataFrame(columns=["Landcover", "Correlation", "PMRE", "Bias"])

for landcover, color in landcover_colors.items():
    landcover_data = extract_landcover_data(landcover)
    corr = landcover_data["L_NDVI"].corr(landcover_data["M_NDVI"])
    pmre = ((landcover_data["L_NDVI"] - landcover_data["M_NDVI"]) / landcover_data["L_NDVI"]).abs().mean()
    bias = (landcover_data["L_NDVI"] - landcover_data["M_NDVI"]).mean()
    landcover_stats = landcover_stats.append(
        {"Landcover": landcover, "Correlation": corr, "PMRE": pmre, "Bias": bias},
        ignore_index=True
    )

print(landcover_stats)

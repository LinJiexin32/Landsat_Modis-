#encoding=utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# 读取第csv文件
fileName = r"E:\Landsat_Modis_NDVI_trend\Slope 相关系数\M_L_slope_M_L_slope.csv"
df = pd.read_csv(fileName)

# 读取csv文件第二列
L_slope = df['L_slope']
M_slope = df['M_slope']
print(L_slope)
print(M_slope)
label1 = "Landsat"
label2 = "MODIS"

# 绘制散点图
fig, ax = plt.subplots()
ax.scatter(L_slope, M_slope,s=1, label='Scatter plot', color='blue')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')

# 添加网格线
ax.grid(True)
# 计算回归方程
slope, intercept, r_value, p_value, std_err = linregress(L_slope, M_slope)

r_squared = r_value**2

# 绘制回归线和文本信息
x = np.linspace(L_slope.min(), L_slope.max(), 100)
y = slope*x + intercept
ax.plot(x, y, label='Regression line', color='red')
textstr = '\n'.join((
    r'$y=%.2fx+%.2f$' % (slope, intercept),
    r'$R=%.2f$' % (r_value,),
    r'$p=%.10f$' % (p_value,)))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.95, 0.05, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='bottom', horizontalalignment='right', bbox=props)

# 添加坐标轴标签和图例
ax.set_xlabel(label1)
ax.set_ylabel(label2)
ax.legend()
plt.show()


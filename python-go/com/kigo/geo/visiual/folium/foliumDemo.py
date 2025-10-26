# encoding=utf-8
"""
# 可视化
https://blog.csdn.net/junshan2009/article/details/87000143?utm_medium=distribute.pc_relevant.none-task-blog-baidujs-9
"""

import numpy as np
import pandas as pd
import seaborn as sns
import folium
import webbrowser
from folium.plugins import HeatMap


'''
二 使用folium绘制散点图，热力图
'''
#导入数据集：
posi = pd.read_excel("D:/Python/File/Cities2015.xlsx")
posi = posi.dropna()

#生成所需要的数组格式数据：
lat = np.array(posi["lat"][0:len(posi)])
lon = np.array(posi["lon"][0:len(posi)])
pop = np.array(posi["pop"][0:len(posi)],dtype=float)
gdp = np.array(posi["GDP"][0:len(posi)],dtype=float)
data1 = [[lat[i],lon[i],pop[i]] for i in range(len(posi))]

#创建以高德地图为底图的密度图：
map_osm = folium.Map(
    location=[35,110],
    zoom_start=5,
    tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
    attr="&copy; <a href="http://ditu.amap.com/">高德地图</a>"
    )

#创建以腾讯地图为底图的密度图：
map_osm = folium.Map(
    location=[35,110],
    zoom_start=5,
    tiles='http://rt{s}.map.gtimg.com/realtimerender?z={z}&x={x}&y={y}&type=vector&style=0',
    attr="&copy; <a href="http://map.qq.com/">腾讯地图</a>"
    )

#生成交互式地图：
HeatMap(data1).add_to(map_osm)
file_path = r"D:/Python/Image/People.html"
map_osm.save(file_path)
webbrowser.open(file_path)


'''
folium的散点图更适合作展示，考虑到加载的顺畅性，不建议读取太大的数据，另外其组件可能会读一些外网的js，如果所在的网络不能访问google可能效果无法展示。解决办法是把里面的js地址替换成国内的镜像。
'''
import pandas as pd
import numpy as np
import os
import folium
from folium import plugins
import webbrowser
import geopandas as gp

#数据导入：
full = pd.read_excel("D:/Python/File/Cities2015.xlsx")
full = full.dropna()

#创建地图对象：
schools_map = folium.Map(location=[full['lat'].mean(), full['lon'].mean()], zoom_start=10)
marker_cluster = plugins.MarkerCluster().add_to(schools_map)

#标注数据点：
for name,row in full.iterrows():
     folium.Marker([row["lat"], row["lon"]], popup="{0}:{1}".format(row["cities"], row["GDP"])).add_to(marker_cluster)
#逐行读取经纬度，数值，并且打点
#folium.RegularPolygonMarker([row["lat"], row["lon"]], popup="{0}:{1}".format(row["cities"], row["GDP"]),number_of_sides=10,radius=5).add_to(marker_cluster)

schools_map.save('schools_map.html') #保存到本地
webbrowser.open('schools_map.html')  #在浏览器中打开

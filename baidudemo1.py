import json
import sys
import requests  # 导入requests库，这是一个第三方库，把网页上的内容爬下来用的
import pandas as pd
import time
ty = sys.getfilesystemencoding()  # 这个可以获取文件系统的编码形式

# test2018.2.23

# test2

# test3
# 查询百度坐标的链接
# http://api.map.baidu.com/lbsapi/getpoint/index.html

#123.195667,41.912925，123.606156,41.707749
lat_1 = 41.707749
lon_1 = 123.195667
lat_2 = 41.912925
lon_2 = 123.606156  # 坐标范围
N = 0.1  # 间隔
ak = 'ZKKarKb7xngE7PGMe9Asyrv6'
Query = '装修'  # 搜索关键词设置
# 我们把变量都放在前面，后面就不涉及到变量了，如果要爬取别的POI，修改这几个变量就可以了，不用改代码了。

startime = time.time()

poi_name = []
poi_lat = []
poi_lng = []
poi_addr = []
poi_prov = []
poi_city = []
poi_area = []
uid = []
tel = []

print('开始')
urls = []  # 声明一个数组列表
lat_count = int((lat_2 - lat_1) / N + 1)
lon_count = int((lon_2 - lon_1) / N + 1)
for lat in range(0, lat_count):
    lat_b1 = lat_1 + N * lat
    for long in range(0, lon_count):
        lon_b1 = lon_1 + N * long
        url = 'http://api.map.baidu.com/place/v2/search?query=' + str(Query) + '& bounds=' + str(
            lat_b1) + ',' + str(
            lon_b1) + ',' + str(lat_b1 + N) + ',' + str(
            lon_b1 + N) + '&page_size=20&page_num=0' + '&output=json&ak=' + ak
        html = requests.get(url)  # 获取网页信息
        data = html.json()  # 获取网页信息的json格式数据
        Total = data['total']
        Maxpage = int(Total / 20) + 1
        for page in range(0, Maxpage):
            url = 'http://api.map.baidu.com/place/v2/search?query=' + str(Query) + '& bounds=' + str(
                lat_b1) + ',' + str(
                lon_b1) + ',' + str(lat_b1 + N) + ',' + str(
                lon_b1 + N) + '&page_size=20&page_num=' + str(page) + '&output=json&ak=' + ak
            urls.append(url)

            # urls.append(url)的意思是，将url添加入urls这个列表中。

print('url列表读取完成')

for url in urls:
    time.sleep(0.2)  # 为了防止并发量报警，设置了一个10秒的休眠。
    html = requests.get(url)  # 获取网页信息
    data = html.json()  # 获取网页信息的json格式数据
    print(data)
    for item in data['results']:
        poi_name.append(item.get('name', ''))
        poi_lat.append(item['location']['lat'])
        poi_lng.append(item['location']['lng'])
        poi_addr.append(item.get('address', ''))
        poi_prov.append(item.get('province', ''))
        poi_city.append(item.get('city', ''))
        poi_area.append(item.get('area', ''))
        uid.append(item.get('uid', ''))
        tel.append(item.get('telephone', ''))

        # 保存正常数据到csv
    raw = pd.DataFrame(
        {'NAME': poi_name, 'LAT': poi_lat, 'LONG': poi_lng, 'ADDRESS': poi_addr, 'PROV': poi_prov, 'CITY': poi_city,
         'DIST': poi_area, 'UID': uid, 'TEL': tel})
    columns = ['UID', 'NAME', 'PROV', 'CITY', 'DIST', 'ADDRESS', 'TEL', 'LONG', 'LAT']  # 按照自定义排序
    raw.to_csv('./' + '4S' + '.csv', encoding='gb18030', index=False, columns=columns)
    raw.head()

print(time.time() - startime)
print('完成')

# -- coding: utf-8 --

__author__ = 'Y.F'

import datetime
import mysql.connector

connect = mysql.connector.connect(user='root', password='sm4547634', host='127.0.0.1', database='hotspot', port='3306')
cursor = connect.cursor()

# t_unit は、時間の刻み幅
t_unit = datetime.timedelta(minutes=10)
# 緯度、経度の刻み幅を設定(だいたい1km四方の正方形となるようにとった)
lat_unit = 0.008983
lng_unit = 0.011039
# 緯度、経度の境界の設定
lat_inf = 35.540198
lng_inf = 139.545137
lat_sup = 35.817059
lng_sup = 139.921101

# 現在の時刻を取得
t_1 = datetime.datetime.now()
t_0 = t_1 - t_unit

lng_0 = lng_inf
i = 0
while True:
    lat_0 = lat_inf
    lng_1 = lng_0 + lng_unit
    while True:
        lat_1 = lat_0 + lat_unit
        query = "select count(*) from tweets where created_at between '"+str(t_0)+"' and '"+str(t_1)+"' and lat between "+str(lat_0)+" and "+str(lat_1)+"and lng between "+str(lng_0)+" and "+str(lng_1)
        cursor.execute(query)
        count = cursor.fetchall()[0][0]
        # point_lat, point_lng は、それぞれのブロックの代表点
        point_lat = (lat_0 + lat_1) / 2
        point_lng = (lng_0 + lng_1) / 2
        print(str(t_1), str(point_lat), str(point_lng), count, i)
        i += 1
        lat_0 = lat_1
        if lat_1 > lat_sup:
            break

    lng_0 = lng_1
    if lng_1 > lng_sup:
        break

cursor.close()
connect.close()
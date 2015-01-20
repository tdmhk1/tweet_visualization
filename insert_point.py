# -- coding: utf-8 --

__author__ = 'Y.F'

import mysql.connector

# 緯度、経度の刻み幅を設定(だいたい1km四方の正方形となるようにとった)
lat_unit = 0.0089831
lng_unit = 0.0110600
# 緯度、経度の境界の設定
lat_inf = 35.616040
lng_inf = 139.681088
lat_sup = 35.729020
lng_sup = 139.820774

lng_0 = lng_inf

connect = mysql.connector.connect(user='root', password='sm4547634', host='127.0.0.1', database='hotspot', port='3306')
cursor = connect.cursor()

i = 0
while True:
    lat_0 = lat_inf
    lng_1 = lng_0 + lng_unit
    while True:
        lat_1 = lat_0 + lat_unit
        query = 'insert into point (place_no, pointlat, pointlng) values ('+str(i)+', '+str(lat_0)+', '+str(lng_0)+')'
        cursor.execute(query)
        connect.commit()
        i += 1
        lat_0 = lat_1
        if lat_1 > lat_sup:
            break
    lng_0 = lng_1
    if lng_1 > lng_sup:
        break

cursor.close()
connect.close()
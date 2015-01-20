# 現在から10分前までさかのぼって、ツイート数を集計するプログラム
#  -- coding: utf-8 --

__author__ = 'Y.F'

import datetime
import mysql.connector

# 場所を指定して、その領域で過去10分間につぶやかれたツイートを集計する
# 引数 lat_0: 緯度の南の境界, lat_1: 緯度の北の境界, lng_0: 経度の西の境界, lng_1: 経度の東の境界, t_0:集計時間の10分前, t_1:集計時間
def countatlocation(lat_0, lat_1, lng_0, lng_1, t_0, t_1):
    query1 = "select count(*) from tweets where created_at between '"+str(t_0)+"' and '"+str(t_1)+"' and lat between "+str(lat_0)+" and "+str(lat_1)+"and lng between "+str(lng_0)+" and "+str(lng_1)
    cursor.execute(query1)
    # count は、現在から過去10分間に投稿されたツイート数
    count = cursor.fetchall()[0][0]
    query2 = "select count from count where gettime = '"+str(t_0)+"' and pointlat = "+str(lat_0)+" and pointlng = "+str(lng_0)
    cursor.execute(query2)
    try:
        # countbは、20分前から10分前の間に投稿されたツイート数
        countb = cursor.fetchall()[0][0]
        # differenceは、現在と10分前のcountの差分
        difference = count - countb
        linear_expect = 2 * count - countb
    except IndexError:
        difference = "null"
        linear_expect = "null"
    # DBに集計結果を格納
    query3 = 'insert into count (gettime, pointlat, pointlng, count, difference, linear_expect) values ("'+str(t_1)[:19]+'", '+str(lat_0)+', '+str(lng_0)+', '+str(count)+', '+str(difference)+', '+str(linear_expect)+')'
    cursor.execute(query3)
    connect.commit()

# t_unit は、時間の刻み幅
t_unit = datetime.timedelta(minutes=10)
# 現在の時刻を取得
t_1 = datetime.datetime.now()
t_0 = t_1 - t_unit

# 緯度、経度の刻み幅を設定(だいたい1km四方の正方形となるようにとった)
lat_unit = 0.008983
lng_unit = 0.011039
# 緯度、経度の境界の設定
lat_inf = 35.540198
lng_inf = 139.545137
lat_sup = 35.817059
lng_sup = 139.921101

lng_0 = lng_inf

connect = mysql.connector.connect(user='root', password='sm4547634', host='127.0.0.1', database='hotspot', port='3306')
cursor = connect.cursor()

while True:
    lat_0 = lat_inf
    lng_1 = lng_0 + lng_unit
    while True:
        lat_1 = lat_0 + lat_unit
        countatlocation(lat_0, lat_1, lng_0, lng_1, t_0, t_1)
        lat_0 = lat_1
        if lat_1 > lat_sup:
            break
    lng_0 = lng_1
    if lng_1 > lng_sup:
        break

cursor.close()
connect.close()
# テーブルtwitterからテーブルhotspotへ情報をうつす
# -- coding: utf-8 --

__author__ = 'Y.F'

import datetime
import mysql.connector

# python から MySQL へデータを格納する
# コンフィグ の作成
config1 = {
    'user': 'root',
    'password': 'sm4547634',
    'host': '127.0.0.1',
    'database': 'twitter',
}

config2 = {
    'user': 'root',
    'password': 'sm4547634',
    'host': '127.0.0.1',
    'database': 'hotspot',
}

connect1 = mysql.connector.connect(**config1)
cursor1 = connect1.cursor()

# 取得時間
t_sup = datetime.datetime(2015, 1, 16, 23, 59, 59)
t_inf = datetime.datetime(2015, 1, 16, 0, 0, 0)

# 取得地域
lat_inf = 35.616040
lat_sup = 139.681088
lng_inf = 35.732832
lng_sup = 139.824608

# データベースtwitterのテーブルtweetsのカラムtweet_id, text, created_at, lat, lntの情報を取得する
# 条件は、東京23区内
query1 = 'select tweet_id, text, created_at, lat, lng from tweets where created_at between "'+str(t_inf)+'" and "'+str(t_sup)+'" and lat between '+str(lat_inf)+' and '+str(lat_sup)+' and lng between '+str(lng_inf)+' and '+str(lng_sup)
cursor1.execute(query1)

connect2 = mysql.connector.connect(**config2)
cursor2 = connect2.cursor()

for data in cursor1.fetchall():
    query2 = 'insert into tweets_analysis(tweet_id, created_at, lat, lng, text) values('+str(data[0])+', "'+str(data[2])+'", '+str(data[3])+', '+str(data[4])+', "'+str(data[1])+'")'
    cursor2.execute(query2)
    connect2.commit()

cursor1.close()
connect1.close()

cursor2.close()
connect2.close()
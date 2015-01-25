# -- coding: utf-8 --

__author__ = 'Y.F'

from flask import Flask, render_template
from flask.ext.googlemaps import GoogleMaps
import datetime
from decimal import *

# 更新時間に合わせて、datetime型データをminuteの1の位以下切り捨て
def floar_minute_ten(s):
    r = s.minute // 10
    return s.replace(minute = r * 10, second = 0, microsecond = 0)

# 時間と空間の刻み幅
t_unit = datetime.timedelta(minutes=10)
lat_unit = Decimal(0.008984)
lng_unit = Decimal(0.011040)

app = Flask(__name__, template_folder="templates")
app.config['DEBUG'] = True
GoogleMaps(app)

@app.route("/")
def mapview():
    try:

        # サイトの訪問時刻の取得
        t_1 = datetime.datetime.now()
        t_0 = t_1 - t_unit
        datatime=[str(t_0)[10:19], str(t_1)[10:19]]
        # 直近の更新時間(集計時間の確保のため、分の一の位が3を超えたとき更新する)
        t_renew = floar_minute_ten(t_1 - datetime.timedelta(minutes=3))

        import mysql.connector
        connect = mysql.connector.connect(user='root', password='sm4547634', host='127.0.0.1', database='hotspot', port='3306')
        cursor = connect.cursor()
        # 直近の更新時間のツイート数の取得
        query1 = 'select pointlat, pointlng, counts from count_data where gettime = "'+str(t_renew)+'" order by counts desc'
        cursor.execute(query1)
        # ツイート数の場所とツイート数が入った配列を作成
        count_data = []
        for column1 in cursor.fetchall():
            count_data.append(column1)

        # ツイート数が最大の場所の緯度、経度を取得
        latmax = Decimal(count_data[0][0])
        lngmax = Decimal(count_data[0][1])
        # ツイート数が最大の地域のツイートを取得
        query2 = 'select * from tweets where created_at between "'+str(t_0)+'" and "'+str(t_1)+'" and lat between '+str(latmax)+'and '+str(latmax+lat_unit)+' and lng between '+str(lngmax)+'and '+str(lngmax+lng_unit)
        cursor.execute(query2)
        tweet_data_max = []
        for column2 in cursor.fetchall():
            tweet_data_max.append(column2)

        # 直近10分間のツイートを取得
        query3 = 'select * from tweets where created_at between "'+str(t_0)+'" and "'+str(t_1)+'"'
        cursor.execute(query3)
        tweet_data = cursor.fetchall()
        return render_template('direct_represent_web.html', tweet_data=tweet_data, tweet_data_max=tweet_data_max, datatime=datatime, count_data=count_data)

    except Exception as e:
                return e

if __name__=="__main__":
 app.run(debug=True)
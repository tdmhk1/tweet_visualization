# -- coding: utf-8 --

__author__ = 'Y.F'

from flask import Flask, render_template
from flask.ext.googlemaps import GoogleMaps
import datetime
from decimal import *
from flask import request

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
        t_00 = t_1 - datetime.timedelta(minutes=30)
        # 直近の更新時間(集計時間の確保のため、分の一の位が3を超えたとき更新する)
        t_renew_1 = floar_minute_ten(t_1 - datetime.timedelta(minutes=3))
        t_renew_0 = t_renew_1 - datetime.timedelta(minutes=10)
        datatime=[str(t_renew_0)[10:19], str(t_renew_1)[10:19]]

        import mysql.connector
        connect = mysql.connector.connect(user='root', password='sm4547634', host='127.0.0.1', database='hotspot', port='3306')
        cursor = connect.cursor()

        # 直近の更新時間のツイート数の取得
        query1 = 'select pointlat, pointlng, counts from count_data where gettime = "'+str(t_renew_1)+'" order by counts desc'
        cursor.execute(query1)

        # ツイート数の場所とツイート数が入った配列を作成
        count_data = []
        for column1 in cursor.fetchall():
            count_data.append(column1)

        # ツイート数が最大の場所の緯度、経度を取得
        latmax = Decimal(count_data[0][0])
        lngmax = Decimal(count_data[0][1])

        # ツイート数が最大の地域のツイートを取得(過去30分間)
        query2 = 'select * from tweets where created_at between "'+str(t_00)+'" and "'+str(t_1)+'" and lat between '+str(latmax)+'and '+str(latmax+lat_unit)+' and lng between '+str(lngmax)+'and '+str(lngmax+lng_unit)+'order by created_at desc'
        cursor.execute(query2)
        tweet_data_max = []
        for column2 in cursor.fetchall():
            tweet_data_max.append(column2)

        # 直近10分間のツイートを取得
        query3 = 'select * from tweets where created_at between "'+str(t_0)+'" and "'+str(t_1)+'"'
        cursor.execute(query3)
        tweet_data = cursor.fetchall()

        # リンクで表示する文章
        linkdata = ['これから注目の場所のツイートに切り替え', "/trendspot"]
        return render_template('direct_represent_web.html', tweet_data=tweet_data, tweet_data_max=tweet_data_max, datatime=datatime, count_data=count_data, linkdata=linkdata, markerpoint=[35.674436, 139.752848])

    except Exception as e:
                return e

@app.route('/trendspot')
def trendspot():
    try:

        # サイトの訪問時刻の取得
        t_1 = datetime.datetime.now()
        t_0 = t_1 - t_unit
        t_00 = t_1 - datetime.timedelta(minutes=30)
        # 直近の更新時間(集計時間の確保のため、分の一の位が3を超えたとき更新する)
        t_renew_1 = floar_minute_ten(t_1 - datetime.timedelta(minutes=3))
        t_renew_0 = t_renew_1 - datetime.timedelta(minutes=10)
        datatime=[str(t_renew_0)[10:19], str(t_renew_1)[10:19]]

        import mysql.connector
        connect = mysql.connector.connect(user='root', password='sm4547634', host='127.0.0.1', database='hotspot', port='3306')
        cursor = connect.cursor()

        # 直近の更新時間のツイート数の取得
        query1 = 'select pointlat, pointlng, linear_expect from count_data where gettime = "'+str(t_renew_1)+'" order by linear_expect desc'
        cursor.execute(query1)

        # ツイート数の場所とツイート数が入った配列を作成
        count_data = []
        for column1 in cursor.fetchall():
            count_data.append(column1)

        # ツイート数が最大の場所の緯度、経度を取得
        latmax = Decimal(count_data[0][0])
        lngmax = Decimal(count_data[0][1])

        # ツイート数が最大の地域のツイートを取得(過去30分間)
        query2 = 'select * from tweets where created_at between "'+str(t_00)+'" and "'+str(t_1)+'" and lat between '+str(latmax)+'and '+str(latmax+lat_unit)+' and lng between '+str(lngmax)+'and '+str(lngmax+lng_unit)+'order by created_at desc'
        cursor.execute(query2)
        tweet_data_max = []
        for column2 in cursor.fetchall():
            tweet_data_max.append(column2)

        # 直近10分間のツイートを取得
        query3 = 'select * from tweets where created_at between "'+str(t_0)+'" and "'+str(t_1)+'"'
        cursor.execute(query3)
        tweet_data = cursor.fetchall()

        # リンクで表示する文章
        linkdata = ['今注目の場所のツイートへ切り替え', "../"]
        return render_template('direct_represent_web.html', tweet_data=tweet_data, tweet_data_max=tweet_data_max, datatime=datatime, count_data=count_data, linkdata=linkdata, markerpoint=[35.674436, 139.752848])

    except Exception as e:
                return e

@app.route('/marker/<latlng>')
def marker(latlng):
    # マーカーの座標を取得
    markerlat = latlng[:9]
    markerlng = latlng[9:]
    # htmlへ渡す用のマーカーの座標
    markerpoint = [markerlat, markerlng]
    # マーカーの座標を中心にするため刻み幅を半分にする
    lat_unit_half = lat_unit / Decimal(2)
    lng_unit_half = lng_unit / Decimal(2)
    # 取得する領域の下限と上限の設定
    markerlat_inf = Decimal(markerlat) - lat_unit_half
    markerlat_sup = Decimal(markerlat) + lat_unit_half
    markerlng_inf = Decimal(markerlng) - lng_unit_half
    markerlng_sup = Decimal(markerlng) + lng_unit_half

    try:

        # サイトの訪問時刻の取得
        t_1 = datetime.datetime.now()
        t_0 = t_1 - t_unit
        t_00 = t_1 - datetime.timedelta(minutes=30)
        # 直近の更新時間(集計時間の確保のため、分の一の位が3を超えたとき更新する)
        t_renew_1 = floar_minute_ten(t_1 - datetime.timedelta(minutes=3))
        t_renew_0 = t_renew_1 - datetime.timedelta(minutes=10)
        datatime=[str(t_renew_0)[10:19], str(t_renew_1)[10:19]]

        import mysql.connector
        connect = mysql.connector.connect(user='root', password='sm4547634', host='127.0.0.1', database='hotspot', port='3306')
        cursor = connect.cursor()

        # マーカーで指定した場所のツイートを取得(過去30分間)
        query2 = 'select * from tweets where created_at between "'+str(t_00)+'" and "'+str(t_1)+'" and lat between '+str(markerlat_inf)+'and '+str(markerlat_sup)+' and lng between '+str(markerlng_inf)+'and '+str(markerlng_sup)+'order by created_at desc'
        cursor.execute(query2)
        tweet_data_max = []
        for column2 in cursor.fetchall():
            tweet_data_max.append(column2)

        # 直近10分間のツイートを取得
        query3 = 'select * from tweets where created_at between "'+str(t_0)+'" and "'+str(t_1)+'"'
        cursor.execute(query3)
        tweet_data = cursor.fetchall()

        # リンクで表示する文章
        linkdata = ['今注目の場所のツイートへ切り替え', "../../"]
        return render_template('direct_represent_web.html', tweet_data=tweet_data, tweet_data_max=tweet_data_max, datatime=datatime, linkdata=linkdata, markerpoint=markerpoint)

    except Exception as e:
                return e

if __name__=="__main__":
 app.run(debug=True)
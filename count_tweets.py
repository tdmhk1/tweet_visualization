# 現在から10分前までさかのぼって、ツイート数を集計するプログラム
#  -- coding: utf-8 --

__author__ = 'Y.F'

import datetime
import mysql.connector
from decimal import *

# datetime型データを秒を0, ミリ秒をnullにして返す
def floar_seconds(s):
    return s.replace(second = 0, microsecond = 0)

# 領域の境界のイテレータの作成
def d_range(begin, end, step):
    n = begin
    while n < end:
        m = n + step
        yield [n, m]
        n = m

def main():
    # t_unit は、時間の刻み幅
    t_unit = datetime.timedelta(minutes=10)
    # 現在の時刻を取得
    # t_1 =datetime.datetime(2015, 1, 22, 1, 10, 0)
    t_1 = floar_seconds(datetime.datetime.now())
    t_0 = t_1 - t_unit

    # 緯度、経度は、decimal型で、小数第6位に丸めた
    # 緯度、経度の刻み幅を設定(だいたい1km四方の正方形となるようにとった)
    lat_unit = 0.008984
    lng_unit = 0.011040
    # 緯度、経度の境界の設定
    lat_inf = 35.616040
    lng_inf = 139.681088
    lat_sup = 35.732832
    lng_sup = 139.824608

    # sqlに格納されている代表点と比較するときの誤差の範囲
    error_range = 0.000010

    connect = mysql.connector.connect(user='root', password='sm4547634', host='127.0.0.1', database='hotspot', port='3306')
    cursor = connect.cursor(buffered=True)

    # 各ブロックにわたって集計をする
    for lat in d_range(begin=lat_inf, end=lat_sup, step=lat_unit):
        for lng in d_range(begin=lng_inf, end=lng_sup, step=lng_unit):
            # 1ブロックの集計結果をDBに格納する
            query1 = 'select count(*) from tweets where created_at between "'+str(t_0)+'" and "'+str(t_1)+'" and lat between '+str(lat[0])+' and '+str(lat[1])+'and lng between '+str(lng[0])+' and '+str(lng[1])
            cursor.execute(query1)
            # count は、現在から過去10分間に投稿されたツイート数
            count = cursor.fetchall()[0][0]
            query2 = 'select counts, difference from count_data where gettime = "'+str(t_0)+'" and pointlat between '+str(lat[0])+'-'+str(error_range)+' and '+str(lat[0])+'+'+str(error_range)+' and pointlng between '+str(lng[0])+'-'+str(error_range)+' and '+str(lng[0])+'+'+str(error_range)
            cursor.execute(query2)
            try:
                # countbは、20分前から10分前の間に投稿されたツイート数
                countb = cursor.description[0][1]
                countbb = cursor.description[1][1]
                # differenceは、現在と10分前のcountの差分
                difference = count - countb
                second_difference = difference - countbb
                linear_expect = count + difference
                second_expect = linear_expect + second_difference
            except IndexError:
                difference = "null"
                linear_expect = "null"
                second_difference = "null"
                second_expect = "null"

            # DBに集計結果を格納
            query3 = 'insert into count_data (gettime, pointlat, pointlng, counts, difference, second_difference, linear_expect, second_expect) values ("'+str(t_1)+'", '+str(lat[0])+', '+str(lng[0])+', '+str(count)+', '+str(difference)+', '+str(second_difference)+', '+str(linear_expect)+', '+str(second_expect)+')'
            cursor.execute(query3)
            connect.commit()

    cursor.close()
    connect.close()

if __name__ == '__main__':
    main()
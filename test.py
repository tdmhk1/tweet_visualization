# 日本のつぶやきを取得する
# -- coding: utf-8 --

__author__ = 'Y.F'

import twitter
import sys
import io
import json
import datetime
import mysql.connector

# 開発目的でTwitter APIにアクセスする
def oauth_login():
    CONSUMER_KEY = 'JciZvlRGhUtCnkf0Wj06TgWoS'
    CONSUMER_SECRET = 'vRAwp04jCvVQGrf90A9QOy8hBGIIV0Zn8baZIIeDi52jDWDmTk'
    ACCESS_TOKEN = '2919428545-uwA4xsbZvmeS4zZ2QLcRuztjbN1wapMjsGCoypy'
    ACCESS_TOKEN_SECRET = 'bvt43SKRzJ2k91qegD01YHFFuFxZmKSzsIABqgkDS0Lzk'

    auth = twitter.oauth.OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

# python から MySQL へデータを格納する
# コンフィグ の作成
config = {
'user': 'root',
'password': 'sm4547634',
'host': '127.0.0.1',
'database': 'twitter',
}
connect = mysql.connector.connect(**config)
cursor = connect.cursor()

# サンプルデータの作成
a = '3'
b = '13'
c = 'い'
d = '2014-12-22 15:46:00'
e = '103'

cursor.execute('insert into tweets values('+a+',' +b+ ',"' +c+ '","'+d + '",' +e+')')
cursor.close()
connect.close()


"""
# twitter.Twitterのインスタンスが返される
twitter_api = oauth_login()

# self.authパラメータのリファレンス
twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)

stream = twitter_stream.statuses.filter(locations='129.482881, 31.285110, 147.852021, 44.908014')

for tweet in stream:
    a = tweet['id_str']
    b = tweet['user']['id_str']
    c = tweet['text']
    d = tweet['created_at']
    e = tweet['retweet_count']

    #print(a+'\n'+b+'\n'+c+'\n'+d+'\n'+str(e)+'\n')
    #now = datetime.datetime.now()
    #print(now.strftime("%a %b %d %H:%M:%S %z %Y"))
    d = datetime.datetime.strptime(d, "%a %b %d %H:%M:%S %z %Y")
    print(str(d.year)+"-"+d.month+"-"+d.day+" "+d.hour+":"+d.minute+":"+d.second)
    #d = d.strftime("%Y-%m-%d %H:%M:%S")
    #d="2014-12-15 00:00:00"
    # MySQLへの操作
    cursor.execute('insert into tweets values('+a+',' +b+ ',"' +c+ '","'+d + '",' +e+')')
    #cursor.execute('insert into tweets values(123456,123456,"aaあ","2014-12-15 00:00:00",123456)')
    connect.commit()

    break

cursor.close()
connect.close()
"""




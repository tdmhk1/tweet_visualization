# -- coding: utf-8 --

__author__ = 'Y.F'

import twitter
import datetime
import mysql.connector

# 月から数字を取得(出力は文字列)
def MouthtoInt(s):
    dict = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
    return dict[s]

# UTC timeから、datetime型への変換(日本時間)
def UTCtoDatetime(s):
    t = datetime.datetime(int(s[26:]), MouthtoInt(s[4:7]), int(s[8:10]), int(s[11:13]), int(s[14:16]), int(s[17:19])) + datetime.timedelta(hours = 9)
    return t

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
    'database': 'hotspot',
}

connect = mysql.connector.connect(**config)
cursor = connect.cursor()

# twitter.Twitterのインスタンスが返される
twitter_api = oauth_login()

# self.authパラメータのリファレンス
twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)

# 東京23区内のツイートを取得する
stream = twitter_stream.statuses.filter(locations='139.681088, 35.616040, 139.824608, 35.732832')

for tweet in stream:

    try:
        # 各カラムのデータを取得
        TWEET_ID = str(tweet['id_str'])
        CREATED_AT = str(UTCtoDatetime(tweet['created_at']))
        LAT = str(tweet['coordinates']['coordinates'][1])
        LNG = str(tweet['coordinates']['coordinates'][0])
        TEXT = tweet['text']

        # 画像が含まれてるかどうかで条件分岐
        if 'media' in tweet['entities']:
            MEDIA_URL = str(tweet['entities']['media'][0]['media_url'])
            cursor.execute('insert into tweets(tweet_id, created_at, lat, lng, text, media_url) values('+TWEET_ID+', "'+CREATED_AT+'", '+LAT+', '+LNG+', "'+TEXT+'", "'+MEDIA_URL+'")')
        else:
            cursor.execute('insert into tweets(tweet_id, created_at, lat, lng, text) values('+TWEET_ID+', "'+CREATED_AT+'", '+LAT+', '+LNG+', "'+TEXT+'")')
        # DBに反映
        connect.commit()
    # 例外処理
    except KeyError:
        pass
    except TypeError:
        pass
    except mysql.connector.errors.ProgrammingError:
        pass

cursor.close()
connect.close()
# -- coding: utf-8 --

__author__ = 'Y.F'

import twitter
import sys
import io
import json
import datetime
import mysql.connector

# UTC time からdatetime への変換
def UTCtoDatetime(s):

    YEAR = s[26:]
    MOUTH = MouthtoInt(s[4:7])
    DAY = s[8:10]
    # 日本は世界標準時より９時間進んでいる
    TIME = WorldtoJst(s[11:19])
    t = YEAR+'-'+MOUTH+'-'+DAY+' '+TIME
    return t

# 月から数字を取得(出力は文字列)
def MouthtoInt(s):
    if s == 'Jan':
        return ('01')
    elif s == 'Feb':
        return('02')
    elif s == 'Mar':
        return('03')
    elif s == 'Apr':
        return('04')
    elif s == 'May':
        return('05')
    elif s == 'Jun':
        return('06')
    elif s == 'Jul':
        return('07')
    elif s == 'Aug':
        return('08')
    elif s == 'Sep':
        return('09')
    elif s == 'Oct':
        return('10')
    elif s == 'Nov':
        return('11')
    else:
        return('12')

# 世界標準時から日本時間に直す(９時間足す)
def WorldtoJst(s):
    h = (int(s[:2]) + 9) % 24
    i = str("{0:02d}".format(h))
    return s.replace(s[:2], i)

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

# twitter.Twitterのインスタンスが返される
twitter_api = oauth_login()

# self.authパラメータのリファレンス
twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)

# 日本のツイートを取得する
stream = twitter_stream.statuses.filter(locations='129.482881, 31.285110, 147.852021, 44.908014')

count = 0
for tweet in stream:

    # 各カラムのデータを取得
    TWEET_ID = str(tweet['id_str'])
    USER_ID = str(tweet['user']['id_str'])
    TEXT = tweet['text']
    CREATED_AT = UTCtoDatetime(tweet['created_at'])
    RETWEETED_COUNT = str(tweet['retweet_count'])

    # SQL文の実行
    cursor.execute('insert into tweets values('+TWEET_ID+', '+USER_ID+', "'+TEXT+'", "'+CREATED_AT+'", '+RETWEETED_COUNT+')')
    # DBに反映
    connect.commit()

    count += 1
    if count > 100:
        break

cursor.close()
connect.close()




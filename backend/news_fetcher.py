#!/usr/bin/env python
# -*- coding:utf8 -*-
import feedparser
import re
import MySQLdb
import datetime
import sys


# Google News 臺灣版 RSS URL
google_news_rss_url = 'https://news.google.com.tw/news/feeds?cf=all&ned=tw&hl=zh-TW&output=rss&num=100'
feedparser.USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:35.0) Gecko/20100101 Firefox/35.0"
feed = feedparser.parse(google_news_rss_url)
reload(sys)
sys.setdefaultencoding('utf8')

for item in feed["items"]:
    title = re.findall(r'(.*?)\s+-\s+(.*?)$', item['title'])
    topic = title[0][0]
    publisher = title[0][1]
    url = re.findall(r'url=(.*)$', item['link'])

    # 把 HTML tag 去掉
    desc = re.sub('<[^<]+?>', '', item['description'])
    desc = re.sub('\'', '', desc)

    # date format: Fri, 05 Dec 2014 04:42:42 GMT
    published_date = datetime.datetime.strptime(item['published'],'%a, %d %b %Y %H:%M:%S %Z')
    t = published_date + datetime.timedelta(hours=8)

    conn = MySQLdb.connect(host="127.0.0.1", user="keywordcloud", passwd="keywordcloud", db="keywordcloud")
    conn.set_character_set('UTF8')
    c = conn.cursor()
    c.execute('SET NAMES UTF8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    # 檢查 publisher 是否存在
    sql = "SELECT COUNT(*) FROM publisher_publisher WHERE name='%s'" % (publisher)
    c.execute(sql)
    for row in c.fetchall():
        for r in row:
            # 如果是未知 publisher ，就寫進資料庫
            if r == 0:
                sql = "INSERT INTO publisher_publisher(name) VALUES('%s')" % (publisher)
                c.execute(sql)

            # 取得 publisher 的 id
            sql = "SELECT id FROM publisher_publisher WHERE name='%s'" % (publisher)
            c.execute(sql)
            fkid = 0
            for row in c.fetchall():
                for r in row:
                    fkid = r

            # 檢查此標題是否已存在，若存在就不寫入資料庫
            sql = "SELECT COUNT(*) FROM news_news WHERE topic = '%s'" % topic
            c.execute(sql)
            for row in c.fetchall():
                for r in row:
                    if r == 0:
                        sql = "INSERT INTO news_news(topic,url,publisher_id,description,pub_time,f_cutted) VALUES ('%s','%s','%s','%s','%s', 0)" % (topic,url[0],fkid,desc,t)
                        c.execute(sql)
                        print u"Insert topic: %s" % (topic)
                    else:
                        print u"Duplicate topic: %s" % (topic)

    conn.commit()
    conn.close()

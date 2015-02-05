#!/usr/bin/env python
#coding:utf8-*-
import getopt
import jieba
import jieba.posseg as pseg
import MySQLdb
import sys
import time


conn = MySQLdb.connect(host="127.0.0.1", user="keywordcloud", passwd="keywordcloud", db="keywordcloud")
conn.set_character_set('UTF8')
c = conn.cursor()
c.execute("SET NAMES UTF8;")
c.execute("SET CHARACTER SET utf8;")
c.execute("SET character_set_connection=utf8;")

# 把字串忽略清單載入到 list 中並回傳
def load_ignore_list(ignore_list_file):
    tmp_list = []
    with open(ignore_list_file) as f:
        for line in f.readlines():
            if line != "":
                tmp_list.append(line.strip())

    f.close()
    return tmp_list


# 將切出來的 segment list 寫入資料庫
def word2db(seglist, index):
    sql = "INSERT INTO words_words (word, count, wordtype, parse_time, news_id_id) VALUES"
    for t in seglist:
        # 如果該詞不在忽略清單中才寫入 DB
        if t.word.encode('utf-8').strip() not in _ignore_list:
            sys.stdout.write("[1;32m%s [0m" % (t.word.encode('utf-8'))),
            sys.stdout.flush()
            sql = sql + "('%s', '%s', '%s', '%s', '%s')," % (t.word.encode('utf-8'), 1, t.flag, time.strftime("%Y-%m-%d %H:%M:%S"), index)
        else:
            sys.stdout.write("[0;30m%s [0m" % (t.word.encode('utf-8'))),
            sys.stdout.flush()
    sql = sql[:-1]
    if _dryrun != 1:
        c.execute(sql)
        conn.commit()


def main(argv):
    global _dryrun
    global _day
    global _ignore_list

    _yesterday = 0
    _dryrun = 0
    _day = 0
    count = 0

    _ignore_list = load_ignore_list("ignore_list.txt")

    # 處理　CLI argumets
    try:
        opts, args = getopt.getopt(argv, "c:d", ["count=", "dry", "day="])
    except:
        sys.exit(2)

    for o, a in opts:
        if o in ("-c", "--count"):
            count = a
        if o in ("-d", "--dry"):
            _dryrun = 1
            print "[33;41m      DRY RUN MODE, NOTHING'S GOING TO WRITE TO DATABASE      [0m"
        if o in ("--day"):
            print a;
            _day = a

    jieba.load_userdict('custom_dict.txt')
    #設定斷詞引擎平行處理
    #jieba.enable_parallel(2)

    if count != 0:
        sql = "SELECT id, topic, url, description FROM news_news WHERE f_cutted != 1 AND date(pub_time) = date(now()) - %s ORDER BY pub_time DESC LIMIT %s;" % (_day, count)
    else:
        sql = "SELECT id, topic, url, description FROM news_news WHERE f_cutted != 1 AND date(pub_time) = date(now()) - %s ORDER BY pub_time DESC;" % (_day)

    c.execute(sql)

    for row in c.fetchall():
        idx = row[0]
        topic = row[1]
        content = row[3]

        # 處理新聞內容
        content_seglist = pseg.cut("%s" % (content))
        word2db(content_seglist, idx)

        # set the news to cutted
        sql = "UPDATE news_news SET f_cutted = 1 WHERE id='%s'" % (idx)
        if _dryrun != 1:
            c.execute(sql)
            conn.commit()

    c.close()
    conn.close()


if __name__ == "__main__":
    main(sys.argv[1:])

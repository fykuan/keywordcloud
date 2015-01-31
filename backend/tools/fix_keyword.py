#!/usr/bin/env python
#-*-coding: utf8 -*-
import sys
import MySQLdb


def main(arguments):
    wrong_keyword = raw_input('Please input the wrong keyword to find: ')

    sql = "SELECT * FROM news WHERE description LIKE '%%%s%%';" % (wrong_keyword)
    conn = MySQLdb.connect(host="127.0.0.1", user="news_fetcher", passwd="news_fetcher", db="news_fetcher")
    conn.set_character_set('UTF8')
    c = conn.cursor()
    c.execute('SET NAMES UTF8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    c.execute(sql)
    for row in c.fetchall():
        print "#"
        print row[4]

    right_keyword = raw_input('Please enter the correct keyword: ')

    sql = "UPDATE words SET word='%s' WHERE news_id IN (SELECT id FROM news WHERE description LIKE '%%%s%%') AND word='%s';" % (right_keyword, right_keyword, wrong_keyword)
    try:
        c.execute(sql)
    except Exception as e:
        print e
    else:
        custom_dict = open("../custom_dict.txt", "a")
        custom_dict.write("%s 10\n" % (right_keyword))
    conn.commit()
    c.close()
    conn.close()


if __name__ == "__main__":
    main(sys.argv[1:])

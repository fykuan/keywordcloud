#!/usr/bin/env python
#-*-coding: utf8-*-
import urllib2
import sys
import argparse
import json

"""
在 CLI 中取得熱門關鍵字列表
"""

def get_keyword(arguments):
    parser = argparse.ArgumentParser(description='Show keywords from remote JSON')
    parser.add_argument('-u', '--url', help='specify url', required=True, action='store')
    args = parser.parse_args(arguments)

    data = urllib2.urlopen(args.url)
    dataList = json.JSONDecoder().decode(data.read())

    for line in dataList:
        print "%s(%s)" % (line['word'], line['c']),


if __name__ == "__main__":
    get_keyword(sys.argv[1:])

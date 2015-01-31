from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.http import HttpResponse
from words.models import words
import json
import decimal

# Create your views here.
def get(request):
    sql = "SELECT word, count(*) AS c, id FROM words_words WHERE (wordtype LIKE 'nr%%' OR wordtype='x' OR wordtype='ns' OR wordtype='nrt' OR wordtype='eng') AND char_length(word) >= 2 AND parse_time > NOW() - INTERVAL 1 DAY GROUP BY word ORDER BY c DESC LIMIT 300;"
    wordlist = words.objects.raw(sql)

    # Defian an empty array, we'll convert this array to JSON object and return later.
    arr = []

    for item in wordlist:
        lst = [item.word, item.c]
        arr.append(lst)

    return HttpResponse(json.dumps(arr), content_type="application/json")


def getTrend(request, keyword):
    sql = u"SELECT t, t1.c AS c, t1.c/t2.c*100 AS r, t2.id FROM (SELECT date(pub_time) AS t, COUNT(*) AS c FROM (SELECT * FROM news_news where description like '%%" + keyword + "%%' AND date(pub_time) > now() - INTERVAL 8 day AND date(pub_time) <= now() - INTERVAL 1 day) as t GROUP BY date(pub_time)) t1 RIGHT JOIN (SELECT date(pub_time) AS d, count(*) AS c, id FROM news_news WHERE date(pub_time) > now() - INTERVAL 8 DAY AND date(pub_time) <= now() - INTERVAL 1 day GROUP BY date(pub_time)) t2 ON t1.t = t2.d"
    print sql
    wordTrend = words.objects.raw(sql)

    arr = []

    for item in wordTrend:
        item.t = str(item.t)
        item.r = str(item.r)
        item.c = str(item.c)
        lst = [item.t, item.c, item.r]
        arr.append(lst)

    print arr
    return HttpResponse(json.dumps(arr), content_type="application/json")

def trend(request, keyword):
    template = loader.get_template('home/trend.html')
    context = RequestContext(request, {
            'keyword': keyword
        })
    return HttpResponse(template.render(context))


def index(request):
    template = loader.get_template('home/index.html')
    context = RequestContext(request, {
        })
    return HttpResponse(template.render(context))
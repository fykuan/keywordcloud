from django.db import models
# Create your models here.
class words(models.Model):
    word = models.CharField(max_length=256)
    count = models.IntegerField(default=0)
    wordtype = models.CharField(max_length=10)
    parse_time = models.DateTimeField()
    news_id = models.ForeignKey('news.news')

    def relatedNew(self, obj):
        return '%s' % (obj.news_id_id.topic)

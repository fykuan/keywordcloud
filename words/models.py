from django.db import models
# Create your models here.
class words(models.Model):
    word = models.CharField(max_length=256)
    wordtype = models.CharField(max_length=10)
    parse_time = models.DateTimeField()
    news_id = models.ForeignKey('news.news', on_delete=models.CASCADE)

    def relatedNew(self, obj):
        return '%s' % (obj.news_id_id.topic)

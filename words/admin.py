from django.contrib import admin
from words.models import words

# Register your models here.
class wordsAdmin(admin.ModelAdmin):
    list_display = ['word', 'parse_time', 'relatedNews']
    ordering = ['-parse_time']

    def relatedNews(self, obj):
        return '%s' % (obj.news_id.topic)

admin.site.register(words, wordsAdmin)
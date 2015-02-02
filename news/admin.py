from django.contrib import admin
from news.models import news

# Register your models here.
class newsAdmin(admin.ModelAdmin):
    list_display = ['topic', 'pub_time']
    ordering = ['-pub_time']

admin.site.register(news, newsAdmin)
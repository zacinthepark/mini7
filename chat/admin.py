from django.contrib import admin
from .models import History

class HistoryAdmin(admin.ModelAdmin):
    ordering = ['chat_time']
    search_fields = ['query', 'answer']
    list_per_page = 10

admin.site.register(History, HistoryAdmin)

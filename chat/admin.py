from django.contrib import admin
from .models import History

class HistoryAdmin(admin.ModelAdmin):
    list_display = ['chat_time', 'query', 'answer']
    list_display_links = ['query']
    ordering = ['chat_time']
    search_fields = ['query', 'answer']
    list_per_page = 10
    
    fieldsets = (
        ('Q&A 내용', {'fields':('query', 'answer', 'chat_time')}),
        ('Sim_score', {'fields':('sim1', 'sim2', 'sim3')}),
    )
    
admin.site.register(History, HistoryAdmin)
from django.contrib import admin
from .models import Analysis

@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ['user', 'about', 'type', 'period_start', 'period_end', 'created_at']
    list_filter = ['about', 'type', 'created_at']
    search_fields = ['user__username', 'user__email', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('user', 'about', 'type')
        }),
        ('기간 설정', {
            'fields': ('period_start', 'period_end')
        }),
        ('분석 내용', {
            'fields': ('description', 'result_image')
        }),
        ('시스템 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
       list_display = ('id', 'notification_type', 'title', 'created_at')
       list_filter = ('notification_type',)
from django.urls import path
from .views import UnreadNotificationListView, NotificationReadView

app_name = 'notification'

urlpatterns = [
    path('unread/', UnreadNotificationListView.as_view(), name='unread-list'),
    path('<int:pk>/read/', NotificationReadView.as_view(), name='read'),
]
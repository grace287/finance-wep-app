from django.urls import path
from .views import AnalysisListView

app_name = 'analysis'

urlpatterns = [
    path('', AnalysisListView.as_view(), name='analysis-list'),
]
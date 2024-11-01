from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    # 거래내역 CRUD
    path('', views.TransactionListView.as_view(), name='transaction-list'),
    path('create/', views.TransactionCreateView.as_view(), name='transaction-create'),
    path('<int:pk>/', views.TransactionDetailView.as_view(), name='transaction-detail'),
    path('<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction-delete'),
]
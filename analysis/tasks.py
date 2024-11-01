from celery import shared_task
from django.contrib.auth import get_user_model
from .analyzers import TransactionAnalyzer

User = get_user_model()

@shared_task
def create_weekly_analysis():
    for user in User.objects.all():
        analyzer = TransactionAnalyzer(user, 'WEEKLY', 'EXPENSE')
        analyzer.analyze()

@shared_task
def create_monthly_analysis():
    for user in User.objects.all():
        analyzer = TransactionAnalyzer(user, 'MONTHLY', 'EXPENSE')
        analyzer.analyze()
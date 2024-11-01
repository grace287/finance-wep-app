from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Analysis
from notification.models import Notification

@receiver(post_save, sender=Analysis)
def create_analysis_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            message=f"새로운 분석 결과가 생성되었습니다. ({instance.start_date} ~ {instance.end_date})"
        ) 
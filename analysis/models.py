from django.db import models
from django.conf import settings

class Analysis(models.Model):
    ANALYSIS_TYPES = [
        ('WEEKLY', '주간'),
        ('MONTHLY', '월간'),
    ]
    
    ANALYSIS_ABOUT = [
        ('EXPENSE', '지출'),
        ('INCOME', '수입'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='analyses'
    )
    about = models.CharField(max_length=20, choices=ANALYSIS_ABOUT)
    type = models.CharField(max_length=20, choices=ANALYSIS_TYPES)
    period_start = models.DateField()
    period_end = models.DateField()
    description = models.TextField()
    result_image = models.ImageField(
        upload_to='analysis_results/%Y/%m/%d/'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'analyses'

    def __str__(self):
        return f"{self.user.username}의 {self.get_type_display()} {self.get_about_display()} 분석"
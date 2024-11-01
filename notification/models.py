from django.db import models

class Notification(models.Model):
       NOTIFICATION_TYPES = (
           ('info', 'Information'),
           ('warning', 'Warning'),
           ('error', 'Error'),
       )

       notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
       title = models.CharField(max_length=255)
       message = models.TextField()
       created_at = models.DateTimeField(auto_now_add=True)

       def __str__(self):
           return self.title
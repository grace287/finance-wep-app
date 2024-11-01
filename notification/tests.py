from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

class NotificationAPITest(APITestCase):
    def setUp(self):
        """테스트 데이터 설정"""
        # 테스트 사용자 생성
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # 테스트 알림 생성
        self.notifications = []
        for i in range(3):
            notification = Notification.objects.create(
                user=self.user,
                notification_type='SYSTEM',
                title=f'Test Notification {i+1}',
                message=f'Test message {i+1}',
                is_read=False
            )
            self.notifications.append(notification)
        
        # 이미 읽은 알림 하나 추가
        self.read_notification = Notification.objects.create(
            user=self.user,
            notification_type='SYSTEM',
            title='Read Notification',
            message='Already read',
            is_read=True
        )
    
    def test_list_unread_notifications(self):
        """미확인 알림 목록 조회 테스트"""
        url = reverse('notification:notification-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        
        # 읽은 알림은 포함되지 않아야 함
        notification_ids = [n['id'] for n in response.data['results']]
        self.assertNotIn(self.read_notification.id, notification_ids)
    
    def test_mark_notification_as_read(self):
        """단일 알림 읽음 처리 테스트"""
        notification = self.notifications[0]
        url = reverse('notification:mark-as-read', kwargs={'pk': notification.id})
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # DB에서 알림 상태 확인
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)
    
    def test_mark_all_notifications_as_read(self):
        """모든 알림 읽음 처리 테스트"""
        url = reverse('notification:mark-all-as-read')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 모든 알림이 읽음 처리되었는지 확인
        unread_count = Notification.objects.filter(
            user=self.user,
            is_read=False
        ).count()
        self.assertEqual(unread_count, 0)
    
    def test_mark_already_read_notification(self):
        """이미 읽은 알림 처리 테스트"""
        url = reverse('notification:mark-as-read', 
                     kwargs={'pk': self.read_notification.id})
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_unauthorized_access(self):
        """미인증 사용자 접근 테스트"""
        self.client.force_authenticate(user=None)
        url = reverse('notification:notification-list')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_mark_other_user_notification(self):
        """다른 사용자의 알림 접근 테스트"""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        
        other_notification = Notification.objects.create(
            user=other_user,
            notification_type='SYSTEM',
            title='Other User Notification',
            message='Test message',
            is_read=False
        )
        
        url = reverse('notification:mark-as-read', 
                     kwargs={'pk': other_notification.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
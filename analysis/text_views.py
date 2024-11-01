from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from ..models import Analysis
from ..analyzers import TransactionAnalyzer

User = get_user_model()

class AnalysisListViewTest(APITestCase):
    def setUp(self):
        # 테스트 사용자 생성
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # 테스트 데이터 생성
        self.today = timezone.now().date()
        
        # 주간 분석 데이터
        Analysis.objects.create(
            user=self.user,
            about='TOTAL_EXPENSE',
            type='WEEKLY',
            period_start=self.today - timedelta(days=7),
            period_end=self.today,
            description='주간 지출 분석'
        )
        
        # 월간 분석 데이터
        Analysis.objects.create(
            user=self.user,
            about='CATEGORY_EXPENSE',
            type='MONTHLY',
            period_start=self.today.replace(day=1),
            period_end=self.today,
            description='월간 카테고리별 지출 분석'
        )
        
    def test_get_analysis_list_authenticated(self):
        """인증된 사용자의 분석 목록 조회 테스트"""
        url = reverse('analysis:analysis-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_get_analysis_list_unauthenticated(self):
        """미인증 사용자의 분석 목록 조회 테스트"""
        self.client.force_authenticate(user=None)
        url = reverse('analysis:analysis-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_filter_by_type(self):
        """분석 유형별 필터링 테스트"""
        url = reverse('analysis:analysis-list')
        response = self.client.get(url, {'type': 'WEEKLY'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['type'], 'WEEKLY')
        
    def test_filter_by_about(self):
        """분석 대상별 필터링 테스트"""
        url = reverse('analysis:analysis-list')
        response = self.client.get(url, {'about': 'TOTAL_EXPENSE'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['about'], 'TOTAL_EXPENSE')
        
    def test_filter_by_date_range(self):
        """기간별 필터링 테스트"""
        url = reverse('analysis:analysis-list')
        params = {
            'start_date': (self.today - timedelta(days=7)).strftime('%Y-%m-%d'),
            'end_date': self.today.strftime('%Y-%m-%d')
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)
        
    def test_invalid_date_format(self):
        """잘못된 날짜 형식 테스트"""
        url = reverse('analysis:analysis-list')
        response = self.client.get(url, {
            'start_date': 'invalid-date',
            'end_date': 'invalid-date'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)  # 날짜 필터 무시됨
        
    def test_empty_result(self):
        """결과가 없는 경우 테스트"""
        Analysis.objects.all().delete()
        url = reverse('analysis:analysis-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
        self.assertEqual(response.data['message'], '해당 조건의 분석 결과가 없습니다.')
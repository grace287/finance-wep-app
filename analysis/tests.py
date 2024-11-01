from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Analysis
from .analyzers import TransactionAnalyzer
from transaction_history.models import Transaction
from datetime import datetime, timedelta

User = get_user_model()

class AnalyzerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # 테스트용 거래 내역 생성
        self.create_test_transactions()

    def create_test_transactions(self):
        # 테스트용 거래 내역 생성 로직
        pass

    def test_analyzer_creates_analysis(self):
        analyzer = TransactionAnalyzer(self.user, 'WEEKLY', 'EXPENSE')
        analysis = analyzer.analyze()
        
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis.user, self.user)
        self.assertEqual(analysis.type, 'WEEKLY')
        self.assertTrue(analysis.result_image)

class AnalysisAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # 테스트용 분석 데이터 생성
        self.analysis = Analysis.objects.create(
            user=self.user,
            about='EXPENSE',
            type='WEEKLY',
            period_start=datetime.now().date(),
            period_end=datetime.now().date() + timedelta(days=7),
            description='Test Analysis'
        )
        # 테스트 이미지 추가
        self.analysis.result_image.save(
            'test.png',
            ContentFile(b'test-image-content')
        )

    def test_list_analysis(self):
        response = self.client.get('/api/analysis/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_type(self):
        response = self.client.get('/api/analysis/?type=WEEKLY')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
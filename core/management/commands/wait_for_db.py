import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2OpError

class Command(BaseCommand):
    """데이터베이스가 사용 가능할 때까지 대기하는 Django 커맨드"""

    def handle(self, *args, **options):
        """커맨드의 메인 핸들러"""
        self.stdout.write('데이터베이스 연결 대기 중...')
        
        for attempt in range(10):
            try:
                connection = connections['default']
                connection.ensure_connection()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'데이터베이스 연결 성공! (시도 {attempt + 1}회)'
                    )
                )
                return
                
            except (Psycopg2OpError, OperationalError):
                if attempt == 9:
                    self.stdout.write(
                        self.style.ERROR(
                            f'데이터베이스 연결 실패 (10회 시도 후 실패)'
                        )
                    )
                    raise
                    
                self.stdout.write(
                    self.style.WARNING(
                        f'데이터베이스 연결 실패 (시도 {attempt + 1}회) - 재시도 중...'
                    )
                )
                time.sleep(1)
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from django.core.files.base import ContentFile
import io
from transaction_history.models import Transaction

class TransactionAnalyzer:
    def __init__(self, user, analysis_type, about):
        self.user = user
        self.analysis_type = analysis_type
        self.about = about
        
    def get_period_dates(self):
        today = datetime.now().date()
        if self.analysis_type == 'WEEKLY':
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        else:  # MONTHLY
            start_date = today.replace(day=1)
            next_month = today.replace(day=28) + timedelta(days=4)
            end_date = next_month - timedelta(days=next_month.day)
        return start_date, end_date

    def get_transactions(self, start_date, end_date):
        return Transaction.objects.filter(
            account__user=self.user,
            created_at__date__range=(start_date, end_date)
        )

    def create_dataframe(self, transactions):
        data = {
            'date': [t.created_at.date() for t in transactions],
            'amount': [t.amount for t in transactions],
        }
        return pd.DataFrame(data)

    def create_plot(self, df):
        plt.figure(figsize=(10, 6))
        plt.plot(df['date'], df['amount'], marker='o')
        plt.title(f"{self.get_type_display()} {self.get_about_display()} 분석")
        plt.xlabel('날짜')
        plt.ylabel('금액')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # 이미지를 바이트 스트림으로 저장
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        
        return buffer

    def analyze(self):
        start_date, end_date = self.get_period_dates()
        transactions = self.get_transactions(start_date, end_date)
        df = self.create_dataframe(transactions)
        
        if df.empty:
            return None
            
        plot_buffer = self.create_plot(df)
        
        from .models import Analysis
        analysis = Analysis.objects.create(
            user=self.user,
            about=self.about,
            type=self.analysis_type,
            period_start=start_date,
            period_end=end_date,
            description=f"{start_date}부터 {end_date}까지의 {self.get_about_display()} 분석"
        )
        
        analysis.result_image.save(
            f'analysis_{self.user.id}_{datetime.now().strftime("%Y%m%d")}.png',
            ContentFile(plot_buffer.getvalue())
        )
        
        return analysis
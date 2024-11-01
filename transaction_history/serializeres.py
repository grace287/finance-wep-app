from rest_framework import serializers
from .models import Transaction
from accounts.models import Account

class TransactionSerializer(serializers.ModelSerializer):
    account_number = serializers.SerializerMethodField()
    
    class Meta:
        model = Transaction
        fields = ['id', 'account', 'account_number', 'transaction_type', 
                 'amount', 'description', 'balance_after_transaction', 
                 'created_at']
        read_only_fields = ['balance_after_transaction']

    def get_account_number(self, obj):
        """마스킹된 계좌번호 반환"""
        num = obj.account.account_number
        return f"{num[:-4]}****"

    def validate(self, attrs):
        account = attrs['account']
        amount = attrs['amount']
        transaction_type = attrs['transaction_type']

        # 본인 계좌인지 확인
        if account.user != self.context['request'].user:
            raise serializers.ValidationError("본인의 계좌만 사용할 수 있습니다.")

        # 출금 시 잔액 검증
        if transaction_type == 'WITHDRAWAL' and account.balance < amount:
            raise serializers.ValidationError({
                "insufficient_balance": "잔액이 부족합니다."
            })

        return attrs

    def create(self, validated_data):
        account = validated_data['account']
        amount = validated_data['amount']
        transaction_type = validated_data['transaction_type']

        # 거래 처리
        if transaction_type == 'DEPOSIT':
            account.balance += amount
        else:  # WITHDRAWAL
            account.balance -= amount

        account.save()
        validated_data['balance_after_transaction'] = account.balance
        
        return super().create(validated_data)
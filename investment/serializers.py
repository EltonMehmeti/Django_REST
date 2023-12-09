from rest_framework import serializers
from investment.models import CashFlow, Loan


class CashFlowSerializer(serializers.ModelSerializer):

    class Meta:
        model = CashFlow
        fields = "__all__"


class LoanSerializer(serializers.ModelSerializer):
    cash_flows = CashFlowSerializer(many=True, read_only=True)

    class Meta:
        model = Loan
        fields = "__all__"



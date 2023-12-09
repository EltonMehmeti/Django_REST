from django.db import models

# Create your models here.
from django.db.models import Sum
from datetime import datetime


class Loan(models.Model):
    loan_id = models.CharField(primary_key=True, max_length=255)
    investment_date = models.DateField()
    maturity_date = models.DateField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.loan_id

    def get_realized_amount(self, reference_date):
        try:
            repayments = self.cash_flows.filter(
                cashflow_date__lte=reference_date, cashflow_type="repayment"
            )
            return repayments.aggregate(Sum("amount"))["amount__sum"] or 0
        except Exception as e:
            print(f"Error in get_realized_amount: {str(e)}")
            return 0

    def get_gross_expected_amount(self, reference_date_str):
        try:
            reference_date = datetime.strptime(reference_date_str, "%Y-%m-%d").date()
            invested_amount = abs(
                self.cash_flows.filter(cashflow_type="funding").aggregate(
                    Sum("amount")
                )["amount__sum"]
                or 0
            )
            daily_interest_rate = self.interest_rate / 365
            daily_interest_amount = invested_amount * daily_interest_rate
            passed_days = (reference_date - self.investment_date).days
            gross_expected_interest_amount = daily_interest_amount * passed_days
            gross_expected_amount = invested_amount + gross_expected_interest_amount
            return gross_expected_amount

        except Exception as e:
            print(f"Error in get_gross_expected_amount: {str(e)}")
            return 0

    def get_remaining_invested_amount(self, reference_date):
        try:
            invested_amount = abs(
                self.cash_flows.filter(cashflow_type="funding").aggregate(
                    Sum("amount")
                )["amount__sum"]
                or 0
            )
            return invested_amount - self.get_realized_amount(reference_date)
        except Exception as e:
            print(f"Error in get_remaining_invested_amount: {str(e)}")
            return 0

    def get_closing_date(self):
        try:
            cash_flows_list = list(self.cash_flows.all())
            for cashflow in cash_flows_list:
                gross_expected_amount = self.get_gross_expected_amount(str(self.maturity_date))
                if cashflow.cashflow_type == "repayment":
                    realized_amount = self.get_realized_amount(cashflow.cashflow_date)
                    if realized_amount >= gross_expected_amount:
                        return f"{cashflow.cashflow_date} with the last repayment amount of {cashflow.amount} {cashflow.cashflow_currency}"

            return "Loan Not Closed!"

        except Exception as e:
            raise Exception(f"Error in get_closing_date: {str(e)}")


class CashFlow(models.Model):
    cashflow_id = models.CharField(primary_key=True, max_length=255)
    loan = models.ForeignKey(Loan, related_name="cash_flows", on_delete=models.CASCADE)
    cashflow_date = models.DateField()
    cashflow_currency = models.CharField(max_length=3)
    cashflow_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.cashflow_id


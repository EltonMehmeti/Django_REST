from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import pandas as pd
from .serializers import LoanSerializer, CashFlowSerializer
from investment.models import Loan, CashFlow
from datetime import datetime
from rest_framework import viewsets
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from io import BytesIO
import openpyxl
class CustomLoanPagination(PageNumberPagination):
    page_size =  10
    page_size_query_param = 'page_size'
    max_page_size = 100
class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    pagination_class = CustomLoanPagination

class CashFlowViewSet(viewsets.ModelViewSet):
    queryset = CashFlow.objects.all()
    serializer_class = CashFlowSerializer
    pagination_class = CustomLoanPagination

class LoanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    lookup_field = 'loan_id'  # Specify the field to use for the lookup

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CashFlowDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CashFlow.objects.all()
    serializer_class = CashFlowSerializer
    lookup_field = 'cashflow_id'  # Specify the field to use for the lookup

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
class LoanUploadView(APIView):

    parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file, engine='openpyxl')

            with transaction.atomic():
                for _, row in df.iterrows():
                    loan = self.process_loan_data(row)

                    if not loan:
                        return Response({"error": "Error processing file"},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    loan.save()

            return Response({"message": "File uploaded successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Error processing file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def process_loan_data(self, row):
        try:
            interest_rate = float(row['interest_rate'].replace('%', '')) / 100.0
            investment_date, maturity_date = self.parse_dates(row['investment_date'], row['maturity_date'])

            if not investment_date or not maturity_date:
                raise ValueError("Invalid date format")

            return Loan(
                loan_id=row['loan_id'],
                investment_date=investment_date,
                maturity_date=maturity_date,
                interest_rate=interest_rate
            )

        except ValueError:
            return None
        
    def parse_dates(self, investment_date_str, maturity_date_str):
        date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]

        for date_format in date_formats:
            try:
                investment_date = datetime.strptime(investment_date_str, date_format).strftime("%Y-%m-%d")
                maturity_date = datetime.strptime(maturity_date_str, date_format).strftime("%Y-%m-%d")
                return investment_date, maturity_date

            except ValueError:
                pass

        return None, None

class CashFlowUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file, engine='openpyxl')

            with transaction.atomic():
                for _, row in df.iterrows():
                    cash_flow = self.process_cash_flow_data(row)

                    if not cash_flow:
                        return Response({"error": "Error processing file"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    cash_flow.save()

                return Response({"message": "File uploaded successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Error processing file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def process_cash_flow_data(self, row):
        try:
            date_str = row['cashflow_date']
            date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]
            date = None

            for date_format in date_formats:
                try:
                    date = datetime.strptime(date_str, date_format).strftime("%Y-%m-%d")
                    break
                except ValueError:
                    pass

            if date is None:
                raise ValueError(f"Invalid date format: {date_str}")

            loan_id = row['loan_id']
            loan = Loan.objects.get(loan_id=loan_id)

            return CashFlow(
                cashflow_id=row['cashflow_id'],
                cashflow_date=date,
                cashflow_currency=row['cashflow_currency'],
                cashflow_type=row['cashflow_type'],
                amount=row['amount'].replace(',', ''),
                loan=loan
            )

        except (ValueError, Loan.DoesNotExist):
            return None


class RealizedAmountView(APIView):
    def post(self, request, loan_id, *args, **kwargs):
        loan = Loan.objects.get(loan_id=loan_id)
        reference_date = request.data.get('reference_date', '2023-12-04')
        realized_amount = loan.get_realized_amount(reference_date)
        return Response({"realized_amount": realized_amount}, status=status.HTTP_200_OK)

class GrossExpectedAmountView(APIView):
    def post(self, request, loan_id, *args, **kwargs):
        loan = Loan.objects.get(loan_id=loan_id)
        reference_date = request.data.get('reference_date', '2023-12-04')
        gross_expected_amount = loan.get_gross_expected_amount(reference_date)
        return Response({"gross_expected_amount": gross_expected_amount}, status=status.HTTP_200_OK)

class RemainingInvestedAmountView(APIView):
    def post(self, request, loan_id, *args, **kwargs):
        loan = Loan.objects.get(loan_id=loan_id)
        reference_date = request.data.get('reference_date', '2023-12-04')
        remaining_invested_amount = loan.get_remaining_invested_amount(reference_date)
        return Response({"remaining_invested_amount": remaining_invested_amount}, status=status.HTTP_200_OK)


class ClosingDateView(APIView):
    def get(self, request, loan_id, *args, **kwargs):
        try:
            # Fix the typo here: change `laon_id` to `loan_id`
            loan = Loan.objects.get(loan_id=loan_id)
            closing_date = loan.get_closing_date()
            return Response(closing_date, status=status.HTTP_200_OK)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExportLoansCSV(APIView):
    def get(self, request, *args, **kwargs):
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans, many=True)
        data = serializer.data
        df = pd.DataFrame(data)
        csv_buffer = df.to_csv(index=False)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="loans_data.csv"'
        response.write(csv_buffer)

        return response


class ExportCashflowsCSV(APIView):
    def get(self, request, *args, **kwargs):
        cashflows = CashFlow.objects.all()
        serializer = CashFlowSerializer(cashflows, many=True)
        data = serializer.data
        df = pd.DataFrame(data)
        csv_buffer = df.to_csv(index=False)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="cashflows_data.csv"'
        response.write(csv_buffer)
        return response
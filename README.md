# Django_REST

Elton Mehmeti

First off execute the docker command to run the container: 
docker-compose up --build
Secondly you need to upload the data of loans and cashflows:
 Loan upload:
  HTTP method: POST
  http://localhost:8000/investment/api/loan/upload/
  Body-form-data:
  key:file,  value:trades.xlsx
Cashflow upload:
  HTTP method: POST
  http://localhost:8000/investment/api/cashflow/upload/
  Body-form-data:
  key:file,  value:cash_flows.xlsx
!Didn't use authentication for the sake of simplicity!
if you want to check all the loans:
one feature to mention is pagination
http://localhost:8000/investment/loans/
All cashflows:
http://localhost:8000/investment/cashflows/
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Loan id example: 10229_AA_2231940
HTTP method: GET
You can check loan details like this: http://localhost:8000/investment/loans/10229_AA_2231940/
same for cashflow details: http://localhost:8000/investment/cashflows/CF_10229_AA_2231940_5/
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Export loans and cashflows as excel files:
HTTP method: GET
http://localhost:8000/investment/export/cashflows/
http://localhost:8000/investment/export/loans/
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Realized Amount:
   HTTP method:POST
   Body-form-data:reference-date:2023-06-04
   Loan id example: 10229_AA_2231940
   http://localhost:8000/investment/realized-amount/10229_AA_2231940/
Gross Expected Amount:
  HTTP method:POST
  Body-form-data:reference-date:2023-06-30
  Loan id example: 10229_AA_2231762
  http://localhost:8000/investment/gross-expected-amount/10229_AA_2231762/
Remaining Invested Amount:
  HTTP method:POST
  Body-form-data:reference-date:2023-10-02
  Loan id example: 10229_AA_2231602
  http://localhost:8000/investment/remaining-invested-amount/10229_AA_2231602/
Closing Date:
  HTTP method: GET
  Loan id example:10229_AA_2231940
  http://localhost:8000/investment/closing-date/10229_AA_2231940/
  
   



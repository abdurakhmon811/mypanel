from django.urls import path
from .views import *


app_name = 'panel'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('incomes-expenses/', IncomesExpensesView.as_view(), name='incomes-expenses'),
    path('incomes/', IncomeView.as_view(), name='incomes'),
    path('expenses/', ExpenseView.as_view(), name='expenses'),
    path('transactions/', TransactionView.as_view(), name='transactions'),
]
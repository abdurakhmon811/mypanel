from django.contrib import admin
from .models import Expense, \
    Income, \
    Transaction
from .relationships import Account, \
    Category, \
    Subcategory

models = [
    Account, 
    Category, 
    Expense, 
    Income, 
    Subcategory, 
    Transaction
]
admin.site.register(models)

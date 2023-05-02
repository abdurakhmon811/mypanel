from django.contrib.auth.models import User
from django.db import models
from djmoney.models.fields import MoneyField
from .relationships import Account, \
    Category, \
    Subcategory


class Expense(models.Model):
    """
    A model for handling expenses.
    """

    currencies = [
        ('EURO', 'EURO'),
        ('RUB', 'RUB'),
        ('USD', 'USD'),
        ('UZS', 'UZS'),
    ]

    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    amount = MoneyField(
        max_digits=1000, 
        decimal_places=2, 
        default_currency='UZS', 
        currency_choices=currencies,
        currency_max_length=4
    )
    date = models.DateTimeField(auto_now_add=True, editable=True)
    comment = models.CharField(max_length=1000)
    maker = models.ForeignKey(User, on_delete=models.PROTECT)

    objects = models.Manager()

    def __str__(self) -> str:
        
        return self.account.name


class Income(models.Model):
    """
    A model for handling incomes.
    """

    currencies = [
        ('EURO', 'EURO'),
        ('RUB', 'RUB'),
        ('USD', 'USD'),
        ('UZS', 'UZS'),
    ]

    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    amount = MoneyField(
        max_digits=1000, 
        decimal_places=2, 
        default_currency='UZS', 
        currency_choices=currencies,
        currency_max_length=4
    )
    date = models.DateTimeField(auto_now_add=True, editable=True)
    comment = models.CharField(max_length=1000)
    maker = models.ForeignKey(User, on_delete=models.PROTECT)

    objects = models.Manager()

    def __str__(self) -> str:

        return self.account.name


class Transaction(models.Model):
    """
    A model for handling transactions between accounts.
    """

    currencies = [
        ('EURO', 'EURO'),
        ('RUB', 'RUB'),
        ('USD', 'USD'),
        ('UZS', 'UZS'),
    ]

    account1 = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='account1')
    account2 = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='account2')
    amount = MoneyField(
        max_digits=1000, 
        decimal_places=2, 
        default_currency='UZS', 
        currency_choices=currencies,
        currency_max_length=4
    )
    date = models.DateTimeField(auto_now_add=True, editable=True)
    comment = models.CharField(max_length=1000)
    maker = models.ForeignKey(User, on_delete=models.PROTECT)

    objects = models.Manager()

    def __str__(self) -> str:
        
        return str(self.from_.name) + ' > ' + str(self.to.name)

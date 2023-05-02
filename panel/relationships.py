from django.contrib.auth.models import User
from django.db import models
from djmoney.models.fields import MoneyField


class Account(models.Model):
    """
    A model for handling money accounts.
    """

    currencies = [
        ('EURO', 'EURO'),
        ('RUB', 'RUB'),
        ('USD', 'USD'),
        ('UZS', 'UZS'),
    ]

    name = models.CharField(max_length=100, unique=True)
    balance = MoneyField(
        max_digits=1000, 
        decimal_places=2, 
        default_currency='UZS', 
        currency_choices=currencies,
        currency_max_length=4
    )
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self) -> str:

        return self.name
    

    def decrement(self, amount: int | float):
        """
        A method for decrementing the current balance of the account by the amount provided.
        """

        self.balance.amount -= amount
        self.save()
    

    def increment(self, amount: int | float):
        """
        A method for incrementing the current balance of the account by the amount provided.
        """

        self.balance.amount += amount
        self.save()


class Category(models.Model):
    """
    A model for handling categories related to incomes or expenses.
    """

    class Meta:

        verbose_name_plural = 'Categories'

    choices = [
        ('Expense', 'Expense'),
        ('Income', 'Income'),
    ]

    name = models.CharField(max_length=500)
    related_to = models.CharField(max_length=7, choices=choices)

    objects = models.Manager()

    def __str__(self) -> str:

        return self.name


class Subcategory(models.Model):
    """
    A model for handling subcategories related to incomes or expenses.
    """

    class Meta:

        verbose_name_plural = 'Subcategories'

    choices = [
        ('Expense', 'Expense'),
        ('Income', 'Income'),
    ]

    name = models.CharField(max_length=500)
    related_to = models.CharField(max_length=7, choices=choices)

    objects = models.Manager()

    def __str__(self) -> str:

        return self.name
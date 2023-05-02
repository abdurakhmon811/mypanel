from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.generic import TemplateView, View
from .assistants import Validator
from .models import Expense, \
    Income, \
    Transaction
from .relationships import Account
from .serializers import ExpenseSerializer, \
    IncomeSerializer, \
    TransactionSerializer


class IndexView(TemplateView):
    """
    A view for rendering the main page of the panel.
    """
    
    template_name = 'panel/index.html'

    def get(self, request: HttpRequest):
        """
        A method for handling GET method of the request that comes for the index page.
        """

        return render(request, self.template_name)


class IncomesExpensesView(View):
    """
    A view for the page of incomes and expenses.
    """

    tempate_name = 'panel/incomes-expenses.html'
    validator = Validator()

    def get(self, request: HttpRequest):
        """
        A method for handling GET method of the request that comes for the incomes and expenses page.
        """

        incomes = render_to_string(
            'includes/incomes.html', 
            {'incomes': Income.objects.filter(maker=request.user).order_by('date')}
        )
        expenses = render_to_string(
            'includes/expenses.html', 
            {'expenses': Expense.objects.filter(maker=request.user).order_by('date')}
        )
        transactions = render_to_string(
            'includes/transactions.html',
            {'transactions': Transaction.objects.filter(maker=request.user).order_by('date')}
        )
        context = {
            'incomes': incomes,
            'expenses': expenses,
            'transactions': transactions,
        }
        return render(request, self.tempate_name, context)


class IncomeView(View):
    """
    A view for managing incomes.
    """

    template_name = 'includes/incomes.html'
    validator = Validator()

    def get(self, request: HttpRequest):
        """
        A method for retrieving/deleting incomes.
        """

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if not is_ajax and not request.user.is_superuser and request.method != 'GET':
            raise PermissionDenied
        
        income_id = self.validator.validate(request.GET.get('income_id'), r'[^0-9]', strip=True)
        income = get_object_or_404(Income, id=income_id)
        account = get_object_or_404(Account, id=income.account.id)
        if 'deleting' in request.GET:
            account.decrement(float(income.amount.amount))
            account.save()
            income.delete()
            html = render_to_string(
                self.template_name,
                {'incomes': Income.objects.filter(maker=request.user).order_by('date')}
            )
            return JsonResponse({'status': 200, 'html': html})
        else:
            result = IncomeSerializer(income)
            return JsonResponse({'status': 200, 'result': result})


    def post(self, request: HttpRequest):
        """
        A method for adding/editing incomes.
        """

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if not is_ajax and not request.user.is_superuser and request.method != 'POST':
            raise PermissionDenied

        income_id = self.validator.validate(request.POST.get('income_id'), r'[^0-9]', strip=True)
        category_id = self.validator.validate(request.POST.get('category_id'), r'[^0-9]', strip=True)
        subcategory_id = self.validator.validate(request.POST.get('subcategory_id'), r'[^0-9]', strip=True)
        account_id = self.validator.validate(request.POST.get('account_id'), r'[^0-9]', strip=True)
        amount = self.validator.validate(request.POST.get('amount'), r'[^0-9.,]', strip=True)
        date = self.validator.validate(request.POST.get('date'), r'[^0-9/.-:;,]')
        comment = self.validator.validate(request.POST.get('comment'), r'[^a-zA-Zа-яА-ЯёЁ0-9,.#+_-()]', strip=True)
        account = get_object_or_404(Account, id=account_id)
        if 'editing' in request.POST:
            income = get_object_or_404(Income, id=income_id)
            account.decrement(float(income.amount.amount))
            account.increment(float(amount))
            income.category = category_id
            income.subcategory = subcategory_id
            income.amount.amount = amount
            income.date = date
            income.comment = comment
            income.save()
            account.save()
            html = render_to_string(
                self.template_name,
                {'incomes': Income.objects.filter(maker=request.user).order_by('date')}
            )
            return JsonResponse({'status': 200, 'html': html})
        else:
            account.increment(float(amount))
            account.save()
            income = Income(
                account=account_id,
                amount=amount,
                comment=comment,
                maker=request.user,
            )
            income.save()
            html = render_to_string(
                self.template_name,
                {'incomes': Income.objects.filter(maker=request.user).order_by('date')}
            )
            return JsonResponse({'status': 200, 'html': html})


class ExpenseView(View):
    """
    A view for managing expenses.
    """

    template_name = 'includes/expenses.html'
    validator = Validator()

    def get(self, request: HttpRequest):
        """
        A method for retrieving/deleting expenses.
        """

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if not is_ajax and not request.user.is_superuser and request.method != 'GET':
            raise PermissionDenied
        
        expense_id = self.validator.validate(request.GET.get('expense_id'), r'[^0-9]', strip=True)
        expense = get_object_or_404(Expense, id=expense_id)
        account = get_object_or_404(Account, id=expense.account.id)
        if 'deleting' in request.GET:
            account.increment(float(expense.amount.amount))
            account.save()
            expense.delete()
            html = render_to_string(
                self.template_name,
                {'expenses': Expense.objects.filter(maker=request.user).order_by('date')}
            )
            return JsonResponse({'status': 200, 'html': html})
        else:
            result = ExpenseSerializer(expense)
            return JsonResponse({'status': 200, 'result': result})

    def post(self, request: HttpRequest):
        """
        A method for adding/editing expenses.
        """

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if not is_ajax and not request.user.is_superuser and request.method != 'POST':
            raise PermissionDenied

        expense_id = self.validator.validate(request.POST.get('expense_id'), r'[^0-9]', strip=True)
        category_id = self.validator.validate(request.POST.get('category_id'), r'[^0-9]', strip=True)
        subcategory_id = self.validator.validate(request.POST.get('subcategory_id'), r'[^0-9]', strip=True)
        account_id = self.validator.validate(request.POST.get('account_id'), r'[^0-9]', strip=True)
        amount = self.validator.validate(request.POST.get('amount'), r'[^0-9.,]', strip=True)
        date = self.validator.validate(request.POST.get('date'), r'[^0-9/.-:;,]')
        comment = self.validator.validate(request.POST.get('comment'), r'[^a-zA-Zа-яА-ЯёЁ0-9,.#+_-()]', strip=True)
        account = get_object_or_404(Account, id=account_id)
        if 'editing' in request.POST:
            expense = get_object_or_404(Income, id=expense_id)
            account.increment(float(expense.amount.amount))
            account.decrement(float(amount))
            expense.category = category_id
            expense.subcategory = subcategory_id
            expense.amount.amount = amount
            expense.date = date
            expense.comment = comment
            expense.save()
            account.save()
            html = render_to_string(
                self.template_name,
                {'incomes': Expense.objects.filter(maker=request.user).order_by('date')}
            )
            return JsonResponse({'status': 200, 'html': html})
        else:
            account.decrement(float(amount))
            account.save()
            expense = Expense(
                account=account_id,
                amount=amount,
                comment=comment,
                maker=request.user,
            )
            expense.save()
            html = render_to_string(
                self.template_name,
                {'expenses': Expense.objects.filter(maker=request.user).order_by('date')}
            )
            return JsonResponse({'status': 200, 'html': html})


class TransactionView(View):
    """
    A view for managing transactions.
    """

    template_name = 'includes/transactions.html'
    validator = Validator()

    def get(self, request: HttpRequest):
        """
        A method for retrieving/deleting transactions.
        """

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if not is_ajax and not request.user.is_superuser and request.method != 'GET':
            raise PermissionDenied
        
        transaction_id = self.validator.validate(request.GET.get('transaction_id'), r'[^0-9]', strip=True)
        transaction = get_object_or_404(Income, id=transaction_id)
        account1 = get_object_or_404(Account, id=transaction.account1.id)
        account2 = get_object_or_404(Account, id=transaction.account2.id)
        if 'deleting' in request.GET:
            account1.increment(float(transaction.amount.amount))
            account2.decrement(float(transaction.amount.amount))
            account1.save()
            account2.save()
            transaction.delete()
            html = render_to_string(
                self.template_name,
                {'transactions': Transaction.objects.filter(maker=request.user).order_by('date')}
            )
            return JsonResponse({'status': 200, 'html': html})
        else:
            result = TransactionSerializer(transaction)
            return JsonResponse({'status': 200, 'result': result})

    def post(self, request: HttpRequest):
        """
        A method for adding/editing transactions.
        """

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if not is_ajax and not request.user.is_superuser and request.method != 'POST':
            raise PermissionDenied

        transaction_id = self.validator.validate(request.POST.get('transaction_id'), r'[^0-9]', strip=True)
        account1 = self.validator.validate(request.POST.get('account1'), r'[^0-9]', strip=True)
        account2 = self.validator.validate(request.POST.get('account2'), r'[^0-9]', strip=True)
        amount = self.validator.validate(request.POST.get('amount'), r'[^0-9.,]', strip=True)
        date = self.validator.validate(request.POST.get('date'), r'[^0-9/.-:;,]')
        comment = self.validator.validate(request.POST.get('comment'), r'[^a-zA-Zа-яА-ЯёЁ0-9,.#+_-()]', strip=True)
        account1 = get_object_or_404(Account, id=account1)
        account2 = get_object_or_404(Account, id=account2)
        if 'editing' in request.POST:
            transaction = get_object_or_404(Transaction, id=transaction_id)
            account1.increment(float(transaction.amount.amount))
            account2.decrement(float(transaction.amount.amount))
            account1.decrement(float(amount))
            account2.increment(float(amount))
            account1.save()
            account2.save()
            transaction.amount.amount = amount
            transaction.date = date
            transaction.comment = comment
            transaction.save()
            html = render_to_string(
                self.template_name,
                {'transactions': Transaction.objects.filter(maker=request.user).order_by('date')}
            )
            return JsonResponse({'status': 200, 'html': html})
        else:
            account1.decrement(float(amount))
            account2.increment(float(amount))
            account1.save()
            account2.save()
            transaction = Transaction(
                account1=account1,
                account2=account2,
                amount=amount,
                comment=comment,
                maker=request.user,
            )
            transaction.save()
            html = render_to_string(
                self.template_name,
                {'transactions': Transaction.objects.filter(maker=request.user).order_by('date')}
            )
            return JsonResponse({'status': 200, 'html': html})

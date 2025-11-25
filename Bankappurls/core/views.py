from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import UserRegisterForm, QuickWalletForm

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html')

    account, _ = Account.objects.get_or_create(user=request.user, defaults={'balance': 0.00})
    transactions = account.transactions.all().order_by('-timestamp')[:5]

    if request.method == 'POST':
        form = QuickWalletForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']
            amount = form.cleaned_data['amount']

            if action == 'DEPOSIT':
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='DEPOSIT')
                messages.success(request, f'Deposited ₹{amount} successfully!')

            elif action == 'WITHDRAW':
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='WITHDRAW')
                    messages.success(request, f'Withdrew ₹{amount} successfully!')
                else:
                    messages.error(request, 'Insufficient balance!')
            return redirect('home')
        else:
            messages.error(request, 'Please enter a valid amount.')
    else:
        form = QuickWalletForm()

    return render(request, 'home.html', {
        'balance': account.balance,
        'transactions': transactions,
        'quick_form': form,
    })

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def deposit(request):
    account, _ = Account.objects.get_or_create(user=request.user, defaults={'balance': 0.00})
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='DEPOSIT')
        messages.success(request, f'Deposited ₹{amount} successfully!')
        return redirect('transactions')
    return render(request, 'deposit.html')
from django.contrib.auth import authenticate

@login_required
def withdraw(request):
    account, _ = Account.objects.get_or_create(user=request.user, defaults={'balance': 0.00})
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        password = request.POST.get('password')  #  get password from form

        #  Verify password before allowing withdrawal
        user = authenticate(username=request.user.username, password=password)
        if user is None:
            messages.error(request, 'Password incorrect. Withdrawal denied.')
            return redirect('withdraw')

        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='WITHDRAW')
            messages.success(request, f'Withdrew ₹{amount} successfully!')
        else:
            messages.error(request, 'Insufficient balance!')
        return redirect('transactions')
    return render(request, 'withdraw.html')

@login_required
def transaction_history(request):
    account, _ = Account.objects.get_or_create(user=request.user, defaults={'balance': 0.00})
    transactions = account.transactions.all().order_by('-timestamp')
    return render(request, 'transactions.html', {
        'transactions': transactions,
        'balance': account.balance
    })

@login_required
def profile(request):
    account, _ = Account.objects.get_or_create(user=request.user, defaults={'balance': 0.00})
    return render(request, 'profile.html', {
        'user': request.user,
        'balance': account.balance
    })
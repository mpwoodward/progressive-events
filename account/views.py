from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import AccountCreationForm, LoginForm
from .models import User


def create_account(request):
    form = AccountCreationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            extra_fields = {
                'first_name': form.cleaned_data.get('first_name').strip(),
                'last_name': form.cleaned_data.get('last_name').strip(),
                'zip': form.cleaned_data.get('zip').strip(),
            }

            User.objects.create_user(
                email=form.cleaned_data.get('email').strip(),
                password=form.cleaned_data.get('password').strip(),
                **extra_fields
            )

            user = authenticate(
                email=form.cleaned_data.get('email').strip(),
                password=form.cleaned_data.get('password').strip()
            )

            if user:
                login(request, user)
                messages.success(request, 'Your account was created! Enter your event details below.')
                return redirect('event:create')
            else:
                messages.error(request, "Your account was created, but we couldn't take you to the event form. Please log in.")
                return redirect('account:login')
        else:
            messages.error(request, 'Please correct the errors highlighted below.')

    return render(request, 'account/create_account.html', {'form': form})


def login_form(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data.get('email'),
                password=form.cleaned_data.get('password')
            )

            if user:
                login(request, user)
                return redirect('event:create')
            else:
                messages.error(request, 'Your login failed. Please try again.')

    return render(request, 'account/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('account:login')

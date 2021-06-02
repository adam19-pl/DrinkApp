from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import Drink

# Create your views here.
from django.urls import reverse
from django.views import View

from .forms import RegisterForm, LoginForm, AddDrinkForm


class IndexView(View):
    def get(self, request):
        return render(request, 'DrinkApp/index.html',)


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        context = {
            'form': form,
        }
        return render(request, 'DrinkApp/register.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            birthday = form.cleaned_data['birth_date']
            user_age = (datetime.now().date() - birthday).days/365
            password1 = form.cleaned_data['password']
            password2 = form.cleaned_data['password_confirm']
            if user_age < 18:
                context = {
                    'message': 'Musisz mieć 18 lat, żeby się zarejestrować !',
                    'form': form,
                }
                return render(request, 'DrinkApp/register.html', context)
            elif password1 != password2:
                context = {
                    'message': 'Hasła nie są takie same ! ',
                    'form': form,
                }
                return render(request, 'DrinkApp/register.html', context)
            else:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                )
                messages.success(request, 'Pomyślnie utworzyłeś konto !')
                return redirect('/login/')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, 'DrinkApp/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.error(request,'Błędny login lub hasło ! ')
                return redirect('/login/')

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request,'Pomyślne wylogowanie !')
        return redirect('/')


class DrinkListView(LoginRequiredMixin, View):
    def get(self, request):
        drinks = Drink.objects.all
        context = {
            'drinks' : drinks,
        }
        return render(request, 'DrinkApp/drinks.html', context)


class AddDrinkView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddDrinkForm()
        # form2 = AddIngredientsForm()
        context = {
            'form': form,
            # 'form2': form2,
        }
        return render(request, 'DrinkApp/add_drink.html', context)

    def post(self, request):
        form = AddDrinkForm(request.POST, request.FILES)
        if form.is_valid():
            created_drink = Drink.objects.create(
                who_add = request.user,
                name = form.cleaned_data['name'],
                category = form.cleaned_data['category'],
                prepare = form.cleaned_data['prepare'],
                ingredients = form.cleaned_data['ingredients'],
                kcal = form.cleaned_data['kcal'],
                portion = form.cleaned_data['portion'],
                time_prepare = form.cleaned_data['time_prepare'],
                image=form.cleaned_data['image']

            )
        #
        # if form2.is_valid():
        #     drink_ingredients = Ingretiend.Objects.Create()
        #     context = {
        #         'created_drink': created_drink,
        #     }
            return redirect('/drinks')
        else:
            messages.error(request, 'Coś poszło źle...')
            return redirect('/add')






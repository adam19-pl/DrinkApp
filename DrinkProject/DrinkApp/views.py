from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta
from .models import Drink, Ingredient

# Create your views here.
from django.urls import reverse
from django.views import View

from .forms import RegisterForm, LoginForm, AddDrinkForm, AdvancedDrinkSearch


class IndexView(View):
    def get(self, request):

        return render(request, 'DrinkApp/index.html')


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
            'drinks': drinks,
        }
        return render(request, 'DrinkApp/drinks.html', context)


class AddDrinkView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddDrinkForm()
        context = {
            'form': form,
        }
        return render(request, 'DrinkApp/add_drink.html', context)

    def post(self, request):
        form = AddDrinkForm(request.POST, request.FILES)
        if form.is_valid():
            print(f"Zdjęcie : {type(form.cleaned_data['image'])}")
            if Drink.objects.filter(name=form.cleaned_data['name']).exists():
                already_drink = Drink.objects.get(name=form.cleaned_data['name'])
                context = {
                    'already_drink': already_drink,
                    'form': form,
                }
                messages.error(request, """Podana nazwa drinka już istnieje!
                 Poniżej znajduję się link do przepisu, który zawiera już tą nazwę.
                 Proszę wybierz inną nazwę, jeśli Twój przepis różni się od wskazanego poniżej.""")
                return render(request, 'DrinkApp/add_drink.html', context)

            else:
                created_drink = Drink.objects.create(
                    who_add=request.user,
                    name=form.cleaned_data['name'],
                    category=form.cleaned_data['category'],
                    prepare=form.cleaned_data['prepare'],
                    kcal=form.cleaned_data['kcal'],
                    portion=form.cleaned_data['portion'],
                    time_prepare=form.cleaned_data['time_prepare'],
                    image=form.cleaned_data['image']
                )
                print(created_drink.image)
                first = Ingredient.objects.get_or_create(ingredient_name=form.cleaned_data['ingredient1'])
                print(first)
                second = Ingredient.objects.get_or_create(ingredient_name=form.cleaned_data['ingredient2'])
                third = Ingredient.objects.get_or_create(ingredient_name=form.cleaned_data['ingredient3'])
                fourth = Ingredient.objects.get_or_create(ingredient_name=form.cleaned_data['ingredient4'])
                five = Ingredient.objects.get_or_create(ingredient_name=form.cleaned_data['ingredient5'])
                sixth = Ingredient.objects.get_or_create(ingredient_name=form.cleaned_data['ingredient6'])
                seventh = Ingredient.objects.get_or_create(ingredient_name=form.cleaned_data['ingredient7'])
                eight = Ingredient.objects.get_or_create(ingredient_name=form.cleaned_data['ingredient8'])

                created_drink.ingredient.add(first[0], second[0], third[0], fourth[0], five[0],
                                             sixth[0], seventh[0], eight[0])
                return redirect(f'/drinks/{created_drink.id}')

        else:
            messages.error(request, 'Błąd danych w formularzu ! ')
            return redirect('/add/')


class DrinkDetailView(LoginRequiredMixin, View):
    def get(self,request, drink_id):
        drink = get_object_or_404(Drink, id=drink_id)
        context = {
            'drink': drink,
        }
        return render(request, 'DrinkApp/drink.html', context)


def search_by_ingredient(drink_list):

    list_to_context = []
    for drink in drink_list:
        for ingredient in drink:
            if ingredient not in list_to_context:
                list_to_context.append(ingredient)

    return list_to_context


class SearchDrinkView(LoginRequiredMixin, View):
    def get(self, request):
        form = AdvancedDrinkSearch()
        context = {
            'form': form
        }
        return render(request, 'DrinkApp/advanced_search.html', context)

    def post(self, request):
        form = AdvancedDrinkSearch(request.POST)
        if form.is_valid():
            searched_name = form.cleaned_data['name']
            searched_ingredients = form.cleaned_data['ingredient_search']

            if searched_name:
                drink_list = []
                objects = Drink.objects.filter(name__contains=searched_name)
                drink_list.append(objects)
                if searched_ingredients:
                    for i in searched_ingredients:
                        drink_list.append(Drink.objects.filter(ingredient=i))

                list_to_context = search_by_ingredient(drink_list)

                context = {
                    'objects': list_to_context,
                    'form': form,
                }

            elif searched_ingredients:
                drink_list = []
                for i in searched_ingredients:
                    drink_list.append(Drink.objects.filter(ingredient=i))

                list_to_context= search_by_ingredient(drink_list)
                # obiekt = Drink.objects.filter(ingredient=searched_ingredients[0])
                # print(obiekt)
                context = {
                    'objects': list_to_context,
                    'form': form,
                }
            else:
                context = {
                    'message': f'Brak wyników dla nazwy drinka : {searched_name} !',
                    'form': form,
                }
            return render(request, 'DrinkApp/advanced_search.html', context)

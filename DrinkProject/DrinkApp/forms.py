from django import forms
from django.forms import NumberInput
from .models import CATEGORY_CHOICE, Ingredient


class RegisterForm(forms.Form):
    username = forms.CharField(label='Login', max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Wpisz swój login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Wpisz hasło'}), label='Hasło', max_length=256,
                               min_length=8)
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}), label='Potwierdź hasło',
                                       max_length=256, min_length=8)
    email = forms.EmailField(label='E-mail', max_length=256, widget=forms.TextInput(attrs={'placeholder': 'Wpisz swój adres E-mail'}))
    birth_date = forms.DateField(label='Data urodzin',widget=NumberInput(attrs={'type': 'date'}))


class LoginForm(forms.Form):
    login = forms.CharField(label='Login', max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Wprowadź login'}))
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'placeholder': 'Wprowadź hasło'}), max_length=256, min_length=8)


class AddDrinkForm(forms.Form):
    name = forms.CharField(label='Nazwa Drinka', max_length=128, required=True,
                           widget=forms.TextInput(attrs={'placeholder': 'Wpisz nazwę'}))
    category = forms.ChoiceField(label='Kategoria', choices=CATEGORY_CHOICE, required=True)
    ingredient1 = forms.CharField(label='Składnik', max_length=256,
                                  widget=forms.TextInput(attrs={'placeholder': 'Wpisz Składnik'})
                                  )
    ingredient2 = forms.CharField(label='Składnik', max_length=256, required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Wpisz Składnik'})
                                  )
    ingredient3 = forms.CharField(label='Składnik', max_length=256, required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Wpisz Składnik'})
                                  )
    ingredient4 = forms.CharField(label='Składnik', max_length=256, required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Wpisz Składnik'})
                                  )
    ingredient5 = forms.CharField(label='Składnik', max_length=256, required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Wpisz Składnik'})
                                  )
    ingredient6 = forms.CharField(label='Składnik', max_length=256, required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Wpisz Składnik'})
                                  )
    ingredient7 = forms.CharField(label='Składnik', max_length=256, required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Wpisz Składnik'})
                                  )
    ingredient8 = forms.CharField(label='Składnik', max_length=256, required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Wpisz Składnik'})
                                  )
    prepare = forms.CharField(label='Sposób przygotowania (podaj tutaj ilości)', required=True, widget=forms.Textarea, max_length=1048)
    kcal = forms.IntegerField(label='Kalorie',min_value=0)
    portion = forms.IntegerField(label='Ilość porcji', min_value=0, required=True)
    time_prepare = forms.IntegerField(label='Czas Przygotowania(min)', min_value=1, required=True)
    image = forms.ImageField(required=False)

    # choices = forms.ModelMultipleChoiceField(
    #     queryset = Ingredient.objects.all(),  # not optional, use .all() if unsure
    #     widget=forms.CheckboxSelectMultiple,
    # )

# class AddIngredientsForm(forms.Form):
# https://github.com/rbartosinski/AssistancePlus/blob/master/assistance/views.py
# https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_one/


class AdvancedDrinkSearch(forms.Form):
    name = forms.CharField(label='Nazwa Drinka', max_length=128, required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Wprowadź nawzę drinka, którego chcesz wyszukać'}))
    ingredient_search = forms.ModelMultipleChoiceField(
        Ingredient.objects.all(), widget=forms.CheckboxSelectMultiple, required=False, label = 'Składniki'
    )
    # category = forms.ChoiceField(label='Kategoria', choices=CATEGORY_CHOICE, required=True)
    # ingredients = forms.CharField(label='Składniki', widget=forms.Textarea, required=True, max_length=1048)
    # kcal = forms.IntegerField(label='Kalorie', min_value=0)
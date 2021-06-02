from django import forms
from django.forms import NumberInput
from .models import CATEGORY_CHOICE, Ingredient


class RegisterForm(forms.Form):
    username = forms.CharField(label='Login', max_length=128)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', max_length=256,
                               min_length=8)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm password',
                                       max_length=256, min_length=8)
    email = forms.EmailField(label='email', max_length=256)
    birth_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))


class LoginForm(forms.Form):
    login = forms.CharField(label='Login', max_length=128)
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput, max_length=256, min_length=8)


class AddDrinkForm(forms.Form):
    name = forms.CharField(label='Nazwa Drinka', max_length=128, required=True,)
    category = forms.ChoiceField(label='Kategoria', choices=CATEGORY_CHOICE, required=True)
    prepare = forms.CharField(label='Sposób przygotowania', required=True, widget=forms.Textarea, max_length=1048)
    ingredients = forms.CharField(label='Składniki', widget=forms.Textarea, required=True, max_length=1048)
    kcal = forms.IntegerField(label='Kalorie',min_value=0)
    portion = forms.IntegerField(label='Ilość Porcji', min_value=0, required=True)
    time_prepare = forms.IntegerField(label='Czas Przygotowania', min_value=1, required=True)
    image = forms.ImageField()
    choices = forms.ModelMultipleChoiceField(
        queryset = Ingredient.objects.all(),  # not optional, use .all() if unsure
        widget=forms.CheckboxSelectMultiple,
    )

# class AddIngredientsForm(forms.Form):


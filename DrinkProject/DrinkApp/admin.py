from django.contrib import admin
from .models import Drink,Ingredient,DrinkIngredients
# Register your models here.

admin.site.register(Drink)
admin.site.register(Ingredient)
admin.site.register(DrinkIngredients)
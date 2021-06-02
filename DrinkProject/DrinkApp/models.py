from django.contrib.auth.models import User
from django.db import models

# Create your models here.
CATEGORY_CHOICE = (
    (0, 'SHOT'),
    (1, 'DRINK'),
    (2, 'KOKTAJL'),
)


class Drink(models.Model):
    who_add = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    category = models.IntegerField(choices=CATEGORY_CHOICE)
    prepare = models.CharField(max_length=1048)
    ingredients = models.CharField(max_length=1048)
    kcal = models.IntegerField(default=0)
    portion = models.IntegerField(default=0)
    time_prepare = models.IntegerField(default=1)
    image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=256)


class DrinkIngredients(models.Model):
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.SET_NULL, null=True)



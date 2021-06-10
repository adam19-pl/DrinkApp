from django.contrib.auth.models import User
from django.db import models

# Create your models here.
CATEGORY_CHOICE = (
    ('Shot', 'SHOT'),
    ('Drink', 'DRINK'),
    ('Koktajl', 'KOKTAJL'),
)


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=256)

    def __str__(self):
        return self.ingredient_name


class Drink(models.Model):
    who_add = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ManyToManyField(Ingredient)
    name = models.CharField(max_length=128)
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=128)
    prepare = models.CharField(max_length=1048)
    kcal = models.IntegerField(default=0)
    portion = models.IntegerField(default=0)
    time_prepare = models.IntegerField(default=1)
    image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name


class DrinkIngredients(models.Model):
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.SET_NULL, null=True)



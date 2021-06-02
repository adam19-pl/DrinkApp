from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('drinks/', views.DrinkListView.as_view(), name='drinks'),
    path('add/', views.AddDrinkView.as_view(), name='add_drink'),
]
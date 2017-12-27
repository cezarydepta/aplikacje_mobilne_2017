from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from diet_app.views import *
from diet_app import views


urlpatterns = [
    path('diary/', views.DiaryView.as_view(), name='diary'),
    path('activity/', views.ActivityView.as_view(), name='activity'),
    path('activities/', views.ActivitiesView.as_view(), name='activities'),
    path('product/', views.ProductView.as_view(), name='product'),
    path('products/', views.ProductsView.as_view(), name='products'),
    path('ingredient/', views.IngredientView.as_view(), name='ingredient'),
    path('discipline/', views.DisciplineView.as_view(), name='discipline'),
    path('disciplines/', views.DisciplinesView.as_view(), name='disciplines'),
    path('meal/', views.MealView.as_view(), name='meal'),
    path('meal-type/', views.MealTypeView.as_view(), name='meal-type'),
    path('meal-types/', views.MealTypesView.as_view(), name='meal-types'),
    path('user/', views.UserView.as_view(), name='user'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('weights/', views.WeightsView.as_view(), name='weights'),
    path('weight/', views.WeightView.as_view(), name='weight'),
    path('login/', views.LoginView.as_view(), name='login'),

]

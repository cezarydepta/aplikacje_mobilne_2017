from django.urls import path
from diet_app import views

urlpatterns = [
    path('diary/', views.diary, name='diary')
]

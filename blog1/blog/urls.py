# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),  # Главная страница со списком статей
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # Страница подробностей
]

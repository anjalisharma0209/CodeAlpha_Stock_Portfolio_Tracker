from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search-stock/', views.search_stock, name='search_stock'),
    path('add-stock/', views.add_stock, name='add_stock'),
    path('delete-stock/<str:ticker>/', views.delete_stock, name='delete_stock'),
]

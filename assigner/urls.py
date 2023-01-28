from django.shortcuts import render
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='ahome'),
    path('manual/', views.manual, name='manual'),
    path('<int:list_id>', views.list_detail, name='list_detail'),
    path('assigned/', views.assigned, name='assigned'),
    path('automatic/', views.automatic, name='automatic'),
    path('rooms/', views.rooms, name='rooms'),
    path('rooms/<int:room_id>', views.detail, name='detail'),
    path('rooms/search', views.search, name='search'),
    path('rooms/add', views.add, name='add'),
    path('rooms/<int:room_id>/delete', views.delete, name='delete'),
    path('rooms/<int:room_id>/edit', views.edit, name='edit'),
]

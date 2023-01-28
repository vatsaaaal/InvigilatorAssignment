from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='thome'),
    path('<int:teacher_id>', views.detail, name='detail'),
    path('search', views.search, name='search'),
    path('add', views.add, name='add'),
    path('<int:teacher_id>/delete', views.delete, name='delete'),
    path('<int:teacher_id>/edit', views.edit, name='edit'),
]
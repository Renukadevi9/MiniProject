from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_employee, name='add'),
    path('update/<int:pk>/', views.update_employee, name='update'),
    path('delete/<int:pk>/', views.delete_employee, name='delete'),
]

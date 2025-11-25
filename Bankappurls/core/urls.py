from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),  # ✅ now matches views.py
    path('transactions/', views.transaction_history, name='transactions'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),  # if you added profile
]

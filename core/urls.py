from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # Dashboard & Betting
    path('dashboard/', views.dashboard, name='dashboard'),
    path('bet/<int:outcome_id>/', views.place_bet, name='place_bet'),

    # Profile & Transactions
    path('profile/', views.profile_view, name='profile'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),

    # Terms
    path('terms/', views.terms_privacy, name='terms_privacy'),
]

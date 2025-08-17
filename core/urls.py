from django.urls import path
from . import views

app_name = "core"

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
    path('profile/', views.profile_view, name='profile_view'),
    path('deposit/', views.deposit_view, name='deposit_view'),
    path('withdraw/', views.withdraw_view, name='withdraw_view'),

    # Terms
    path('terms/', views.terms_privacy, name='terms_privacy'),
    path('about-us/', views.about_us, name='about_us'),  # Add this line
    # Missing URLs (Add these)
    path('sports/', views.sports, name='sports'),
    path('live/', views.live, name='live'),
    path('win-games/', views.win_games, name='win_games'),
    path('casino/', views.casino, name='casino'),
    path('live-casino/', views.live_casino, name='live_casino'),
    path('more/', views.more, name='more'),
]
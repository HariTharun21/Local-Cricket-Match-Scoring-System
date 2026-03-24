# access/urls.py
from django.urls import path
from . import views
from .views import Match, Player, Team
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
urlpatterns = [
   path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'), 
    
    # Users request access to a resource
    path('request/match/<int:match_id>/', views.request_access, name='request_match_access'),
    path('request/player/<int:player_id>/', views.request_access, name='request_player_access'),
    path('request/team/<int:team_id>/', views.request_access, name='request_team_access'),

    # Main user manages requests
    path('manage/match/<int:match_id>/', views.manage_requests, name='manage_match_requests'),
    path('manage/player/<int:player_id>/', views.manage_requests, name='manage_player_requests'),
    path('manage/team/<int:team_id>/', views.manage_requests, name='manage_team_requests'),

     # Forgot Password
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]


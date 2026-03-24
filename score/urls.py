from django.views.generic import TemplateView
from .views import (
    HomeView, PlayerListView, PlayerCreateView, PlayerUpdateView,
    PlayerDeleteView, TeamListView, TeamCreateView, TeamPlayersView,
    TeamDeleteView, MatchListView, MatchCreateView, MatchDeleteView,
    TossDecisionView, OverListView,  OverScoreView,BasicOverCreationView,ErrorReportCreateView)
from django.urls import path
urlpatterns = [
   
    path('', HomeView.as_view(), name='home'),
    path('home/', HomeView.as_view(), name='home'),  
    path('players/', PlayerListView.as_view(), name='player_list'),
    path('players/add/', PlayerCreateView.as_view(), name='player_create'),
    path('players/<int:pk>/edit/', PlayerUpdateView.as_view(), name='player_edit'),
    path('players/<int:pk>/delete/', PlayerDeleteView.as_view(), name='player_delete'),
    path('teams/', TeamListView.as_view(), name='team_list'),
    path('teams/add/', TeamCreateView.as_view(), name='team_create'),
    path('teams/<int:pk>/players/', TeamPlayersView.as_view(), name='team_players'),
    path('teams/<int:pk>/delete/', TeamDeleteView.as_view(), name='team_delete'),
    path('matches/', MatchListView.as_view(), name='match_list'),
    path('matches/add/', MatchCreateView.as_view(), name='match_create'),
    path('matches/<int:pk>/delete/', MatchDeleteView.as_view(), name='match_delete'),
    path('match/<int:match_id>/toss/', TossDecisionView.as_view(), name='toss_decision'),
    path('overs/', OverListView.as_view(), name='over_list'),

    
    path("over/create/<int:match_id>/", BasicOverCreationView.as_view(), name="basic_over_create"),

  
    path('over_score/<int:match_id>/<int:over_id>/<int:striker_id>/<int:non_striker_id>/<int:bowler_id>/', 
     OverScoreView.as_view(), name='over_score'),
     path('update_ball/<int:match_id>/<int:over_id>/', OverScoreView.as_view(), name='update_ball'),


      path("report-error/", ErrorReportCreateView.as_view(), name="report_error"),
    path("report-sent/", TemplateView.as_view(template_name="report_sent.html"), name="error_report_sent"),


]




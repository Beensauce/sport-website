from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index-page'),
    path('teams/', views.teams, name='team-list'),
    path('teams/<str:level>/<str:sport>/<int:year>', views.rooster, name='team'),
    path('teams/<str:level>/<str:sport>/<int:year>/<int:pk>', views.profile, name='player'),
    path('legends/', views.legends, name='legends'),
    path('past-seasons/', views.past_seasons, name="past-seasons"),
    path('register-player/', views.register_player, name='register-player'),
    path('register-legend/', views.register_legend, name='register-legend'),
    path('api/legends/<int:class_of>/', views.get_more_legends, name='get_more_legends'),
    path('api/teams/<int:year>/', views.get_more_teams, name='get_more_teams'),
    path('api/more-games/<str:level>/<str:sport>/<int:year>/<int:amount>', views.get_more_results, name='get_more_results'),
    path('api/more-upcomings/<str:level>/<str:sport>/<int:year>/<int:amount>', views.get_more_upcomings, name='get_more_upcomings'),
] 
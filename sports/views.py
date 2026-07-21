from django.shortcuts import get_object_or_404, redirect, render
from .models import Team, Player, Event, Game, Legend, SiteSettings, Coach
from django.utils import formats
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse
from .forms import PlayerForm, LegendForm
from django.contrib import messages

# Create your views here.
def index(request):
    events = Event.objects.all().order_by('-date')[:4]  
    results = Game.objects.filter(is_finished=True).order_by('-date')[:4]
    upcomings = Game.objects.filter(is_finished=False).order_by('-date')[:4]

    context = {
        'events':events,
        'results':results,
        'upcomings':upcomings,
    }
    return render(request, 'index.html', context)
 
def teams(request):
    settings = SiteSettings.objects.first()
    teams = Team.objects.filter(is_published=True, year=settings.current_academic_year)
    return render(request, 'team_list.html', {'teams': teams})


def rooster(request, level, sport, year):
    team = get_object_or_404(Team, level__code=level, sport__code=sport, year=year)
    players = Player.objects.filter(team=team, is_correct=True).exclude(is_captain=True).order_by('shirt_number')
    coaches = Coach.objects.filter(team=team)
    results = Game.objects.filter(is_finished=True, dcb_team=team).order_by('-date')[:2]
    upcomings = Game.objects.filter(is_finished=False, dcb_team=team).order_by('-date')[:2]


    context = {
        'team':team,
        'players':players,
        'results':results,
        'upcomings': upcomings,
        'coaches': coaches
    }

    return render(request, 'team.html', context)


def profile(request, level, sport, year, pk):
    player = get_object_or_404(Player, pk=pk)
    teamIn = get_object_or_404(Team, level__code=level, sport__code=sport, year=year)
    teamates = Player.objects.filter(team=teamIn, is_correct=True).exclude(pk=pk).order_by('?')[:4]

    context = {
        'teamates': teamates,
        'player': player
    }

    return render(request, 'player_profile.html', context)


def legends(request):
    legends = Legend.objects.filter(class_of=2026, is_correct=True)
    settings = SiteSettings.objects.first()
    years = list(range(2025, settings.current_academic_year + 2))
    
    context = {
        'legends': legends,
        'years': years
    }

    return render(request, 'legends.html', context)

# Getting more legends
@ratelimit(key='ip', rate="100/min")
def get_more_legends(request, class_of):
    legends = Legend.objects.filter(class_of=class_of, is_correct=True)
    legends_data = []
    for legend in legends: 
        legends_data.append({
            'name': legend.name,
            'teams': legend.teams,
            'description': legend.description,
            'image': legend.profile_pic_url
        })

    return JsonResponse({'legends_data': legends_data})


def past_seasons(request):
    settings = SiteSettings.objects.first()
    years = list(range(2025, settings.current_academic_year + 1))
    teams = Team.objects.filter(is_published=True, year=2025)
    context = {
        'teams': teams,
        'years': years,
    }
    return render(request, 'past-seasons.html', context)

# Getting more teams NEED TO FIX EFFICIENCY HERE
@ratelimit(key='ip', rate="100/min")
def get_more_teams(request, year):
    teams = Team.objects.filter(year=year, is_published=True)
    teams_data = []
    for team in teams: 
        captains = team.get_captain()
        
        teams_data.append({
            'name': str(team),    
            'sport': team.sport.code,
            'level': team.level.code,                               
            'sport_display': team.sport.name,                 
            'level_display': team.level.name,                 
            'coaches': [str(c.name) for c in team.get_coach()],  
            'student_coaches': [str(c.name) for c in team.get_student_coach()],
            'captain': [str(captain) for captain in captains] if captains else None,
            'image': team.get_image(),
        })

    return JsonResponse({'teams_data': teams_data})

# APIs getting mroe games FIX EFFICIENCY ISSUE
@ratelimit(key='ip', rate="100/min")
def get_more_results(request, level, sport, year, amount):
    team = get_object_or_404(Team, level__code=level, sport__code=sport, year=year)
    results = Game.objects.filter(dcb_team=team, is_finished=True).order_by('-date')[amount: amount + 4]
    result_data = []
    team_name_str = str(team)

    for result in results:
        result_data.append({
            'id': result.id,
            'dcb_team':team_name_str,
            'opposition':result.opposition,
            'raw_date': result.date,
            'raw_time': result.time,
            'date': formats.date_format(result.date, "F j, Y"),
            'time': formats.time_format(result.time, "g:i a") if result.time else None,
            'location':result.location,
            'dcb_score':result.dcb_score,
            'opp_score':result.opp_score,
            'is_finished':True
        })

    return JsonResponse({'games':result_data})
    
@ratelimit(key='ip', rate="100/min")
def get_more_upcomings(request, level, sport, year, amount):
    team = get_object_or_404(Team, level__code=level, sport__code=sport, year=year)
    upcomings = Game.objects.filter(dcb_team=team, is_finished=False).order_by('-date')[amount: amount + 4]
    upcoming_data = []

    for upcoming in upcomings:
        upcoming_data.append({
            'id': upcoming.id,
            'dcb_team':str(upcoming.dcb_team),
            'opposition':str(upcoming.opposition),
            'raw_date': upcoming.date,
            'raw_time': upcoming.time,
            'date': formats.date_format(upcoming.date, "F j, Y"),
            'time': formats.time_format(upcoming.time, "g:i a") if upcoming.time else None,
            'location':upcoming.location,
            'dcb_score':upcoming.dcb_score,
            'opp_score':upcoming.opp_score,
            'is_finished':False
        })

    return JsonResponse({'games':upcoming_data})


# Student registration
def register_player(request):
    if request.method == "POST":
        form = PlayerForm(request.POST, request.FILES) # Binds data with fields
        if form.is_valid():
            form.save() # creates player
            messages.success(request, "You have registered, pls wait whilst your captain approves")
            return redirect('index-page')
    else:
        form = PlayerForm() # creates empty form just in case
    return render(request, 'register-player.html', {'form': form})


def register_legend(request):
    if request.method == "POST":
        form = LegendForm(request.POST, request.FILES) # Binds data with fields
        if form.is_valid():
            form.save() # creates player
            messages.success(request, "You have registered, pls wait whilst beensauce approves")
            return redirect('index-page')
    else:
        form = LegendForm() # creates empty form just in case
    return render(request, 'register-legend.html', {'form': form})
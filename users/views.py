from django.shortcuts import get_object_or_404, redirect, render
from sports import models as sport_models
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import GameForm, TeamEditForm, CoachForm
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse

# Create your views here.
@login_required
def captain_panel(request, year=None):

    if not hasattr(request.user, 'captain'):
            messages.error(request, 'You are not a captain, try another account')
            return redirect('login')
    
    settings = sport_models.SiteSettings.objects.first()
    current_year = settings.current_academic_year
    years = list(range(2025, current_year + 1))
    if year:
        current_year = int(year)

    level = request.user.captain.level
    sport = request.user.captain.sport
    team = sport_models.Team.objects.filter(level=level, sport=sport, year=current_year).first()
    unreg_players = sport_models.Player.objects.filter(team=team, is_correct=False)
    reg_players = sport_models.Player.objects.filter(team=team, is_correct=True)
    coaches = sport_models.Coach.objects.filter(team=team)
    results = sport_models.Game.objects.filter(is_finished=True, dcb_team=team).order_by('-date')[:2]
    upcomings = sport_models.Game.objects.filter(is_finished=False, dcb_team=team).order_by('-date')[:2]
    game_form = GameForm()  
    edit_team_form = TeamEditForm(instance=team)
    coach_form =  CoachForm()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'reg_players':
            approved_list = request.POST.getlist('player_ids')
            if approved_list:
                players = sport_models.Player.objects.filter(id__in=approved_list, team=team)
                
                if players:
                    players.update(is_correct=True)
                    messages.success(request, f"Successfully approved {len(approved_list)} players")
                else:
                    messages.error(request, "Failed to update your selected players")

                return redirect('captain-panel-by-year', year=current_year)
            
        elif action == 'del_players':
            delete_list = request.POST.getlist('player_ids')
            if delete_list:
                players = sport_models.Player.objects.filter(id__in=delete_list, team=team)
                if players:
                    players.delete()
                    messages.success(request, f"Successfully deleted {len(delete_list)} players")
                else:
                    messages.error(request, "Failed to delete your selected players")
                return redirect('captain-panel-by-year', year=current_year)
            
        elif action == 'del_coach':
            delete_list = request.POST.getlist('delete_coach_ids')
            if delete_list:
                coaches = sport_models.Coach.objects.filter(id__in=delete_list, team=team)
                if coaches:
                    coaches.delete()
                    messages.success(request, f"Successfully deleted {len(delete_list)} Coaches")
                else:
                    messages.error(request, "Failed to delete your selected coaches")
                return redirect('captain-panel-by-year', year=current_year)

        elif action == 'unreg_players':
            unapproved_list = request.POST.getlist('unapproved_player_ids')
            if unapproved_list:
                players = sport_models.Player.objects.filter(id__in=unapproved_list, team=team)
                if players:
                    players.update(is_correct=False)
                    messages.success(request, f"Successfully unapproved {len(unapproved_list)} players")
                else:
                    messages.error(request, "Failed to update your selected players")
                return redirect('captain-panel-by-year', year=current_year)
            
        elif action == 'update_team':
            edit_team_form = TeamEditForm(request.POST, request.FILES or None, instance=team)
            if edit_team_form.is_valid():
                edit_team_form.save()
                messages.success(request, "Team updated succesfully")
                return redirect('captain-panel-by-year', year=current_year)
            
        elif action == 'add_game':
            game_form = GameForm(request.POST)
            if game_form.is_valid():
                game = game_form.save(commit=False)    
                
                # Validate: if game is finished, scores must be provided
                if game.is_finished:
                    if game.dcb_score is None or game.opp_score is None:
                        messages.error(request, "Both scores are required for finished games.")
                        return redirect('captain-panel-by-year', year=current_year)
                    
                game.dcb_team = team
                game.save()
                
                messages.success(request, "Added new game")
                return redirect('captain-panel-by-year', year=current_year)
        

        elif action == 'add_coach':
            coach_form = CoachForm(request.POST, request.FILES)
            if coach_form.is_valid():
                coach = coach_form.save(commit=False)    
                coach.team = team
                coach.save()
                
                messages.success(request, "Added new coach")
                return redirect('captain-panel-by-year', year=current_year)

                
    context = {
        'team':team,
        'unreg_players': unreg_players,
        'reg_players': reg_players,
        'coaches': coaches,
        'results': results,
        'upcomings': upcomings,
        'team_form': edit_team_form,
        'game_form': game_form,
        'coach_form': coach_form,
        'years': years,
        'current_year': current_year,
    }

    return render(request, 'users/captain.html', context)


@login_required
def edit_game(request, year):
    year = int(year)
    if request.method == 'POST':
        game_id = request.POST.get('game_id')
        
        game = get_object_or_404(sport_models.Game, id=game_id)
        
        try:
            game.opposition = request.POST.get("opposition")
            
            # Convert empty strings to None for integer fields
            dcb_score = request.POST.get("dcb_score")
            game.dcb_score = int(dcb_score) if dcb_score else None
            
            opp_score = request.POST.get("opp_score")
            game.opp_score = int(opp_score) if opp_score else None
            
            game.date = request.POST.get("date")
    
            time = request.POST.get("time")
            game.time = time if time else None
            
            game.location = request.POST.get("location") 
            game.is_finished = request.POST.get("is_finished") == "on"
            

            if game.is_finished:
                if game.dcb_score is None or game.opp_score is None:
                    raise ValueError("Both DCB Score and Opposition Score are required for finished games.")
                
            game.save()
            messages.success(request, "Game updated successfully!")
        except ValueError as e:
            messages.error(request, str(e))

        except Exception as e:
            messages.error(request, f"Error updating game: {str(e)}")
    
    return redirect('captain-panel-by-year', year=year)

@login_required
def delete_game(request, game_id, year):
    year = int(year)
    level = request.user.captain.level
    sport = request.user.captain.sport
    team = sport_models.Team.objects.filter(level=level, sport=sport, year=year).first()
    game = get_object_or_404(sport_models.Game, id=game_id, dcb_team=team)
    opposition = game.opposition
    game.delete()
    messages.success(request, f"Successfully deleted the game vs {opposition}")
    return redirect('captain-panel-by-year', year)


# Admin for legends
@user_passes_test(lambda u: u.is_superuser)
def legends_admin(request, class_of=None):
    settings = sport_models.SiteSettings.objects.first()
    current_year = settings.current_academic_year
    years = list(range(2025, current_year + 2))
    
    registered_Legends = sport_models.Legend.objects.filter(is_correct=True, class_of=current_year) 
    unregistered_Legends = sport_models.Legend.objects.filter(is_correct=False, class_of=current_year) 
    
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'reg_legends':
            approved_list = request.POST.getlist('legend_ids')
            if approved_list:
                sport_models.Legend.objects.filter(id__in=approved_list).update(is_correct=True)
                messages.success(request, f"Successfully approved {len(approved_list)} players")
                return redirect('legends-approval-by-year', class_of=current_year)
        
        elif action == 'unreg_legends':
            unapproved_list = request.POST.getlist('legend_ids')
            if unapproved_list:
                sport_models.Legend.objects.filter(id__in=unapproved_list).update(is_correct=False)
                messages.success(request, f"Successfully approved {len(unapproved_list)} players")
                return redirect('legends-approval-by-year', class_of=current_year)
            
        elif action == 'del_legends':
            delete_list = request.POST.getlist('legend_ids')
            if delete_list:
                sport_models.Legend.objects.filter(id__in=delete_list).delete()
                messages.success(request, f"Successfully deleted {len(delete_list)} legends")
                return redirect('legends-approval-by-year', class_of=current_year)
        
    context = {
        'reg_legends': registered_Legends,
        'unreg_legends': unregistered_Legends,
        'years': years,
        'current_year': current_year,
    }

    return render(request, 'users/legends-admin.html', context)

@ratelimit(key='ip', rate="100/min")
@user_passes_test(lambda u: u.is_superuser)
def get_more_legends(request, class_of):
    legends = sport_models.Legend.objects.filter(class_of=class_of)
    legends_data = []
    for legend in legends: 
        legends_data.append({
            'id': legend.id,
            'name': str(legend.name),
            'teams': legend.teams,
            'description': legend.description,
            'image': legend.profile_pic_url,
            'class_of': legend.class_of,
            'is_correct': legend.is_correct,
        })

    return JsonResponse({'legends_data': legends_data})
from django import forms
from sports.models import Game, Team, Coach

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['opposition', 'dcb_score', 'opp_score', 'date', 'time', 'location', 'is_finished']

        labels = {
            'is_finished': 'Is the game finished? If so, make it true, false otherwise',
            'time': 'In Hour:minute am/pm format'
        }

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

class TeamEditForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['description', 'image', 'instagram', 'is_published']

        labels = {
            'instagram': 'Instagram - Just put the link is fine',
            'is_published': 'Is it ready to be seen by everyone?'
        }

class CoachForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = ['name', 'image', 'is_student_coach']

    labels = {
        'is_student_coach': 'Is this coach a student as well?'
    }
from django import forms
from .models import Player, Legend, Team, SiteSettings

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['team', 'first_name', 'last_name', 'position', 'year', 
                  'image', 'shirt_number', 'is_captain', 'quote']
        labels = {
            'position': 'Your position (Striker, middle blocker...)',
            'year': 'Your year group',
            'image': 'Your profile image (optional, would be cool though)',
        }
        help_texts = {
            'year': 'e.g., 9th, 10th, 11th, 12th',
        }

    def __init__(self, *args, **kwargs):
        settings = SiteSettings.objects.first()
        current_year = settings.current_academic_year
        super().__init__(*args, **kwargs)
        self.fields['team'].queryset = Team.objects.filter(year=current_year)

class LegendForm(forms.ModelForm):
    class Meta:
        model = Legend
        fields = ['name','teams', 'class_of', 'image', 'description']
        labels = {
            'teams': 'Sport teams you played for, or coached before',
            'image': 'A cool pic of you',
            'description': 'Description, or a short quote about you',
            'class_of': 'Which year do you graduate? Class of 2026...'
        }
        help_texts = {
            'teams': 'Varsity Football, Jv basketball...',
        }
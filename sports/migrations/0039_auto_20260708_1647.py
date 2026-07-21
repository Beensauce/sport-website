# In your migration file (e.g., 000X_auto_2025XXXX_XXXX.py)

from django.db import migrations

def create_sports_and_levels(apps, schema_editor):
    Sport = apps.get_model('sports', 'Sport')
    Level = apps.get_model('sports', 'Level')
    
    # Create Sports
    sports = [
        ('VB', 'Volleyball'),
        ('FB', 'Football'),
        ('BB', 'Basketball'),
        ('TE', 'Tennis'),
        ('BD', 'Badminton'),
        ('TR', 'Track & Field'),
        ('SW', 'Swimming'),
    ]
    
    for code, name in sports:
        Sport.objects.get_or_create(code=code, name=name)
    
    # Create Levels
    levels = [
        ('BV', 'Boys Varsity'),
        ('GV', 'Girls Varsity'),
        ('JVB', 'Junior Varsity Boys'),
        ('JVG', 'Junior Varsity Girls'),
        ('U14B', 'Boys U14s A'),
        ('U14G', 'Girls U14s A'),
        ('14B', 'U14s B'),
        ('y7B', 'Boys Year 7'),
        ('y7G', 'Girls Year 7'),
    ]
    
    for code, name in levels:
        Level.objects.get_or_create(code=code, name=name)

class Migration(migrations.Migration):
    dependencies = [
        ('sports', '0038_alter_team_level_alter_team_sport'),  # Replace with your actual dependency
    ]

    operations = [
        migrations.RunPython(create_sports_and_levels),
    ]
from django.db import migrations

def transfer_sport_level_data(apps, schema_editor):
    Team = apps.get_model('sports', 'Team')
    Sport = apps.get_model('sports', 'Sport')
    Level = apps.get_model('sports', 'Level')
    
    for team in Team.objects.all():
        # Find the sport by code
        try:
            sport_obj = Sport.objects.get(code=team.sport)
            team.sport_new = sport_obj
        except Sport.DoesNotExist:
            # Handle missing sport if any
            print(f"Sport {team.sport} not found for team {team.id}")
        
        # Find the level by code
        try:
            level_obj = Level.objects.get(code=team.level)
            team.level_new = level_obj
        except Level.DoesNotExist:
            print(f"Level {team.level} not found for team {team.id}")
        
        team.save()

class Migration(migrations.Migration):
    dependencies = [
        ('sports', '0040_auto_20260708_1650'),  # Replace with actual dependency
    ]

    operations = [
        migrations.RunPython(transfer_sport_level_data),
    ]
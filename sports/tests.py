from django.test import TestCase, Client
from .models import Team, Player, Legend, SiteSettings, Game

# Create your tests here.
class SportsAppTests(TestCase):
    def setup(self):
        self.client = Client()
        self.settings = SiteSettings.objects.create(current_academic_year=2026)

        # Create Boys varsity volleyball
        self.team_bv = Team.objects.create(
            season='1',
            year=2026,
            sport='VB',
            level='BV',
            is_published=True
        )

        self.y7_team = Team.objects.create(
            season='1',
            year=2026,
            sport='FB',
            level='y7B',
            is_published=True
        )
    
    def test_team_priority_assignment(self):
        # Test whether auto priority system correct
        self.assertEqual(self.team_bv.priority, 1)
        self.assertEqual(self.y7_team.priority, 6)

    # Test output for team names
    def test_team_string_representation(self):
        self.assertEqual(str(self.team_bv), "Boys Varsity Volleyball 2026")
        self.assertEqual(str(self.y7_team), "Boys Year 7 Football 2026")


    # def test_teams_view_status_and_context(self):
        
        
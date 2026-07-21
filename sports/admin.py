from django.contrib import admin
from .models import Player, Team, Game, Event, Legend, Coach, SiteSettings, Sport, Level

admin.site.register(SiteSettings)
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Game)
admin.site.register(Event)
admin.site.register(Legend)
admin.site.register(Coach)
admin.site.register(Sport)
admin.site.register(Level)
from django.db import models
from django.contrib.auth.models import User
from sports.models import Sport, Level

# Create your models here.
class Captain(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.PROTECT, null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f"{self.level} {self.sport}"

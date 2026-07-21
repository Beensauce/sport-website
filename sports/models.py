from django.db import models
import random
from PIL import Image
from django.core.validators import MinValueValidator
from django.templatetags.static import static
# Create your models here.


# Change which year of teams to show
class SiteSettings(models.Model):
    current_academic_year = models.IntegerField(
        help_text="Use the school-year start year, e.g. 2025 for 2025-2026"
    )

    def __str__(self):
        return "Site Settings"
    
    @classmethod
    def get_current_year(cls):
        settings = cls.objects.first()

        if settings:
            return settings.current_academic_year
        return 2026
    

class Sport(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="e.g., Volleyball, Rugby")
    code = models.CharField(max_length=5, unique=True, help_text="e.g., VB, FB ")

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="e.g., Boys Varsity, U12 Boys")
    code = models.CharField(max_length=5, unique=True, help_text="e.g., BV, U12B")

    def __str__(self):
        return self.name


def resize_image_field(image_field_attr, max_width, max_height):
    try:
        if image_field_attr:
            img = Image.open(image_field_attr)

            if img.height > max_height or img.width > max_height:
                output_size = (max_width, max_height)
                img.thumbnail(output_size) # Maintain aspect ratio
                img.save(image_field_attr.path)
    except Exception as e:
        print(e)


class Team(models.Model):

    SEASON_CHOICES = [
        ('1', 'Season 1'),
        ('2', 'Season 2'),
        ('3', 'Season 3'),
        ('4', 'Season 4'),
        ('5', 'All season')
    ]
    

    season = models.CharField(max_length=10, choices=SEASON_CHOICES)
    year = models.IntegerField(default=SiteSettings.get_current_year, blank=True, help_text="e.g., 2025... 2026... 2027")
    sport = models.ForeignKey(Sport, on_delete=models.PROTECT)
    level = models.ForeignKey(Level, on_delete=models.PROTECT)

    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='teams/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    instagram = models.URLField(blank=True, null=True)
    priority = models.IntegerField(default=1, help_text="1=Varsity, 2=JV, 3=Lower teams (lower number = higher on page)")
    is_published = models.BooleanField(default=False, help_text="Only published teams are visible to the public")

    def get_captain(self):
        return self.players.filter(is_captain=True, is_correct=True)
    
    def get_coach(self):
        return self.coaches.filter(is_student_coach=False)
    
    def get_student_coach(self):
         return self.coaches.filter(is_student_coach=True)
    
    def get_image(self):
        if self.image:
            return self.image.url
        return static('Pictures/default-pics/amogusSports.png')

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return f"{self.level} {self.sport} {self.year}"
    
    def save(self, *args, **kwargs):
        
        if not self.priority or self.priority == 1:  # If default or not changed
            if self.level.code in ['BV', 'GV']:
                self.priority = 1
            elif self.level.code in ['JVB', 'JVG']:
                self.priority = 2
            elif self.level.code in ['U14B', 'U14G']:
                self.priority = 4
            elif self.level.code in ['14B']:
                self.priority = 5
            elif self.level.code == 'y7':
                self.priority = 6
        super().save(*args, **kwargs)

        resize_image_field(self.image, 1920, 1080)


class Coach(models.Model):
    is_student_coach = models.BooleanField(default=False)
    name = models.CharField(max_length=300)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="coaches")
    image = models.ImageField(upload_to='coaches/', blank=True, null=True)

    DEFAULT_PICS = [
        'Pictures/amongus/Orange.png',
        'Pictures/amongus/Yellow.png',
        'Pictures/amongus/White.png',
        'Pictures/amongus/Red.png',
        'Pictures/amongus/Purple.png',
    ]

    class Meta:
        ordering = ['is_student_coach']


    def __str__(self):
        return f"{self.name}"
    
    def profile_pic_url(self):
        if self.image:
            return self.image.url
        else:
            return static(random.choice(self.DEFAULT_PICS))
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        resize_image_field(self.image, 350, 150)


class Player(models.Model):

    YEAR_GROUP = [
        (7, "Year 7"),
        (8, "Year 8"),
        (9, "Year 9"),
        (10, "Year 10"),
        (11, "Year 11"),
        (12, "Year 12"),
        (13, "Year 13"),
    ]
        
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField(choices=YEAR_GROUP)
    image = models.ImageField(upload_to='players/', blank=True, null=True)
    is_captain = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    shirt_number = models.IntegerField(blank=True, null=True)
    quote = models.CharField(max_length=500, blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    
    DEFAULT_PICS = [
        'Pictures/amongus/Orange.png',
        'Pictures/amongus/Yellow.png',
        'Pictures/amongus/White.png',
        'Pictures/amongus/Red.png',
        'Pictures/amongus/Purple.png',
    ]

    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def profile_pic_url(self):
        if self.image:
            return self.image.url
        else:
            return static(random.choice(self.DEFAULT_PICS))
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        resize_image_field(self.image, 350, 150)


class Game(models.Model):
    dcb_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='dcb_team')
    opposition = models.CharField(max_length=50)
    dcb_score = models.PositiveIntegerField(blank=True, null=True)
    opp_score = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)  
    location = models.CharField(max_length=200, blank=True, null=True)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.dcb_team} vs {self.opposition} - {self.date} {self.time}"
    
    @property
    def datetime_combined(self):
        from datetime import datetime
        return datetime.combine(self.date, self.time)


class Event(models.Model):
    event_name = models.CharField(max_length=50)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/')

    def __str__(self):
        return self.event_name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        resize_image_field(self.image, 1920, 1080)


class Legend(models.Model):
    name = models.CharField(max_length=300)
    teams = models.CharField(max_length=200)
    image = models.ImageField(upload_to='legends/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    class_of = models.PositiveIntegerField(validators=[MinValueValidator(2025)])

    DEFAULT_PICS = [
        'Pictures/amongus/Orange.png',
        'Pictures/amongus/Yellow.png',
        'Pictures/amongus/White.png',
        'Pictures/amongus/Red.png',
        'Pictures/amongus/Purple.png',
    ]
    
    def __str__(self):
        return self.name
    
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        resize_image_field(self.image, 450, 450)

    @property
    def profile_pic_url(self):
        if self.image:
            return self.image.url
        else:
            return static(random.choice(self.DEFAULT_PICS))

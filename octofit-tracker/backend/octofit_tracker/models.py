from djongo import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MinLengthValidator


class User(models.Model):
    """User model for fitness app users"""
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(1, message="Name cannot be empty")]
    )
    email = models.EmailField(unique=True)
    team = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(1, message="Team cannot be empty")]
    )
    avatar = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(1, message="Avatar cannot be empty")]
    )
    total_points = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, message="Points cannot be negative")]
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.name} ({self.email})"


class Team(models.Model):
    """Team model for team-based competition"""
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    members = models.JSONField(default=list)
    total_points = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, message="Points cannot be negative")]
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Activity(models.Model):
    """Activity model for tracking fitness activities"""
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('weightlifting', 'Weightlifting'),
        ('yoga', 'Yoga'),
        ('boxing', 'Boxing'),
    ]
    
    _id = models.ObjectIdField(primary_key=True)
    user_email = models.EmailField()
    user_name = models.CharField(max_length=200)
    activity_type = models.CharField(max_length=100, choices=ACTIVITY_TYPES)
    duration = models.IntegerField(
        help_text="Duration in minutes",
        validators=[MinValueValidator(0, message="Duration cannot be negative")]
    )
    distance = models.FloatField(
        default=0,
        help_text="Distance in km",
        validators=[MinValueValidator(0.0, message="Distance cannot be negative")]
    )
    calories = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, message="Calories cannot be negative")]
    )
    points = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, message="Points cannot be negative")]
    )
    date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'activities'
        ordering = ['-date']

    def __str__(self):
        return f"{self.user_name} - {self.activity_type} ({self.date.strftime('%Y-%m-%d')})"


class Leaderboard(models.Model):
    """Leaderboard model for rankings"""
    _id = models.ObjectIdField(primary_key=True)
    type = models.CharField(max_length=20, choices=[('individual', 'Individual'), ('team', 'Team')])
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    team = models.CharField(max_length=200, null=True, blank=True)
    points = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']

    def __str__(self):
        return f"{self.type}: {self.name} - Rank {self.rank}"


class Workout(models.Model):
    """Workout model for workout recommendations"""
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=50, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ])
    duration = models.IntegerField(help_text="Duration in minutes")
    exercises = models.JSONField(default=list)
    target_muscle_groups = models.JSONField(default=list)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return f"{self.name} ({self.difficulty})"

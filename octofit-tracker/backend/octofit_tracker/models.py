from djongo import models
from django.utils import timezone


class User(models.Model):
    """User model for fitness app users"""
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    team = models.CharField(max_length=200)
    avatar = models.CharField(max_length=10)
    total_points = models.IntegerField(default=0)
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
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Activity(models.Model):
    """Activity model for tracking fitness activities"""
    _id = models.ObjectIdField(primary_key=True)
    user_email = models.EmailField()
    user_name = models.CharField(max_length=200)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Duration in minutes")
    distance = models.FloatField(default=0, help_text="Distance in km")
    calories = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
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

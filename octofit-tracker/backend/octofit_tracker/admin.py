from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model"""
    list_display = ['name', 'email', 'team', 'total_points', 'created_at']
    list_filter = ['team', 'created_at']
    search_fields = ['name', 'email']
    ordering = ['-total_points']
    readonly_fields = ['_id', 'created_at']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team model"""
    list_display = ['name', 'description', 'total_points', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-total_points']
    readonly_fields = ['_id', 'created_at']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity model"""
    list_display = ['user_name', 'activity_type', 'duration', 'distance', 'points', 'date']
    list_filter = ['activity_type', 'date']
    search_fields = ['user_name', 'user_email', 'activity_type']
    ordering = ['-date']
    readonly_fields = ['_id']
    date_hierarchy = 'date'


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard model"""
    list_display = ['rank', 'name', 'type', 'team', 'points', 'updated_at']
    list_filter = ['type', 'team']
    search_fields = ['name', 'email']
    ordering = ['rank']
    readonly_fields = ['_id', 'updated_at']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin interface for Workout model"""
    list_display = ['name', 'difficulty', 'duration', 'created_at']
    list_filter = ['difficulty', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['difficulty', 'name']
    readonly_fields = ['_id', 'created_at']

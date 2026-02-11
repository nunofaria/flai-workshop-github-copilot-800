from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = ['_id', 'name', 'email', 'team', 'avatar', 'total_points', 'created_at']
        read_only_fields = ['_id', 'created_at']


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    
    class Meta:
        model = Team
        fields = ['_id', 'name', 'description', 'members', 'total_points', 'created_at']
        read_only_fields = ['_id', 'created_at']


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    
    class Meta:
        model = Activity
        fields = [
            '_id', 'user_email', 'user_name', 'activity_type', 
            'duration', 'distance', 'calories', 'points', 'date', 'notes'
        ]
        read_only_fields = ['_id']


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    
    class Meta:
        model = Leaderboard
        fields = ['_id', 'type', 'name', 'email', 'team', 'points', 'rank', 'updated_at']
        read_only_fields = ['_id', 'updated_at']


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for Workout model"""
    
    class Meta:
        model = Workout
        fields = [
            '_id', 'name', 'description', 'difficulty', 
            'duration', 'exercises', 'target_muscle_groups', 'created_at'
        ]
        read_only_fields = ['_id', 'created_at']

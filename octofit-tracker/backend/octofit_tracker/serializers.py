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
    
    exercises = serializers.SerializerMethodField()
    target_muscle_groups = serializers.SerializerMethodField()
    
    class Meta:
        model = Workout
        fields = [
            '_id', 'name', 'description', 'difficulty', 
            'duration', 'exercises', 'target_muscle_groups', 'created_at'
        ]
        read_only_fields = ['_id', 'created_at']
    
    def get_exercises(self, obj):
        """Convert exercises to proper list of dicts"""
        if isinstance(obj.exercises, str):
            import ast
            try:
                # Try to evaluate string representation
                return ast.literal_eval(obj.exercises)
            except:
                return []
        return obj.exercises if obj.exercises else []
    
    def get_target_muscle_groups(self, obj):
        """Convert target_muscle_groups to proper list"""
        if isinstance(obj.target_muscle_groups, str):
            import ast
            try:
                # Try to evaluate string representation
                return ast.literal_eval(obj.target_muscle_groups)
            except:
                return []
        return obj.target_muscle_groups if obj.target_muscle_groups else []

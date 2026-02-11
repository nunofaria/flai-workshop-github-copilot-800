from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, TeamSerializer, ActivitySerializer,
    LeaderboardSerializer, WorkoutSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.
    Provides CRUD operations for user profiles.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['team', 'email']
    search_fields = ['name', 'email']
    ordering_fields = ['total_points', 'created_at', 'name']
    ordering = ['-total_points']

    @action(detail=False, methods=['get'])
    def top_performers(self, request):
        """Get top 10 users by points"""
        top_users = User.objects.all().order_by('-total_points')[:10]
        serializer = self.get_serializer(top_users, many=True)
        return Response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing teams.
    Provides CRUD operations for teams.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['total_points', 'created_at', 'name']
    ordering = ['-total_points']

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of a specific team"""
        team = self.get_object()
        users = User.objects.filter(team=team.name)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing fitness activities.
    Provides CRUD operations for tracking activities.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user_email', 'activity_type', 'user_name']
    search_fields = ['user_name', 'activity_type', 'notes']
    ordering_fields = ['date', 'points', 'calories', 'duration']
    ordering = ['-date']

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent activities (last 30 days)"""
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_activities = Activity.objects.filter(date__gte=thirty_days_ago)
        serializer = self.get_serializer(recent_activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get activities for a specific user email"""
        email = request.query_params.get('email', None)
        if email:
            activities = Activity.objects.filter(user_email=email)
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response({"error": "Email parameter required"}, status=400)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing leaderboard.
    Provides access to individual and team rankings.
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type', 'team']
    ordering_fields = ['rank', 'points']
    ordering = ['rank']

    @action(detail=False, methods=['get'])
    def individual(self, request):
        """Get individual leaderboard"""
        individual_board = Leaderboard.objects.filter(type='individual').order_by('rank')
        serializer = self.get_serializer(individual_board, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def teams(self, request):
        """Get team leaderboard"""
        team_board = Leaderboard.objects.filter(type='team').order_by('rank')
        serializer = self.get_serializer(team_board, many=True)
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing workout recommendations.
    Provides CRUD operations for workout plans.
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['difficulty']
    search_fields = ['name', 'description', 'target_muscle_groups']
    ordering_fields = ['duration', 'created_at', 'name']
    ordering = ['name']

    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Get workouts filtered by difficulty level"""
        difficulty = request.query_params.get('level', None)
        if difficulty in ['beginner', 'intermediate', 'advanced']:
            workouts = Workout.objects.filter(difficulty=difficulty)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response({"error": "Invalid difficulty level. Use: beginner, intermediate, or advanced"}, status=400)

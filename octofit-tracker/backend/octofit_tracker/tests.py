from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import User, Team, Activity, Leaderboard, Workout


class UserAPITestCase(APITestCase):
    """Test cases for User API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'name': 'Test Hero',
            'email': 'test@hero.com',
            'team': 'Test Team',
            'avatar': '🦸',
            'total_points': 100
        }
        self.user = User.objects.create(**self.user_data)
    
    def test_get_users_list(self):
        """Test retrieving list of users"""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_user(self):
        """Test creating a new user"""
        url = reverse('user-list')
        new_user = {
            'name': 'New Hero',
            'email': 'newhero@test.com',
            'team': 'Test Team',
            'avatar': '⚡',
            'total_points': 0
        }
        response = self.client.post(url, new_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_user_detail(self):
        """Test retrieving a specific user"""
        url = reverse('user-detail', kwargs={'pk': self.user._id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user_data['email'])


class TeamAPITestCase(APITestCase):
    """Test cases for Team API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.team_data = {
            'name': 'Test Avengers',
            'description': 'Mighty test heroes',
            'members': ['Hero1', 'Hero2'],
            'total_points': 500
        }
        self.team = Team.objects.create(**self.team_data)
    
    def test_get_teams_list(self):
        """Test retrieving list of teams"""
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_team(self):
        """Test creating a new team"""
        url = reverse('team-list')
        new_team = {
            'name': 'New League',
            'description': 'New test team',
            'members': ['Hero3'],
            'total_points': 0
        }
        response = self.client.post(url, new_team, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ActivityAPITestCase(APITestCase):
    """Test cases for Activity API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.activity_data = {
            'user_email': 'test@hero.com',
            'user_name': 'Test Hero',
            'activity_type': 'running',
            'duration': 30,
            'distance': 5.0,
            'calories': 300,
            'points': 50,
            'notes': 'Test run'
        }
        self.activity = Activity.objects.create(**self.activity_data)
    
    def test_get_activities_list(self):
        """Test retrieving list of activities"""
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_activity(self):
        """Test creating a new activity"""
        url = reverse('activity-list')
        new_activity = {
            'user_email': 'test@hero.com',
            'user_name': 'Test Hero',
            'activity_type': 'cycling',
            'duration': 45,
            'distance': 15.0,
            'calories': 400,
            'points': 60,
            'notes': 'Test cycling'
        }
        response = self.client.post(url, new_activity, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_filter_activities_by_type(self):
        """Test filtering activities by type"""
        url = reverse('activity-list')
        response = self.client.get(url, {'activity_type': 'running'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LeaderboardAPITestCase(APITestCase):
    """Test cases for Leaderboard API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.leaderboard_data = {
            'type': 'individual',
            'name': 'Test Hero',
            'email': 'test@hero.com',
            'team': 'Test Team',
            'points': 500,
            'rank': 1
        }
        self.leaderboard_entry = Leaderboard.objects.create(**self.leaderboard_data)
    
    def test_get_leaderboard_list(self):
        """Test retrieving leaderboard"""
        url = reverse('leaderboard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_individual_leaderboard(self):
        """Test retrieving individual leaderboard"""
        url = reverse('leaderboard-individual')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_team_leaderboard(self):
        """Test retrieving team leaderboard"""
        url = reverse('leaderboard-teams')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITestCase(APITestCase):
    """Test cases for Workout API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.workout_data = {
            'name': 'Test Workout',
            'description': 'A test workout routine',
            'difficulty': 'beginner',
            'duration': 30,
            'exercises': [
                {'name': 'Push-ups', 'sets': 3, 'reps': 10}
            ],
            'target_muscle_groups': ['chest', 'arms']
        }
        self.workout = Workout.objects.create(**self.workout_data)
    
    def test_get_workouts_list(self):
        """Test retrieving list of workouts"""
        url = reverse('workout-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_workout(self):
        """Test creating a new workout"""
        url = reverse('workout-list')
        new_workout = {
            'name': 'Advanced Cardio',
            'description': 'High intensity cardio',
            'difficulty': 'advanced',
            'duration': 45,
            'exercises': [
                {'name': 'Burpees', 'sets': 4, 'reps': 15}
            ],
            'target_muscle_groups': ['cardio', 'full-body']
        }
        response = self.client.post(url, new_workout, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_filter_workouts_by_difficulty(self):
        """Test filtering workouts by difficulty"""
        url = reverse('workout-list')
        response = self.client.get(url, {'difficulty': 'beginner'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIRootTestCase(APITestCase):
    """Test cases for API root endpoint"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_api_root(self):
        """Test API root returns all available endpoints"""
        url = reverse('api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)

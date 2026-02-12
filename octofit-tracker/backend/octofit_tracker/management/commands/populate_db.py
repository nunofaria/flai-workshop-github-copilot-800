from django.core.management.base import BaseCommand
from django.utils import timezone
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import timedelta
import random
import os
import sys


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force data population without confirmation',
        )

    def handle(self, *args, **kwargs):
        # Safety check: Prevent running in production
        if os.environ.get('DJANGO_ENV') == 'production':
            self.stdout.write(
                self.style.ERROR(
                    'ERROR: This command cannot be run in production! '
                    'It will delete all existing data.'
                )
            )
            sys.exit(1)
        
        # Confirmation prompt unless --force is used
        if not kwargs.get('force'):
            self.stdout.write(
                self.style.WARNING(
                    '\nWARNING: This command will DELETE ALL existing data '
                    'in the database and populate it with test data.'
                )
            )
            confirmation = input('Are you sure you want to continue? (yes/no): ')
            if confirmation.lower() != 'yes':
                self.stdout.write(self.style.ERROR('Operation cancelled.'))
                return

        # Clear existing data using Django ORM
        self.stdout.write('Clearing existing data...')
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Cleared existing data'))

        # Sample superhero users data - define as dicts for easy iteration
        users_data = [
            # Team Marvel
            {
                "name": "Tony Stark",
                "email": "ironman@marvel.com",
                "team": "Team Marvel",
                "avatar": "🦾",
                "total_points": 0,
                "created_at": timezone.now()
            },
            {
                "name": "Steve Rogers",
                "email": "captain@marvel.com",
                "team": "Team Marvel",
                "avatar": "🛡️",
                "total_points": 0,
                "created_at": timezone.now()
            },
            {
                "name": "Natasha Romanoff",
                "email": "blackwidow@marvel.com",
                "team": "Team Marvel",
                "avatar": "🕷️",
                "total_points": 0,
                "created_at": timezone.now()
            },
            {
                "name": "Thor Odinson",
                "email": "thor@marvel.com",
                "team": "Team Marvel",
                "avatar": "⚡",
                "total_points": 0,
                "created_at": timezone.now()
            },
            {
                "name": "Bruce Banner",
                "email": "hulk@marvel.com",
                "team": "Team Marvel",
                "avatar": "💪",
                "total_points": 0,
                "created_at": timezone.now()
            },
            # Team DC
            {
                "name": "Bruce Wayne",
                "email": "batman@dc.com",
                "team": "Team DC",
                "avatar": "🦇",
                "total_points": 0,
                "created_at": timezone.now()
            },
            {
                "name": "Clark Kent",
                "email": "superman@dc.com",
                "team": "Team DC",
                "avatar": "🦸",
                "total_points": 0,
                "created_at": timezone.now()
            },
            {
                "name": "Diana Prince",
                "email": "wonderwoman@dc.com",
                "team": "Team DC",
                "avatar": "⭐",
                "total_points": 0,
                "created_at": timezone.now()
            },
            {
                "name": "Barry Allen",
                "email": "flash@dc.com",
                "team": "Team DC",
                "avatar": "⚡",
                "total_points": 0,
                "created_at": timezone.now()
            },
            {
                "name": "Arthur Curry",
                "email": "aquaman@dc.com",
                "team": "Team DC",
                "avatar": "🔱",
                "total_points": 0,
                "created_at": timezone.now()
            }
        ]

        # Insert users using Django ORM
        users = []
        for user_data in users_data:
            user = User.objects.create(**user_data)
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(users)} users'))

        # Teams data
        teams_data = [
            {
                "name": "Team Marvel",
                "description": "Earth's Mightiest Heroes",
                "members": [
                    "Tony Stark",
                    "Steve Rogers",
                    "Natasha Romanoff",
                    "Thor Odinson",
                    "Bruce Banner"
                ],
                "total_points": 0,
                "created_at": timezone.now()
            },
            {
                "name": "Team DC",
                "description": "Justice League",
                "members": [
                    "Bruce Wayne",
                    "Clark Kent",
                    "Diana Prince",
                    "Barry Allen",
                    "Arthur Curry"
                ],
                "total_points": 0,
                "created_at": timezone.now()
            }
        ]

        # Insert teams using Django ORM
        teams = []
        for team_data in teams_data:
            team = Team.objects.create(**team_data)
            teams.append(team)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(teams)} teams'))

        # Sample activities data
        activity_types = ["running", "cycling", "swimming", "weightlifting", "yoga", "boxing"]
        activities_data = []
        
        for user in users_data:
            # Generate 5-10 random activities per user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                days_ago = random.randint(1, 30)
                activity_date = timezone.now() - timedelta(days=days_ago)
                activity_type = random.choice(activity_types)
                
                # Generate realistic metrics based on activity type
                if activity_type == "running":
                    duration = random.randint(20, 90)  # minutes
                    distance = round(random.uniform(3, 15), 2)  # km
                    calories = int(duration * random.uniform(8, 12))
                    points = int(duration * 1.5)
                elif activity_type == "cycling":
                    duration = random.randint(30, 120)
                    distance = round(random.uniform(10, 50), 2)
                    calories = int(duration * random.uniform(6, 10))
                    points = int(duration * 1.2)
                elif activity_type == "swimming":
                    duration = random.randint(20, 60)
                    distance = round(random.uniform(0.5, 3), 2)
                    calories = int(duration * random.uniform(10, 14))
                    points = int(duration * 2)
                elif activity_type == "weightlifting":
                    duration = random.randint(30, 90)
                    distance = 0
                    calories = int(duration * random.uniform(5, 8))
                    points = int(duration * 1.8)
                elif activity_type == "yoga":
                    duration = random.randint(30, 90)
                    distance = 0
                    calories = int(duration * random.uniform(3, 5))
                    points = int(duration * 1.0)
                else:  # boxing
                    duration = random.randint(30, 60)
                    distance = 0
                    calories = int(duration * random.uniform(10, 15))
                    points = int(duration * 2.5)
                
                activities_data.append({
                    "user_email": user["email"],
                    "user_name": user["name"],
                    "activity_type": activity_type,
                    "duration": duration,
                    "distance": distance,
                    "calories": calories,
                    "points": points,
                    "date": activity_date,
                    "notes": f"Great {activity_type} session!"
                })

        # Insert activities using Django ORM (bulk_create for efficiency)
        if activities_data:
            activities = [Activity(**activity_data) for activity_data in activities_data]
            Activity.objects.bulk_create(activities)
            self.stdout.write(self.style.SUCCESS(f'Inserted {len(activities)} activities'))

        # Calculate total points for users and update using Django ORM
        for user in users:
            user_activities = Activity.objects.filter(user_email=user.email)
            total_points = sum(activity.points for activity in user_activities)
            user.total_points = total_points
            user.save()

        # Calculate total points for teams and update using Django ORM
        marvel_team = Team.objects.get(name="Team Marvel")
        dc_team = Team.objects.get(name="Team DC")
        
        marvel_activities = Activity.objects.filter(user_email__in=[u.email for u in users if u.team == "Team Marvel"])
        dc_activities = Activity.objects.filter(user_email__in=[u.email for u in users if u.team == "Team DC"])
        
        marvel_team.total_points = sum(activity.points for activity in marvel_activities)
        dc_team.total_points = sum(activity.points for activity in dc_activities)
        
        marvel_team.save()
        dc_team.save()

        # Create leaderboard entries
        leaderboard_data = []
        
        # Individual leaderboard
        for user in users:
            user_activities = Activity.objects.filter(user_email=user.email)
            total_points = sum(activity.points for activity in user_activities)
            leaderboard_data.append({
                "type": "individual",
                "name": user.name,
                "email": user.email,
                "team": user.team,
                "points": total_points,
                "rank": 0,  # Will be calculated after sorting
                "updated_at": timezone.now()
            })
        
        # Sort and assign ranks
        leaderboard_data.sort(key=lambda x: x["points"], reverse=True)
        for i, entry in enumerate(leaderboard_data, 1):
            entry["rank"] = i
        
        # Team leaderboard
        team_leaderboard = [
            {
                "type": "team",
                "name": "Team Marvel",
                "points": marvel_team.total_points,
                "rank": 1 if marvel_team.total_points > dc_team.total_points else 2,
                "updated_at": timezone.now()
            },
            {
                "type": "team",
                "name": "Team DC",
                "points": dc_team.total_points,
                "rank": 1 if dc_team.total_points > marvel_team.total_points else 2,
                "updated_at": timezone.now()
            }
        ]
        
        leaderboard_data.extend(team_leaderboard)
        
        # Insert leaderboard using Django ORM (bulk_create for efficiency)
        leaderboard_entries = [Leaderboard(**entry) for entry in leaderboard_data]
        Leaderboard.objects.bulk_create(leaderboard_entries)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(leaderboard_entries)} leaderboard entries'))

        # Sample workout recommendations
        workouts_data = [
            {
                "name": "Superhero Strength Training",
                "description": "Build strength like a superhero with this power-packed workout",
                "difficulty": "advanced",
                "duration": 45,
                "exercises": [
                    {"name": "Deadlifts", "sets": 4, "reps": 8},
                    {"name": "Bench Press", "sets": 4, "reps": 10},
                    {"name": "Pull-ups", "sets": 3, "reps": 12},
                    {"name": "Squats", "sets": 4, "reps": 10}
                ],
                "target_muscle_groups": ["chest", "back", "legs"],
                "created_at": timezone.now()
            },
            {
                "name": "Speed Force Cardio",
                "description": "Lightning-fast cardio workout for speed and endurance",
                "difficulty": "intermediate",
                "duration": 30,
                "exercises": [
                    {"name": "Sprint Intervals", "duration": "10 min"},
                    {"name": "Jump Rope", "duration": "5 min"},
                    {"name": "Burpees", "sets": 3, "reps": 15},
                    {"name": "Mountain Climbers", "sets": 3, "reps": 20}
                ],
                "target_muscle_groups": ["cardio", "legs", "core"],
                "created_at": timezone.now()
            },
            {
                "name": "Warrior Flexibility Flow",
                "description": "Improve flexibility and balance with this yoga-inspired routine",
                "difficulty": "beginner",
                "duration": 30,
                "exercises": [
                    {"name": "Sun Salutations", "sets": 5},
                    {"name": "Warrior Poses", "duration": "5 min"},
                    {"name": "Hip Openers", "duration": "5 min"},
                    {"name": "Cool Down Stretches", "duration": "5 min"}
                ],
                "target_muscle_groups": ["flexibility", "balance", "core"],
                "created_at": timezone.now()
            },
            {
                "name": "Combat Training Circuit",
                "description": "High-intensity circuit for combat readiness",
                "difficulty": "advanced",
                "duration": 40,
                "exercises": [
                    {"name": "Shadow Boxing", "duration": "5 min"},
                    {"name": "Heavy Bag Work", "duration": "5 min"},
                    {"name": "Plank Variations", "sets": 3, "duration": "1 min each"},
                    {"name": "Medicine Ball Slams", "sets": 4, "reps": 15}
                ],
                "target_muscle_groups": ["cardio", "core", "arms"],
                "created_at": timezone.now()
            },
            {
                "name": "Aquatic Endurance",
                "description": "Swimming-based workout for full-body conditioning",
                "difficulty": "intermediate",
                "duration": 45,
                "exercises": [
                    {"name": "Freestyle Swim", "distance": "400m"},
                    {"name": "Backstroke", "distance": "200m"},
                    {"name": "Butterfly", "distance": "100m"},
                    {"name": "Treading Water", "duration": "5 min"}
                ],
                "target_muscle_groups": ["full-body", "cardio", "endurance"],
                "created_at": timezone.now()
            }
        ]

        # Insert workouts using Django ORM (bulk_create for efficiency)
        workout_objects = [Workout(**workout_data) for workout_data in workouts_data]
        Workout.objects.bulk_create(workout_objects)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(workout_objects)} workout recommendations'))

        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Users: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Teams: {Team.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Activities: {Activity.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard entries: {Leaderboard.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts: {Workout.objects.count()}'))

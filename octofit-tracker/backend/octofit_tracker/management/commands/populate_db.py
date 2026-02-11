from django.core.management.base import BaseCommand
from pymongo import MongoClient
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['octofit_db']

        self.stdout.write(self.style.SUCCESS('Connected to MongoDB'))

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email field for users collection
        db.users.create_index([("email", 1)], unique=True)
        self.stdout.write(self.style.SUCCESS('Created unique index on email field'))

        # Sample superhero users data
        users_data = [
            # Team Marvel
            {
                "name": "Tony Stark",
                "email": "ironman@marvel.com",
                "team": "Team Marvel",
                "avatar": "🦾",
                "total_points": 0,
                "created_at": datetime.now()
            },
            {
                "name": "Steve Rogers",
                "email": "captain@marvel.com",
                "team": "Team Marvel",
                "avatar": "🛡️",
                "total_points": 0,
                "created_at": datetime.now()
            },
            {
                "name": "Natasha Romanoff",
                "email": "blackwidow@marvel.com",
                "team": "Team Marvel",
                "avatar": "🕷️",
                "total_points": 0,
                "created_at": datetime.now()
            },
            {
                "name": "Thor Odinson",
                "email": "thor@marvel.com",
                "team": "Team Marvel",
                "avatar": "⚡",
                "total_points": 0,
                "created_at": datetime.now()
            },
            {
                "name": "Bruce Banner",
                "email": "hulk@marvel.com",
                "team": "Team Marvel",
                "avatar": "💪",
                "total_points": 0,
                "created_at": datetime.now()
            },
            # Team DC
            {
                "name": "Bruce Wayne",
                "email": "batman@dc.com",
                "team": "Team DC",
                "avatar": "🦇",
                "total_points": 0,
                "created_at": datetime.now()
            },
            {
                "name": "Clark Kent",
                "email": "superman@dc.com",
                "team": "Team DC",
                "avatar": "🦸",
                "total_points": 0,
                "created_at": datetime.now()
            },
            {
                "name": "Diana Prince",
                "email": "wonderwoman@dc.com",
                "team": "Team DC",
                "avatar": "⭐",
                "total_points": 0,
                "created_at": datetime.now()
            },
            {
                "name": "Barry Allen",
                "email": "flash@dc.com",
                "team": "Team DC",
                "avatar": "⚡",
                "total_points": 0,
                "created_at": datetime.now()
            },
            {
                "name": "Arthur Curry",
                "email": "aquaman@dc.com",
                "team": "Team DC",
                "avatar": "🔱",
                "total_points": 0,
                "created_at": datetime.now()
            }
        ]

        # Insert users
        result = db.users.insert_many(users_data)
        user_ids = result.inserted_ids
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(user_ids)} users'))

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
                "created_at": datetime.now()
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
                "created_at": datetime.now()
            }
        ]

        # Insert teams
        result = db.teams.insert_many(teams_data)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(result.inserted_ids)} teams'))

        # Sample activities data
        activity_types = ["running", "cycling", "swimming", "weightlifting", "yoga", "boxing"]
        activities_data = []
        
        for user in users_data:
            # Generate 5-10 random activities per user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                days_ago = random.randint(1, 30)
                activity_date = datetime.now() - timedelta(days=days_ago)
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

        # Insert activities
        if activities_data:
            result = db.activities.insert_many(activities_data)
            self.stdout.write(self.style.SUCCESS(f'Inserted {len(result.inserted_ids)} activities'))

        # Calculate total points for users and update
        for user in users_data:
            user_activities = [a for a in activities_data if a["user_email"] == user["email"]]
            total_points = sum(a["points"] for a in user_activities)
            db.users.update_one(
                {"email": user["email"]},
                {"$set": {"total_points": total_points}}
            )

        # Calculate total points for teams and update
        marvel_members_emails = [u["email"] for u in users_data if u["team"] == "Team Marvel"]
        dc_members_emails = [u["email"] for u in users_data if u["team"] == "Team DC"]
        
        marvel_points = sum(a["points"] for a in activities_data if a["user_email"] in marvel_members_emails)
        dc_points = sum(a["points"] for a in activities_data if a["user_email"] in dc_members_emails)
        
        db.teams.update_one({"name": "Team Marvel"}, {"$set": {"total_points": marvel_points}})
        db.teams.update_one({"name": "Team DC"}, {"$set": {"total_points": dc_points}})

        # Create leaderboard entries
        leaderboard_data = []
        
        # Individual leaderboard
        for user in users_data:
            user_activities = [a for a in activities_data if a["user_email"] == user["email"]]
            total_points = sum(a["points"] for a in user_activities)
            leaderboard_data.append({
                "type": "individual",
                "name": user["name"],
                "email": user["email"],
                "team": user["team"],
                "points": total_points,
                "rank": 0,  # Will be calculated after sorting
                "updated_at": datetime.now()
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
                "points": marvel_points,
                "rank": 1 if marvel_points > dc_points else 2,
                "updated_at": datetime.now()
            },
            {
                "type": "team",
                "name": "Team DC",
                "points": dc_points,
                "rank": 1 if dc_points > marvel_points else 2,
                "updated_at": datetime.now()
            }
        ]
        
        leaderboard_data.extend(team_leaderboard)
        
        # Insert leaderboard
        result = db.leaderboard.insert_many(leaderboard_data)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(result.inserted_ids)} leaderboard entries'))

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
                "created_at": datetime.now()
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
                "created_at": datetime.now()
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
                "created_at": datetime.now()
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
                "created_at": datetime.now()
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
                "created_at": datetime.now()
            }
        ]

        # Insert workouts
        result = db.workouts.insert_many(workouts_data)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(result.inserted_ids)} workout recommendations'))

        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Users: {len(users_data)}'))
        self.stdout.write(self.style.SUCCESS(f'Teams: {len(teams_data)}'))
        self.stdout.write(self.style.SUCCESS(f'Activities: {len(activities_data)}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard entries: {len(leaderboard_data)}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts: {len(workouts_data)}'))
        
        client.close()

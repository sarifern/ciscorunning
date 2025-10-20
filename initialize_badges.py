from django.contrib.staticfiles.storage import staticfiles_storage
from badgify.models import Award, Badge

print("Initializing badges...")

# Distance milestones
badges_config = [
    ("ownK", "My milestone", "Congratulations! You achieved your goal", "img/own.jpg"),
    ("168K", "168K Milestone Achieved", "Impossible is nothing! You set a four marathon record", "img/168k.jpg"),
    ("126K", "126K Milestone Achieved", "Insane! You set a three marathon record", "img/126k.jpg"),
    ("84K", "84K Milestone Achieved", "You're on Fire!  You set a two marathon record", "img/84k.jpg"),
    ("42K", "42K Milestone Achieved", "You reached your goal! Give an extra mile!", "img/42k.jpg"),
    ("21K", "21K Award Unlocked", "Wow! You set a new half marathon personal record", "img/21k.jpg"),
    ("10K", "10K Record Smashed", "Congrats! You set a new 10k personal record", "img/10k.jpg"),
    ("7day-streak", "Week Warrior", "Amazing! You completed 7 consecutive days of workouts!", "img/trophy.svg"),
    ("14day-streak", "Fortnight Champion", "Incredible! You completed 14 consecutive days of workouts!", "img/reward.svg"),
    ("21day-streak", "Three Week Legend", "Outstanding! You completed 21 consecutive days of workouts!", "img/runner.svg"),
]

for slug, name, description, image_path in badges_config:
    badge, created = Badge.objects.get_or_create(
        slug=slug,
        defaults={
            'name': name,
            'description': description,
            'image': staticfiles_storage.open(image_path)
        }
    )
    if created:
        print(f"✓ Created badge: {name} ({slug})")
    else:
        print(f"- Badge already exists: {name} ({slug})")

print("\nBadge initialization complete!")

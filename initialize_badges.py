import os
from django.core.files import File
from django.conf import settings
from badgify.models import Award, Badge

print("Initializing badges...")

# Distance milestones
badges_config = [
    ("ownK", "My milestone", "Congratulations! You achieved your goal", "own.jpg"),
    ("168K", "168K Milestone Achieved", "Impossible is nothing! You set a four marathon record", "168k.jpg"),
    ("126K", "126K Milestone Achieved", "Insane! You set a three marathon record", "126k.jpg"),
    ("84K", "84K Milestone Achieved", "You're on Fire!  You set a two marathon record", "84k.jpg"),
    ("42K", "42K Milestone Achieved", "You reached your goal! Give an extra mile!", "42k.jpg"),
    ("21K", "21K Award Unlocked", "Wow! You set a new half marathon personal record", "21k.jpg"),
    ("10K", "10K Record Smashed", "Congrats! You set a new 10k personal record", "10k.jpg"),
    ("7day-streak", "Week Warrior", "Amazing! You completed 7 consecutive days of workouts!", "7DayStreak.svg"),
    ("14day-streak", "Fortnight Champion", "Incredible! You completed 14 consecutive days of workouts!", "14DayStreak.svg"),
    ("21day-streak", "Three Week Legend", "Outstanding! You completed 21 consecutive days of workouts!", "21DayStreak.svg"),
]

# Get the path to the static img directory
static_img_path = os.path.join(settings.BASE_DIR, 'ic_marathon_app', 'static', 'img')

for slug, name, description, image_filename in badges_config:
    # Check if badge already exists
    try:
        badge = Badge.objects.get(slug=slug)
        print(f"- Badge already exists: {name} ({slug})")
        continue
    except Badge.DoesNotExist:
        pass
    
    # Full path to the image file
    image_path = os.path.join(static_img_path, image_filename)
    
    if not os.path.exists(image_path):
        print(f"✗ Image not found: {image_path}")
        continue
    
    # Open the image file and create the badge
    with open(image_path, 'rb') as img_file:
        badge = Badge.objects.create(
            slug=slug,
            name=name,
            description=description,
        )
        # Save the image to the badge's image field (will upload to S3 if configured)
        badge.image.save(image_filename, File(img_file), save=True)
        print(f"✓ Created badge: {name} ({slug}) - Image uploaded to S3")

print("\nBadge initialization complete!")

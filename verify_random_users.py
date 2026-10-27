import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ic_marathon_site.settings')
django.setup()

from ic_marathon_app.models import Profile, Workout
from datetime import datetime, timedelta
import pytz

# Pick some random users with workouts
profiles_with_workouts = Profile.objects.filter(
    id__in=Workout.objects.values_list('belongs_to_id', flat=True).distinct()
)

# Select 5 random profiles
sample_profiles = random.sample(list(profiles_with_workouts), min(5, profiles_with_workouts.count()))

mexico_tz = pytz.timezone('America/Mexico_City')
brazil_tz = pytz.timezone('America/Sao_Paulo')

for profile in sample_profiles:
    print(f"\n{'=' * 100}")
    print(f"USER: {profile.cec}")
    print(f"{'=' * 100}")
    print(f"Current streak: {profile.current_streak} | Longest streak: {profile.longest_streak}")
    
    workouts = Workout.objects.filter(belongs_to=profile).order_by('date_time')
    print(f"Total workouts: {workouts.count()}")
    
    # Calculate dates in local timezone
    dates_set = set()
    print(f"\nRecent workouts (last 15):")
    print(f"{'-' * 100}")
    
    for workout in workouts[:15]:
        # All workouts are in UTC, convert to local timezone
        if profile.cec == 'wrocha':
            local_date = workout.date_time.astimezone(brazil_tz).date()
            tz_info = "Brazil"
        else:
            local_date = workout.date_time.astimezone(mexico_tz).date()
            tz_info = "Mexico"
        
        dates_set.add(local_date)
        print(f"  {workout.date_time} -> {local_date} [{tz_info}] | {workout.distance:.2f} km")
    
    if workouts.count() > 15:
        print(f"  ... and {workouts.count() - 15} more workouts")
    
    # Get all dates
    all_dates = set()
    for workout in workouts:
        # All workouts are in UTC, convert to local timezone
        if profile.cec == 'wrocha':
            local_date = workout.date_time.astimezone(brazil_tz).date()
        else:
            local_date = workout.date_time.astimezone(mexico_tz).date()
        all_dates.add(local_date)
    
    dates_list = sorted(list(all_dates))
    print(f"\nUnique workout dates: {len(dates_list)}")
    
    # Find longest streak manually
    longest = 1
    current = 1
    for i in range(1, len(dates_list)):
        if (dates_list[i] - dates_list[i-1]).days == 1:
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    
    # Find current streak
    if profile.cec == 'wrocha':
        today = datetime.now(brazil_tz).date()
    else:
        today = datetime.now(mexico_tz).date()
    
    most_recent = dates_list[-1]
    days_since_last = (today - most_recent).days
    
    if days_since_last <= 1:
        current_streak = 1
        for i in range(len(dates_list) - 2, -1, -1):
            if (dates_list[i+1] - dates_list[i]).days == 1:
                current_streak += 1
            else:
                break
    else:
        current_streak = 0
    
    print(f"\nManual calculation:")
    print(f"  Current streak: {current_streak} (DB shows: {profile.current_streak}) {'✓' if current_streak == profile.current_streak else '✗ MISMATCH'}")
    print(f"  Longest streak: {longest} (DB shows: {profile.longest_streak}) {'✓' if longest == profile.longest_streak else '✗ MISMATCH'}")
    print(f"  Today: {today}")
    print(f"  Most recent workout: {most_recent}")
    print(f"  Days since last: {days_since_last}")

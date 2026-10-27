"""
Recalculate workout_days_count for all users using the correct method
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ic_marathon_site.settings')
django.setup()

from ic_marathon_app.models import Profile, Workout

print("=" * 100)
print("RECALCULATING workout_days_count FOR ALL USERS")
print("=" * 100)

profiles = Profile.objects.all()
updated_count = 0
mismatches = []

for profile in profiles:
    old_count = profile.workout_days_count
    
    # Use Django's dates() method (correct method)
    new_count = Workout.objects.filter(belongs_to=profile).dates('date_time', 'day').count()
    
    if old_count != new_count:
        mismatches.append({
            'cec': profile.cec,
            'old': old_count,
            'new': new_count,
            'diff': new_count - old_count
        })
        
        profile.workout_days_count = new_count
        profile.save()
        updated_count += 1

print(f"\nTotal profiles checked: {profiles.count()}")
print(f"Profiles with mismatches: {len(mismatches)}")
print(f"Profiles updated: {updated_count}")

if mismatches:
    print("\n" + "=" * 100)
    print("MISMATCHES FOUND AND CORRECTED:")
    print("=" * 100)
    
    # Sort by difference (largest first)
    mismatches.sort(key=lambda x: abs(x['diff']), reverse=True)
    
    for m in mismatches:
        symbol = "+" if m['diff'] > 0 else ""
        print(f"  {m['cec']:20s} | Old: {m['old']:3d} -> New: {m['new']:3d} | Diff: {symbol}{m['diff']:2d}")
    
    print(f"\n✅ Updated {updated_count} profiles with corrected workout_days_count")
else:
    print("\n✅ All profiles already have correct workout_days_count!")

from django.core.management.base import BaseCommand
from django.db.models import Sum
from ic_marathon_app.models import Profile, Workout
from decimal import Decimal


class Command(BaseCommand):
    help = 'Verify that profile distances match the sum of their workout distances'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Fix discrepancies by updating profile distances',
        )
        parser.add_argument(
            '--tolerance',
            type=float,
            default=0.01,
            help='Tolerance for distance differences (default: 0.01 km)',
        )

    def handle(self, *args, **options):
        fix_mode = options['fix']
        tolerance = Decimal(str(options['tolerance']))
        
        profiles = Profile.objects.all()
        total_profiles = profiles.count()
        discrepancies = []
        fixed_count = 0
        
        self.stdout.write(f"Checking {total_profiles} profiles...")
        self.stdout.write(f"Tolerance: ±{tolerance} km")
        if fix_mode:
            self.stdout.write(self.style.WARNING("FIX MODE: Will update incorrect distances\n"))
        else:
            self.stdout.write("DRY RUN: Use --fix to update distances\n")
        
        for profile in profiles:
            # Get sum of all workout distances for this profile
            workout_sum = Workout.objects.filter(belongs_to=profile).aggregate(
                total=Sum('distance')
            )['total'] or Decimal('0.00')
            
            # Compare with profile's stored distance
            stored_distance = profile.distance
            difference = abs(workout_sum - stored_distance)
            
            if difference > tolerance:
                discrepancies.append({
                    'cec': profile.cec,
                    'stored': stored_distance,
                    'actual': workout_sum,
                    'difference': difference,
                    'workout_count': Workout.objects.filter(belongs_to=profile).count()
                })
                
                if fix_mode:
                    profile.distance = workout_sum
                    profile.save()
                    fixed_count += 1
        
        # Report results
        self.stdout.write("=" * 100)
        if discrepancies:
            self.stdout.write(self.style.WARNING(f"\n⚠️  Found {len(discrepancies)} profiles with distance discrepancies:\n"))
            
            for item in discrepancies:
                self.stdout.write(
                    f"  {item['cec']:15} | "
                    f"Stored: {item['stored']:8.2f} km | "
                    f"Actual: {item['actual']:8.2f} km | "
                    f"Diff: {item['difference']:6.2f} km | "
                    f"Workouts: {item['workout_count']}"
                )
            
            if fix_mode:
                self.stdout.write(
                    self.style.SUCCESS(f"\n✅ Fixed {fixed_count} profile distances")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"\n💡 Run with --fix to update these distances")
                )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"\n✅ All profile distances are correct!")
            )
        
        # Summary
        self.stdout.write("\n" + "=" * 100)
        self.stdout.write(f"Total profiles checked: {total_profiles}")
        self.stdout.write(f"Discrepancies found: {len(discrepancies)}")
        if fix_mode:
            self.stdout.write(f"Profiles fixed: {fixed_count}")
        self.stdout.write(f"Correct profiles: {total_profiles - len(discrepancies)}")

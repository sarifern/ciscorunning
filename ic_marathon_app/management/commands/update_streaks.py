from django.core.management.base import BaseCommand
from django.utils import timezone
from ic_marathon_app.models import Profile, Workout
from badgify.models import Award, Badge
from datetime import datetime, timedelta
import pytz


class Command(BaseCommand):
    help = 'Update workout streaks for all users. Run this command every 10 minutes via cron/scheduler.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Print detailed information about streak updates',
        )

    def handle(self, *args, **options):
        verbose = options['verbose']
        
        profiles = Profile.objects.all()
        total_profiles = profiles.count()
        updated_count = 0
        broken_streaks = 0
        new_records = 0
        badges_awarded = 0
        
        self.stdout.write(f"Starting streak update for {total_profiles} profiles...")
        
        for profile in profiles:
            old_current_streak = profile.current_streak
            old_longest_streak = profile.longest_streak
            
            # Calculate current streaks WITH timezone correction
            current_streak, longest_streak = self.calculate_streaks_with_correction(profile)
            
            # Check if anything changed
            if current_streak != old_current_streak or longest_streak != old_longest_streak:
                profile.current_streak = current_streak
                profile.longest_streak = longest_streak
                profile.save()
                updated_count += 1
                
                # Track broken streaks
                if old_current_streak > 0 and current_streak == 0:
                    broken_streaks += 1
                    if verbose:
                        self.stdout.write(
                            self.style.WARNING(
                                f"💔 {profile.cec}: Streak broken! Was {old_current_streak} days"
                            )
                        )
                
                # Track new personal records
                if longest_streak > old_longest_streak:
                    new_records += 1
                    if verbose:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"🏆 {profile.cec}: New personal record! {longest_streak} days (was {old_longest_streak})"
                            )
                        )
                
                # Log milestone streaks
                if verbose and current_streak > 0 and current_streak % 7 == 0 and current_streak != old_current_streak:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"🔥 {profile.cec}: Hit a {current_streak}-day streak milestone!"
                        )
                    )
                
                # Award streak badges based on longest_streak
                # Badges are awarded once and kept forever (based on longest streak achieved)
                user = profile.user
                new_badges = self.award_streak_badges(user, longest_streak, old_longest_streak, verbose)
                badges_awarded += len(new_badges)
        
        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Streak update complete!"
            )
        )
        self.stdout.write(f"   Total profiles: {total_profiles}")
        self.stdout.write(f"   Updated: {updated_count}")
        self.stdout.write(f"   Broken streaks: {broken_streaks}")
        self.stdout.write(f"   New records: {new_records}")
        self.stdout.write(f"   Badges awarded: {badges_awarded}")
        self.stdout.write(f"   Unchanged: {total_profiles - updated_count}")
    
    def calculate_streaks_with_correction(self, profile):
        """
        Calculate streaks with timezone correction for old workouts.
        
        IMPORTANT: Workouts submitted before Dec 22, 2025 19:11 UTC were stored
        with incorrect timezone info (local Mexico time saved as UTC).
        We correct this in the calculation WITHOUT modifying stored data
        to preserve what users see in the admin/UI.
        
        Streak logic: Workouts within 30 hours (1 day + 6 hours) maintain the streak.
        Each workout counts as 1 day in the streak.
        
        Args:
            profile: User profile to calculate streaks for
            
        Returns:
            Tuple of (current_streak, longest_streak)
        """
        # Cutoff for timezone fix: Dec 22, 2025 at 19:11:04 UTC
        TIMEZONE_FIX_CUTOFF = datetime(2025, 12, 22, 19, 11, 0, tzinfo=pytz.UTC)
        STREAK_THRESHOLD_HOURS = 30  # 1 day + 6 hours flexibility
        
        # Get all workouts for this profile
        workouts = Workout.objects.filter(belongs_to=profile).order_by('date_time')
        
        if not workouts:
            return 0, 0
        
        # Get workout datetimes with timezone correction (keep as datetimes, not dates)
        corrected_datetimes = []
        for workout in workouts:
            # Special correction for user 'wrocha' (Brazil/São Paulo, UTC-3)
            if profile.cec == 'wrocha' and workout.date_time < TIMEZONE_FIX_CUTOFF:
                # Old workout from Brazil: ADD 3 hours to get correct UTC
                corrected_time = workout.date_time + timedelta(hours=3)
                corrected_datetimes.append(corrected_time.astimezone(timezone.utc))
            elif workout.date_time < TIMEZONE_FIX_CUTOFF:
                # Old workout from Mexico: ADD 6 hours to get correct UTC
                corrected_time = workout.date_time + timedelta(hours=6)
                corrected_datetimes.append(corrected_time.astimezone(timezone.utc))
            else:
                # New workout: already has correct timezone
                corrected_datetimes.append(workout.date_time.astimezone(timezone.utc))
        
        # Sort by datetime
        corrected_datetimes.sort()
        
        # Remove duplicate dates (multiple workouts on same day = count as 1)
        unique_date_workouts = []
        seen_dates = set()
        for dt in corrected_datetimes:
            date = dt.date()
            if date not in seen_dates:
                seen_dates.add(date)
                unique_date_workouts.append(dt)
        
        # Calculate longest streak based on 30-hour threshold between unique-date workouts
        longest = 1
        current = 1
        
        for i in range(1, len(unique_date_workouts)):
            time_diff = unique_date_workouts[i] - unique_date_workouts[i-1]
            hours_diff = time_diff.total_seconds() / 3600
            
            if hours_diff <= STREAK_THRESHOLD_HOURS:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        
        # Calculate current streak
        now = timezone.now().astimezone(timezone.utc)
        current_streak = 0
        
        if unique_date_workouts:
            most_recent = unique_date_workouts[-1]
            hours_since_last = (now - most_recent).total_seconds() / 3600
            
            if hours_since_last <= STREAK_THRESHOLD_HOURS:
                current_streak = 1
                for i in range(len(unique_date_workouts) - 2, -1, -1):
                    time_diff = unique_date_workouts[i+1] - unique_date_workouts[i]
                    hours_diff = time_diff.total_seconds() / 3600
                    
                    if hours_diff <= STREAK_THRESHOLD_HOURS:
                        current_streak += 1
                    else:
                        break
            else:
                current_streak = 0
        
        return current_streak, longest
    
    def award_streak_badges(self, user, longest_streak, old_longest_streak, verbose):
        """
        Award streak badges based on longest streak achieved.
        Badges are permanent and based on longest_streak, not current_streak.
        
        Args:
            user: Django User object
            longest_streak: Current longest streak value
            old_longest_streak: Previous longest streak value
            verbose: Whether to print detailed output
            
        Returns:
            List of newly awarded badges
        """
        new_badges = []
        
        # Only award badges if longest_streak actually increased
        # This prevents re-awarding badges on every run
        if longest_streak <= old_longest_streak:
            return new_badges
        
        # Define streak milestones and their badge slugs
        streak_badges = [
            (7, "7day-streak", "Week Warrior"),
            (14, "14day-streak", "Fortnight Champion"),
            (21, "21day-streak", "Three Week Legend"),
        ]
        
        for threshold, slug, name in streak_badges:
            # Award badge if user reached this threshold and didn't have it before
            if longest_streak >= threshold and old_longest_streak < threshold:
                # Check if badge already exists
                existing_award = Award.objects.filter(user=user, badge__slug=slug).first()
                
                if not existing_award:
                    try:
                        badge = Badge.objects.get(slug=slug)
                        award = Award.objects.create(user=user, badge=badge)
                        new_badges.append(award)
                        
                        if verbose:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"🏅 {user.profile.cec}: Awarded '{name}' badge!"
                                )
                            )
                    except Badge.DoesNotExist:
                        if verbose:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"⚠️  Badge '{slug}' not found in database. Run initialize_badges.py first."
                                )
                            )
        
        return new_badges

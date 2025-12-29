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
        
        Streak logic: Based on calendar days - any workout on a day counts.
        Consecutive calendar days = maintained streak, regardless of time.
        
        Args:
            profile: User profile to calculate streaks for
            
        Returns:
            Tuple of (current_streak, longest_streak)
        """
        # Cutoff for timezone fix: Dec 22, 2025 at 19:11:04 UTC
        TIMEZONE_FIX_CUTOFF = datetime(2025, 12, 22, 19, 11, 0, tzinfo=pytz.UTC)
        
        # Get all workouts for this profile
        workouts = Workout.objects.filter(belongs_to=profile).order_by('date_time')
        
        if not workouts:
            return 0, 0
        
        # Extract unique dates with timezone correction
        dates_set = set()
        for workout in workouts:
            # Special correction for user 'wrocha' (Brazil/São Paulo, UTC-3)
            if profile.cec == 'wrocha' and workout.date_time < TIMEZONE_FIX_CUTOFF:
                # Old workout from Brazil: ADD 3 hours to get correct UTC date
                corrected_time = workout.date_time + timedelta(hours=3)
                utc_date = corrected_time.astimezone(timezone.utc).date()
            elif workout.date_time < TIMEZONE_FIX_CUTOFF:
                # Old workout from Mexico: ADD 6 hours to get correct UTC date
                corrected_time = workout.date_time + timedelta(hours=6)
                utc_date = corrected_time.astimezone(timezone.utc).date()
            else:
                # New workout: already has correct timezone
                utc_date = workout.date_time.astimezone(timezone.utc).date()
            
            dates_set.add(utc_date)
        
        # Convert to sorted list
        dates_list = sorted(list(dates_set))
        
        # Calculate longest streak based on consecutive calendar days
        longest = 1
        current = 1
        
        for i in range(1, len(dates_list)):
            if (dates_list[i] - dates_list[i-1]).days == 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        
        # Calculate current streak
        today = timezone.now().astimezone(timezone.utc).date()
        current_streak = 0
        
        if dates_list:
            most_recent = dates_list[-1]
            days_since_last = (today - most_recent).days
            
            # Allow today or yesterday to maintain streak
            if days_since_last <= 1:
                current_streak = 1
                for i in range(len(dates_list) - 2, -1, -1):
                    if (dates_list[i+1] - dates_list[i]).days == 1:
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

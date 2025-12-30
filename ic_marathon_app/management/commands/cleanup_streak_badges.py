from django.core.management.base import BaseCommand
from ic_marathon_app.models import Profile
from badgify.models import Award, Badge


class Command(BaseCommand):
    help = 'Remove streak and distance badges from users who no longer qualify'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be removed without actually removing',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN MODE - No changes will be made"))
        
        total_removed = 0
        
        # Clean up streak badges
        self.stdout.write(self.style.SUCCESS("\n=== Checking Streak Badges ==="))
        streak_removed = self.cleanup_streak_badges(dry_run)
        total_removed += streak_removed
        
        # Clean up distance badges
        self.stdout.write(self.style.SUCCESS("\n=== Checking Distance Badges ==="))
        distance_removed = self.cleanup_distance_badges(dry_run)
        total_removed += distance_removed
        
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Cleanup complete! Total badges removed: {total_removed}"
            )
        )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    "\nThis was a DRY RUN. Run without --dry-run to actually remove badges."
                )
            )
    
    def cleanup_streak_badges(self, dry_run):
        """Remove streak badges from users who no longer qualify"""
    def cleanup_streak_badges(self, dry_run):
        """Remove streak badges from users who no longer qualify"""
        # Define streak badges
        streak_badges = [
            (7, "7day-streak", "Week Warrior"),
            (14, "14day-streak", "Fortnight Champion"),
            (21, "21day-streak", "Three Week Legend"),
        ]
        
        total_removed = 0
        
        for threshold, slug, name in streak_badges:
            badge = Badge.objects.filter(slug=slug).first()
            if not badge:
                continue
            
            # Find users who have the badge but shouldn't
            awards = Award.objects.filter(badge=badge)
            removed_count = 0
            
            for award in awards:
                profile = award.user.profile
                if profile.longest_streak < threshold:
                    removed_count += 1
                    total_removed += 1
                    
                    self.stdout.write(
                        f"  Removing {slug} from {profile.cec} (longest_streak={profile.longest_streak}, required={threshold})"
                    )
                    
                    if not dry_run:
                        award.delete()
            
            if removed_count > 0:
                self.stdout.write(
                    self.style.WARNING(
                        f"\n{name} ({slug}): Removed {removed_count} incorrect awards"
                    )
                )
        
        return total_removed
    
    def cleanup_distance_badges(self, dry_run):
        """Remove distance badges from users who no longer qualify"""
        # Define distance badges (km_required, slug, name)
        distance_badges = [
            (10.0, "10K", "10K Challenge"),
            (21.0, "21K", "Half Marathon"),
            (42.0, "42K", "Marathon"),
            (84.0, "84K", "Double Marathon"),
            (126.0, "126K", "Triple Marathon"),
            (168.0, "168K", "Quad Marathon"),
        ]
        
        total_removed = 0
        
        for threshold, slug, name in distance_badges:
            badge = Badge.objects.filter(slug=slug).first()
            if not badge:
                continue
            
            # Find users who have the badge but shouldn't
            awards = Award.objects.filter(badge=badge)
            removed_count = 0
            
            for award in awards:
                profile = award.user.profile
                if profile.distance < threshold:
                    removed_count += 1
                    total_removed += 1
                    
                    self.stdout.write(
                        f"  Removing {slug} from {profile.cec} (distance={profile.distance} km, required={threshold} km)"
                    )
                    
                    if not dry_run:
                        award.delete()
            
            if removed_count > 0:
                self.stdout.write(
                    self.style.WARNING(
                        f"\n{name} ({slug}): Removed {removed_count} incorrect awards"
                    )
                )
        
        # Check ownK badge separately (user goal)
        badge = Badge.objects.filter(slug="ownK").first()
        if badge:
            awards = Award.objects.filter(badge=badge)
            removed_count = 0
            
            for award in awards:
                profile = award.user.profile
                if profile.distance < profile.user_goal_km:
                    removed_count += 1
                    total_removed += 1
                    
                    self.stdout.write(
                        f"  Removing ownK from {profile.cec} (distance={profile.distance} km, goal={profile.user_goal_km} km)"
                    )
                    
                    if not dry_run:
                        award.delete()
            
            if removed_count > 0:
                self.stdout.write(
                    self.style.WARNING(
                        f"\nPersonal Goal (ownK): Removed {removed_count} incorrect awards"
                    )
                )
        
        return total_removed

from django.core.management.base import BaseCommand
from ic_marathon_app.models import Profile
from badgify.models import Award, Badge


class Command(BaseCommand):
    help = 'Remove streak badges from users who no longer qualify after timezone correction'

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

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from ic_marathon_app.models import Workout


class Command(BaseCommand):
    help = 'Delete expired unconfirmed partner workout requests (older than 2 days)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Find unconfirmed partner workouts older than 2 days
        expiration_threshold = timezone.now() - timedelta(days=2)
        
        expired_workouts = Workout.objects.filter(
            is_partner_workout=True,
            partner_confirmed=False,
            uploaded_at__lt=expiration_threshold
        )
        
        count = expired_workouts.count()
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'[DRY RUN] Would delete {count} expired partner workout(s)')
            )
            for workout in expired_workouts:
                self.stdout.write(
                    f'  - Workout {workout.uuid} from {workout.belongs_to.cec} '
                    f'to {workout.partner_profile.cec} '
                    f'(created {workout.uploaded_at})'
                )
        else:
            expired_workouts.delete()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {count} expired partner workout(s)')
            )

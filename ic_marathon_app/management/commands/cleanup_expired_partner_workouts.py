from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from ic_marathon_app.models import Workout


class Command(BaseCommand):
    help = 'Converts expired unconfirmed partner workouts to solo workouts'

    def handle(self, *args, **options):
        # Find all unconfirmed partner workouts older than 48 hours
        expiration_threshold = timezone.now() - timedelta(hours=48)
        
        expired_workouts = Workout.objects.filter(
            is_partner_workout=True,
            partner_confirmed=False,
            uploaded_at__lt=expiration_threshold
        )
        
        count = expired_workouts.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No expired partner workouts found.'))
            return
        
        # Convert each expired workout to solo workout
        for workout in expired_workouts:
            original_owner = workout.belongs_to.cec
            base_distance = workout.base_distance
            
            # Convert to solo workout (no bonus)
            workout.is_partner_workout = False
            workout.partner_confirmed = False
            workout.distance = workout.base_distance
            workout.partner_profile = None
            workout.partner_workout_group = None
            workout.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Converted expired partner workout to solo: {original_owner} - {base_distance}km'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully converted {count} expired partner workout(s) to solo workouts.'
            )
        )

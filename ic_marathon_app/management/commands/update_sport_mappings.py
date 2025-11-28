from django.core.management.base import BaseCommand
from ic_marathon_app.models import Sport, IntensityLevel, SportIntensityMapping


class Command(BaseCommand):
    help = 'Update sport intensity mappings to match prorrateo.csv values'

    def handle(self, *args, **options):
        # Get intensity levels
        try:
            low = IntensityLevel.objects.get(name='Low')
            moderate = IntensityLevel.objects.get(name='Moderate')
            high = IntensityLevel.objects.get(name='High')
        except IntensityLevel.DoesNotExist:
            self.stdout.write(self.style.ERROR('Intensity levels not found!'))
            return

        # Define mappings from prorrateo.csv
        mappings = {
            # Group 1: 10, 8.5, 7
            'Running': {'High': 10, 'Moderate': 8.5, 'Low': 7},
            'Biking': {'High': 10, 'Moderate': 8.5, 'Low': 7},
            'Swimming': {'High': 10, 'Moderate': 8.5, 'Low': 7},
            'Crossfit': {'High': 10, 'Moderate': 8.5, 'Low': 7},
            'Calisthenics': {'High': 10, 'Moderate': 8.5, 'Low': 7},
            
            # Group 2: 9, 7.65, 6.3
            'Weightlifting': {'High': 9, 'Moderate': 7.65, 'Low': 6.3},
            'Boxing': {'High': 9, 'Moderate': 7.65, 'Low': 6.3},
            'Soccer': {'High': 9, 'Moderate': 7.65, 'Low': 6.3},
            'Basketball': {'High': 9, 'Moderate': 7.65, 'Low': 6.3},
            'Volleyball': {'High': 9, 'Moderate': 7.65, 'Low': 6.3},
            'Tennis': {'High': 9, 'Moderate': 7.65, 'Low': 6.3},
            
            # Group 3: 8, 6.8, 5.6
            'Yoga': {'High': 8, 'Moderate': 6.8, 'Low': 5.6},
            'Pilates': {'High': 8, 'Moderate': 6.8, 'Low': 5.6},
            'Zumba': {'High': 8, 'Moderate': 6.8, 'Low': 5.6},
            'Dancing': {'High': 8, 'Moderate': 6.8, 'Low': 5.6},
            'Hiking': {'High': 8, 'Moderate': 6.8, 'Low': 5.6},
            'Elliptical': {'High': 8, 'Moderate': 6.8, 'Low': 5.6},
            'Bowling': {'High': 8, 'Moderate': 6.8, 'Low': 5.6},
            'Pole dancing': {'High': 8, 'Moderate': 6.8, 'Low': 5.6},
            'Rowing': {'High': 8, 'Moderate': 6.8, 'Low': 5.6},
            'Other': {'High': 8, 'Moderate': 6.8, 'Low': 5.6},
        }

        updated_count = 0
        for sport_name, intensity_values in mappings.items():
            try:
                sport = Sport.objects.get(name=sport_name)
                
                # Update High intensity
                mapping, created = SportIntensityMapping.objects.get_or_create(
                    sport=sport,
                    intensity=high,
                    defaults={'km_per_hour': intensity_values['High']}
                )
                if not created and mapping.km_per_hour != intensity_values['High']:
                    old_value = mapping.km_per_hour
                    mapping.km_per_hour = intensity_values['High']
                    mapping.save()
                    self.stdout.write(f"  {sport_name} - High: {old_value} -> {intensity_values['High']}")
                    updated_count += 1
                
                # Update Moderate intensity
                mapping, created = SportIntensityMapping.objects.get_or_create(
                    sport=sport,
                    intensity=moderate,
                    defaults={'km_per_hour': intensity_values['Moderate']}
                )
                if not created and mapping.km_per_hour != intensity_values['Moderate']:
                    old_value = mapping.km_per_hour
                    mapping.km_per_hour = intensity_values['Moderate']
                    mapping.save()
                    self.stdout.write(f"  {sport_name} - Moderate: {old_value} -> {intensity_values['Moderate']}")
                    updated_count += 1
                
                # Update Low intensity
                mapping, created = SportIntensityMapping.objects.get_or_create(
                    sport=sport,
                    intensity=low,
                    defaults={'km_per_hour': intensity_values['Low']}
                )
                if not created and mapping.km_per_hour != intensity_values['Low']:
                    old_value = mapping.km_per_hour
                    mapping.km_per_hour = intensity_values['Low']
                    mapping.save()
                    self.stdout.write(f"  {sport_name} - Low: {old_value} -> {intensity_values['Low']}")
                    updated_count += 1
                    
            except Sport.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Sport not found: {sport_name}'))

        if updated_count > 0:
            self.stdout.write(self.style.SUCCESS(f'\nSuccessfully updated {updated_count} sport intensity mappings!'))
        else:
            self.stdout.write(self.style.SUCCESS('All sport intensity mappings are already up to date!'))

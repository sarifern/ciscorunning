# Generated migration to update sport intensity mappings to match prorrateo.csv
from django.db import migrations

def update_sport_intensity_mappings(apps, schema_editor):
    Sport = apps.get_model('ic_marathon_app', 'Sport')
    IntensityLevel = apps.get_model('ic_marathon_app', 'IntensityLevel')
    SportIntensityMapping = apps.get_model('ic_marathon_app', 'SportIntensityMapping')

    # Update intensity level names from 'Light' to 'Low' if needed
    try:
        light_intensity = IntensityLevel.objects.get(name='Light')
        light_intensity.name = 'Low'
        light_intensity.save()
    except IntensityLevel.DoesNotExist:
        pass

    # Ensure all intensity levels exist with correct names
    IntensityLevel.objects.get_or_create(name='Low')
    IntensityLevel.objects.get_or_create(name='Moderate')
    IntensityLevel.objects.get_or_create(name='High')

    # Sports list matching prorrateo.csv
    sports_data = [
        "Running", "Biking", "Swimming", "Crossfit", "Calisthenics",
        "Weightlifting", "Boxing", "Soccer", "Basketball", "Volleyball",
        "Tennis", "Yoga", "Pilates", "Zumba", "Dancing",
        "Hiking", "Elliptical", "Bowling", "Pole dancing", "Rowing", "Other"
    ]
    
    intensity_map = {
        "Low": 0,
        "Moderate": 1,
        "High": 2,
    }
    
    # km/hr mapping from prorrateo.csv
    # Format: [Low (70%), Moderate (85%), High (100%)]
    km_data = {
        "Running":        [7.0, 8.5, 10.0],
        "Biking":         [7.0, 8.5, 10.0],
        "Swimming":       [7.0, 8.5, 10.0],
        "Crossfit":       [7.0, 8.5, 10.0],
        "Calisthenics":   [7.0, 8.5, 10.0],
        "Weightlifting":  [6.3, 7.65, 9.0],
        "Boxing":         [6.3, 7.65, 9.0],
        "Soccer":         [6.3, 7.65, 9.0],
        "Basketball":     [6.3, 7.65, 9.0],
        "Volleyball":     [6.3, 7.65, 9.0],
        "Tennis":         [6.3, 7.65, 9.0],
        "Yoga":           [5.6, 6.8, 8.0],
        "Pilates":        [5.6, 6.8, 8.0],
        "Zumba":          [5.6, 6.8, 8.0],
        "Dancing":        [5.6, 6.8, 8.0],
        "Hiking":         [5.6, 6.8, 8.0],
        "Elliptical":     [5.6, 6.8, 8.0],
        "Bowling":        [5.6, 6.8, 8.0],
        "Pole dancing":   [5.6, 6.8, 8.0],
        "Rowing":         [5.6, 6.8, 8.0],
        "Other":          [5.6, 6.8, 8.0],
    }

    # Update or create sports and their intensity mappings
    for sport_name in sports_data:
        sport, _ = Sport.objects.get_or_create(name=sport_name)
        
        for intensity_name in ["Low", "Moderate", "High"]:
            intensity_obj = IntensityLevel.objects.get(name=intensity_name)
            km_per_hour = km_data[sport_name][intensity_map[intensity_name]]
            
            # Update existing mapping or create new one
            mapping, created = SportIntensityMapping.objects.get_or_create(
                sport=sport,
                intensity=intensity_obj,
                defaults={'km_per_hour': km_per_hour}
            )
            
            # If it already exists, update the km_per_hour value
            if not created and mapping.km_per_hour != km_per_hour:
                mapping.km_per_hour = km_per_hour
                mapping.save()

def reverse_update(apps, schema_editor):
    # Optionally define a reverse operation if needed
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('ic_marathon_app', '0007_profile_current_streak_profile_first_workout_date_and_more'),
    ]

    operations = [
        migrations.RunPython(update_sport_intensity_mappings, reverse_update),
    ]

# Generated by Django 2.2.3 on 2019-09-18 22:38

from django.db import migrations, models
import ic_marathon_app.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ic_marathon_app', '0011_workout_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='time',
            field=models.IntegerField(help_text='Workout in minutes', validators=[ic_marathon_app.validators.validate_workout_time]),
        ),
    ]

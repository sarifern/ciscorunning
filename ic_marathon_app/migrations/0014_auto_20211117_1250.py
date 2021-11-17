# Generated by Django 2.2.13 on 2021-11-17 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ic_marathon_app', '0013_workout_intensity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='intensity',
            field=models.CharField(choices=[('light', 'Light'), ('medium', 'Medium'), ('high', 'High')], default='medium', max_length=10, verbose_name='Intensity'),
        ),
    ]

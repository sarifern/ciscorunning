# Generated by Django 4.2.7 on 2025-07-24 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ic_marathon_app', '0019_rename_audited_workout_is_audited_workout_is_gift_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='category',
            field=models.CharField(choices=[('beginnerrunner', 'Beginner Runner'), ('runner', 'Runner'), ('biker', 'Biker'), ('freestyler', 'Freestyler'), ('advfreestyler', 'Advanced Freestyler')], default='beginnerrunner', max_length=20),
        ),
        migrations.AlterField(
            model_name='workout',
            name='date_time',
            field=models.DateTimeField(verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='time',
            field=models.TimeField(default='00:00', help_text='Workout/Gift', verbose_name='Type'),
        ),
    ]

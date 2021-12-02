# Generated by Django 2.2.13 on 2021-12-01 19:44

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ic_marathon_app', '0015_auto_20211201_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='distance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_goal_km',
            field=models.DecimalField(decimal_places=2, default=42.0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('21.0'))]),
        ),
    ]

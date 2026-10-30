from django.core.management import call_command
from django.db import migrations

CACHE_TABLES = ["django_cache_table", "select2_cache_table"]


def create_cache_tables(apps, schema_editor):
    for table_name in CACHE_TABLES:
        call_command("createcachetable", table_name)


def drop_cache_tables(apps, schema_editor):
    for table_name in CACHE_TABLES:
        schema_editor.execute(f"DROP TABLE IF EXISTS {table_name}")


class Migration(migrations.Migration):

    dependencies = [
        ('ic_marathon_app', '0012_workout_partner_photo_evidence_and_more'),
    ]

    operations = [
        migrations.RunPython(create_cache_tables, drop_cache_tables),
    ]

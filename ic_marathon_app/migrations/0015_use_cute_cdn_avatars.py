from django.db import migrations, models


LEGACY_AVATAR_URL = (
    "https://ciscorunning2023.s3.us-east-1.amazonaws.com/static/img/user.png"
)
AVATAR_CDN_URL = "https://api.dicebear.com/9.x/bottts/svg?seed=ciscorunning-{}"


def assign_cute_avatars(apps, schema_editor):
    Profile = apps.get_model("ic_marathon_app", "Profile")
    profiles = Profile.objects.filter(avatar__in=["", LEGACY_AVATAR_URL])
    for profile in profiles.iterator():
        profile.avatar = AVATAR_CDN_URL.format(profile.user_id)
        profile.save(update_fields=["avatar"])


class Migration(migrations.Migration):

    dependencies = [
        ("ic_marathon_app", "0014_alter_workout_edition"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="avatar",
            field=models.CharField(blank=True, default="", max_length=400),
        ),
        migrations.RunPython(assign_cute_avatars, migrations.RunPython.noop),
    ]

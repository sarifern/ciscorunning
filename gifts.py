from ic_marathon_app.models import Profile
from django.core.exceptions import MultipleObjectsReturned
from ic_marathon_app.views import check_badges
import os

cecs_who_joined = os.environ.get("CECS_WHO_JOINED").split(',')

for cec in cecs_who_joined:
    try:
        # get profile
        profile = Profile.objects.get(cec=cec)
        profile.distance += 2
        profile.save()
        print(f"user {cec} has been granted the gift")
        check_badges(profile.user)
    except MultipleObjectsReturned:
        # check profile manually
        print(f"duplicated user {cec}, check manually")
    except Profile.DoesNotExist:
        pass

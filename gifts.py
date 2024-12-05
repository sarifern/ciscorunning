from ic_marathon_app.models import Profile, Workout
from django.core.exceptions import MultipleObjectsReturned
from ic_marathon_app.views import check_badges, WTAPI
import os
import datetime

cecs_who_joined = os.environ.get("CECS_WHO_JOINED").split(",")

for cec in cecs_who_joined:
    try:
        # get profile
        profile = Profile.objects.get(cec=cec)
        workout = Workout.objects.create(
            belongs_to=profile,
            distance=5,
            time="00:00",
            date_time=str(datetime.datetime.now()),
            photo_evidence=None,
            is_gift=True,
            is_audited=True,
        )

        print(f"user {cec} has been granted the gift")
        check_badges(profile.user)
    except MultipleObjectsReturned:
        # check profile manually
        print(f"duplicated user {cec}, check manually")
    except Profile.DoesNotExist:
        pass

markdown = f"Hey, thanks for attending the special event. \nFive extra kms have been granted to the following users: "
for cec in cecs_who_joined:
    markdown += f"<@personEmail:{cec}@cisco.com>,"
markdown = markdown[:-1]
WTAPI.messages.create(
    roomId=os.environ.get("WT_ROOMID"),
    markdown=markdown,
)

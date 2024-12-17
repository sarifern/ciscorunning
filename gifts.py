from ic_marathon_app.models import Profile, Workout
from django.core.exceptions import MultipleObjectsReturned
from ic_marathon_app.views import check_badges, WTAPI
import os
import datetime


def divide_into_batches(input_list, batch_size):
    """Divide a list into batches of a specified size."""
    for i in range(0, len(input_list), batch_size):
        yield input_list[i : i + batch_size]


cecs_who_joined = os.environ.get("CECS_WHO_JOINED").split(",")

for cec in cecs_who_joined:
    try:
        # get profile
        profile = Profile.objects.get(cec=cec.lower())
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
        WTAPI.messages.create(
            toPersonEmail=f"{cec}@cisco.com",
            markdown=f"Hey, you still haven't registered at www.ciscorunning.com. Please complete your profile. Once you have completed your registration, contact 'gpe-reyes-marathon@cisco.com' to get your extra KM.",
        )
        print(f"profile for user {cec} does not exist")
        pass

markdown = f"Hey, thanks for attending the special event. \nFive extra kms have been granted to the following users: "
WTAPI.messages.create(
    roomId=os.environ.get("WT_ROOMID"),
    markdown=markdown,
)

batches = list(divide_into_batches(cecs_who_joined, 15))
for batch in batches:
    markdown = ""
    for cec in batch:
        markdown += f"\n- <@personEmail:{cec}@cisco.com>"
    WTAPI.messages.create(
        roomId=os.environ.get("WT_ROOMID"),
        markdown=markdown,
    )

from django.core.exceptions import ValidationError
from datetime import datetime, timezone
import pytz as tz


def validate_date(value):
    current_date = datetime.now().replace(
        tzinfo=tz.timezone('America/Mexico_City'))
    if (value - current_date).seconds > 0 and (value - current_date).days >= 0:
        raise ValidationError("You cannot submit workouts in the future!")
    elif (value - current_date).days < -3:
        raise ValidationError("You cannot submit workouts older than two days!")
    else:
        return value


def validate_file_size(value):
    filesize = value.size

    if filesize > 5242880:
        raise ValidationError(
            "The maximum file size that can be uploaded is 5MB")
    else:
        return value


def validate_workout_time(value):
    total_min = value.hour * 60 + value.minute
    if total_min < 14:
        raise ValidationError("The minimum time value for a workout is 15 min")
    else:
        return value


def validate_distance(value):
    if float(value.real) > 250.00:
        raise ValidationError(
            "The maximum distance value for a workout is 250 km")
    else:
        return value

def validate_min_goal(value):
    if float(value.real) >= 21.00:
        return value
    else:
        raise ValidationError(
            "The minimum distance for a personal goal is 21K")

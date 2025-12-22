from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
import pytz as tz
import re


def validate_date(value):
    """Validate workout date with proper timezone handling.
    
    This function ensures workout dates are valid regardless of the user's timezone.
    All comparisons are done in UTC to avoid timezone conversion issues.
    """
    # Get current time in UTC (Django's timezone-aware now())
    current_date = timezone.now()
    
    # Ensure the submitted value is timezone-aware
    if timezone.is_naive(value):
        # If somehow a naive datetime comes through, make it aware in UTC
        value = timezone.make_aware(value, timezone.utc)
    
    # Calculate time difference
    time_diff = current_date - value
    
    # Check if workout is in the future (allowing small buffer for clock differences)
    if time_diff.total_seconds() < -300:  # 5 minute buffer for clock differences
        raise ValidationError("You cannot submit workouts in the future!")
    
    # Check if workout is too old (more than 2 days ago)
    if time_diff > timedelta(days=2):
        raise ValidationError("You cannot submit workouts older than two days!")
    
    return value

def validate_cec(value):
    if "@" in value:
        raise ValidationError("Please submit your CEC user without the @cisco.com'")
    elif re.match("\d+",value):
        raise ValidationError("Please submit your CEC user <CEC user>@cisco.com, not your employee number")
    else:
        return value

def validate_file_size(value):
    filesize = value.size

    if filesize > 10485760:
        raise ValidationError(
            "The maximum file size that can be uploaded is 10MB")
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

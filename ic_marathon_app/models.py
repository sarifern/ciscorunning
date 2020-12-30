from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.core.files.storage import default_storage
from django.contrib.staticfiles.storage import staticfiles_storage
from ic_marathon_site.storage_backends import PrivateMediaStorage
from django.forms import ModelForm
from django import forms
from django.dispatch import receiver
from django_select2.forms import Select2Widget
from bootstrap_datepicker_plus import TimePickerInput, DateTimePickerInput
import uuid
from .validators import validate_file_size, validate_workout_time, validate_distance, validate_date
import q

# Create your models here.
BEGINNERRUNNER = "beginnerrunner"
RUNNER = "runner"
BIKER = "biker"
DUATHLONER = "duathloner"
FREESTYLER = "freestyler"

CATEGORY_CHOICES = ((BEGINNERRUNNER,
                     'Beginner Runner'), (RUNNER, 'Runner'), (BIKER, 'Biker'),
                    (DUATHLONER, 'Duathloner'), (FREESTYLER, 'Freestyler'))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_goal = models.BooleanField(default=False)
    avatar = models.CharField(max_length=400, blank=False)
    cec = models.CharField(max_length=30, blank=True)
    distance = models.DecimalField(default=0.00,
                                   max_digits=10,
                                   decimal_places=2)

    category = models.CharField(max_length=20,
                                choices=CATEGORY_CHOICES,
                                blank=False,
                                default=BEGINNERRUNNER)

    def __str__(self):
        return self.cec


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['cec', 'category']


#Expand the model for the special WorkoutForm (free style)
class Workout(models.Model):
    belongs_to = models.ForeignKey(Profile,
                                   on_delete=models.CASCADE,
                                   default=None,
                                   unique=False)
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4,
                            editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    distance = models.DecimalField(verbose_name="KM",
                                   default=0.00,
                                   max_digits=5,
                                   decimal_places=2,
                                   validators=[validate_distance])
    photo_evidence = models.ImageField(verbose_name="Evidence",
                                       validators=[validate_file_size],
                                       storage=PrivateMediaStorage())
    date_time = models.DateTimeField(verbose_name="Date",
                                     validators=[validate_date])
    time = models.TimeField(verbose_name="Duration",
                            help_text='Workout in minutes',
                            validators=[validate_workout_time],
                            default='00:00')


class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['distance', 'date_time', 'time', 'photo_evidence']
        widgets = {
            'date_time': DateTimePickerInput(),
            'time': TimePickerInput(),
        }


class FSWorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['date_time', 'time', 'photo_evidence']
        widgets = {
            'date_time': DateTimePickerInput(),
            'time': TimePickerInput(),
        }


@receiver(post_delete, sender=Workout)
def delete_workout(sender, instance, **kwargs):
    # update personal distance
    profile = instance.belongs_to
    profile.distance -= instance.distance

    if profile.distance < 42.0:
        profile.user_goal = False
    profile.save()

    # delete image from S3
    try:
        default_storage.delete(instance.photo_evidence.name)
    except Exception:
        q("Can't delete the file {} in S3".format(
            instance.photo_evidence.name))


@receiver(post_save, sender=Workout)
def save_workout(sender, instance, **kwargs):
    # update personal distance
    profile = instance.belongs_to
    profile.distance += instance.distance
    if profile.distance >= 84.0 and profile.category == "beginnerrunner":
        profile.category = "runner"
    if profile.distance >= 42.0:
        profile.user_goal = True
    profile.save()

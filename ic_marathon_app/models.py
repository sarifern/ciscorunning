from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from decimal import *
from django.db.models.signals import post_save, post_delete
from django.core.files.storage import default_storage
from django.contrib.staticfiles.storage import staticfiles_storage
from ic_marathon_site.storage_backends import PrivateMediaStorage
from django.forms import ModelForm
from django import forms
from django.dispatch import receiver
from django_select2.forms import Select2Widget
from bootstrap_datepicker_plus.widgets import TimePickerInput, DateTimePickerInput
import uuid
from .validators import validate_file_size, validate_distance, validate_date, validate_min_goal, validate_cec
import q
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
# Create your models here.
BEGINNERRUNNER = "beginnerrunner"
RUNNER = "runner"
FREESTYLER = "freestyler"
BEGINNERFREESTYLER = "beginnerfreestyler"
CATEGORY_CHOICES = ((BEGINNERRUNNER, 'Beginner Runner'), 
                    (RUNNER, 'Runner'),
                    (FREESTYLER, 'Freestyler'),
                    (BEGINNERFREESTYLER, 'Beginner Freestyler'))


class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Sport"
        verbose_name_plural = "Sports"

    def __str__(self):
        return self.name

class IntensityLevel(models.Model):
    LEVEL_CHOICES = [
        ('Low', 'Low'),
        ('Moderate', 'Moderate'),
        ('High', 'High'),
    ]
    name = models.CharField(max_length=10, choices=LEVEL_CHOICES, unique=True)

    class Meta:
        verbose_name = "Intensity Level"
        verbose_name_plural = "Intensity Levels"

    def __str__(self):
        return self.name

class SportIntensityMapping(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    intensity = models.ForeignKey(IntensityLevel, on_delete=models.CASCADE)
    km_per_hour = models.FloatField(help_text="Kilometers equivalent for 1 hour at this intensity.")

    class Meta:
        unique_together = ('sport', 'intensity')
        verbose_name = "Sport Intensity Mapping"
        verbose_name_plural = "Sport Intensity Mappings"

    def __str__(self):
        return f"{self.sport} - {self.intensity} ({self.km_per_hour} km/hr)"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_goal = models.BooleanField(default=False)
    user_goal_km = models.DecimalField(default=42.00,
                                   max_digits=10,
                                   decimal_places=2,
                                   validators=[validate_min_goal])
    avatar = models.CharField(max_length=400, blank=True, default="https://ciscorunning2023.s3.us-east-1.amazonaws.com/static/img/user.png")
    cec = models.CharField(max_length=30, blank=True, validators=[validate_cec])
    distance = models.DecimalField(default=0.00,
                                   max_digits=10,
                                   decimal_places=2)

    category = models.CharField(max_length=20,
                                choices=CATEGORY_CHOICES,
                                blank=False,
                                default=BEGINNERRUNNER)
    category_changed = models.BooleanField(default=False, help_text="Has the user changed their category from the default?")
    first_workout_date = models.DateField(null=True, blank=True, help_text="Date of first workout - used for auto-promotion")
    workout_days_count = models.IntegerField(default=0, help_text="Number of unique days with workouts - used for auto-promotion")
    current_streak = models.IntegerField(default=0, help_text="Current consecutive days with workouts")
    longest_streak = models.IntegerField(default=0, help_text="Longest streak of consecutive workout days achieved")

    def __str__(self):
        return self.cec
    
    def get_parent_category(self):
        """
        Returns the parent category (runner or freestyler) for partner matching.
        """
        if self.category in [BEGINNERRUNNER, RUNNER]:
            return 'runner'
        else:  # beginnerfreestyler or freestyler
            return 'freestyler'
    
    def get_eligible_partners(self):
        """
        Returns a queryset of profiles that can be partners.
        Rules:
        - Must be in same parent category (runners with runners, freestylers with freestylers)
        - Must have completed profile (has CEC)
        - Excludes self
        """
        my_parent = self.get_parent_category()
        
        if my_parent == 'runner':
            eligible_categories = [BEGINNERRUNNER, RUNNER]
        else:
            eligible_categories = [BEGINNERFREESTYLER, FREESTYLER]
        
        return Profile.objects.filter(
            category__in=eligible_categories
        ).exclude(
            user=self.user
        ).exclude(
            cec=''
        ).order_by('cec')
    
    def calculate_streaks(self):
        """
        Calculate current and longest workout streaks for this profile.
        Returns a tuple: (current_streak, longest_streak)
        """
        from datetime import timedelta
        
        # Get all unique workout dates for this profile, ordered by date
        workout_dates = Workout.objects.filter(
            belongs_to=self
        ).dates('date_time', 'day').order_by('date_time__date')
        
        if not workout_dates:
            return 0, 0
        
        # Convert to list for easier processing
        dates_list = list(workout_dates)
        
        # Calculate longest streak
        longest = 1
        current = 1
        
        for i in range(1, len(dates_list)):
            # Check if dates are consecutive (difference of 1 day)
            if (dates_list[i] - dates_list[i-1]).days == 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        
        # Calculate current streak (from most recent date backwards)
        from django.utils import timezone
        today = timezone.now().date()
        
        current_streak = 0
        if dates_list:
            most_recent = dates_list[-1]
            
            # Only count as current streak if it includes today or yesterday
            days_since_last = (today - most_recent).days
            
            if days_since_last <= 1:
                # Start from most recent and go backwards
                current_streak = 1
                for i in range(len(dates_list) - 2, -1, -1):
                    if (dates_list[i+1] - dates_list[i]).days == 1:
                        current_streak += 1
                    else:
                        break
            # If more than 1 day since last workout, streak is broken
            else:
                current_streak = 0
        
        return current_streak, longest


class ProfileForm(ModelForm):
    # Only show Runner and Freestyler in the wizard (not beginner categories)
    # Users will be auto-assigned to beginner categories and promoted after 42km
    WIZARD_CATEGORY_CHOICES = (
        (RUNNER, 'Runner'),
        (FREESTYLER, 'Freestyler'),
    )
    
    category = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=WIZARD_CATEGORY_CHOICES
    )
    
    class Meta:
        model = Profile
        fields = ['cec', 'user_goal_km', 'category']
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Auto-assign to beginner category based on selection
        # This prevents gaming the system - everyone starts as beginner
        if instance.category == RUNNER:
            instance.category = BEGINNERRUNNER
        elif instance.category == FREESTYLER:
            instance.category = BEGINNERFREESTYLER
        
        if commit:
            instance.save()
        return instance


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
    edition = models.IntegerField(default=2025)
    distance = models.DecimalField(verbose_name="KM",
                                   default=0.00,
                                   max_digits=5,
                                   decimal_places=2,
                                   validators=[validate_distance])
    photo_evidence = models.ImageField(verbose_name="Evidence",
                                       validators=[validate_file_size],
                                       storage=PrivateMediaStorage())
    date_time = models.DateTimeField(verbose_name="Date")
    time = models.TimeField(verbose_name="Type",
                            help_text='Workout/Gift',
                          
                            default='00:00')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, default=1)  # Running
    intensity = models.ForeignKey(IntensityLevel, on_delete=models.CASCADE, default=1)  # Light

    is_audited = models.BooleanField(verbose_name="Audited?",
                                  help_text="Already audited?",
                                  default=False)
    is_gift = models.BooleanField(verbose_name="Gift?", help_text="Was this a gift (extra kms)?", default=False)
    
    # Partner Workout Fields
    is_partner_workout = models.BooleanField(
        verbose_name="Partner Workout?",
        help_text="Is this a partner workout (1.5x distance bonus)?",
        default=False
    )
    partner_profile = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='partner_workouts_received',
        help_text="The partner who trained with you"
    )
    partner_confirmed = models.BooleanField(
        verbose_name="Partner Confirmed?",
        help_text="Has the partner confirmed this workout?",
        default=False
    )
    partner_workout_group = models.UUIDField(
        null=True,
        blank=True,
        editable=False,
        help_text="Shared UUID linking both partner workouts together"
    )
    base_distance = models.DecimalField(
        verbose_name="Base Distance (before bonus)",
        default=0.00,
        max_digits=5,
        decimal_places=2,
        help_text="Original distance before 1.5x partner bonus"
    )
    
    def get_parent_category(self):
        """
        Returns the parent category (runner or freestyler) for this workout's profile.
        Used for partner workout validation.
        """
        if self.belongs_to.category in [BEGINNERRUNNER, RUNNER]:
            return 'runner'
        else:  # beginnerfreestyler or freestyler
            return 'freestyler'
    
    def can_partner_with(self, other_profile):
        """
        Validates if the current workout's profile can partner with another profile.
        Rules:
        - Both must be in same parent category (runners or freestylers)
        - Other profile must exist and have a CEC (completed registration)
        - Cannot partner with yourself
        """
        if not other_profile or not other_profile.cec:
            return False, "Partner must have a complete profile with CEC"
        
        if self.belongs_to.user == other_profile.user:
            return False, "Cannot partner with yourself"
        
        # Check parent category match
        my_parent = self.get_parent_category()
        
        if other_profile.category in [BEGINNERRUNNER, RUNNER]:
            partner_parent = 'runner'
        else:
            partner_parent = 'freestyler'
        
        if my_parent != partner_parent:
            return False, f"Partner must be in the same category family (both runners or both freestylers)"
        
        return True, "Valid partner"
    
    def is_expired(self):
        """
        Check if unconfirmed partner workout has expired (older than 2 days)
        """
        from django.utils import timezone
        from datetime import timedelta
        
        if not self.is_partner_workout or self.partner_confirmed:
            return False
        
        expiration_date = self.uploaded_at + timedelta(days=2)
        return timezone.now() > expiration_date
    
    def time_until_expiration(self):
        """
        Return timedelta until expiration (for display purposes)
        Returns None if already expired or not applicable
        """
        from django.utils import timezone
        from datetime import timedelta
        
        if not self.is_partner_workout or self.partner_confirmed:
            return None
        
        expiration_date = self.uploaded_at + timedelta(days=2)
        remaining = expiration_date - timezone.now()
        
        if remaining.total_seconds() <= 0:
            return None  # Already expired
        
        return remaining
    
    def get_expiration_status(self):
        """
        Returns human-readable expiration status
        """
        if not self.is_partner_workout or self.partner_confirmed:
            return None
        
        remaining = self.time_until_expiration()
        
        if remaining is None:
            return "Expired"
        
        hours = int(remaining.total_seconds() // 3600)
        
        if hours < 1:
            minutes = int(remaining.total_seconds() // 60)
            return f"{minutes} minutes remaining"
        elif hours < 24:
            return f"{hours} hours remaining"
        else:
            days = hours // 24
            return f"{days} day{'s' if days != 1 else ''} remaining"
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_goal = models.BooleanField(default=False)
    user_goal_km = models.DecimalField(default=42.00,
                                   max_digits=10,
                                   decimal_places=2,
                                   validators=[validate_min_goal])
    avatar = models.CharField(max_length=400, blank=True, default="https://ciscorunning2023.s3.us-east-1.amazonaws.com/static/img/user.png")
    cec = models.CharField(max_length=30, blank=True, validators=[validate_cec])
    distance = models.DecimalField(default=0.00,
                                   max_digits=10,
                                   decimal_places=2)

    category = models.CharField(max_length=20,
                                choices=CATEGORY_CHOICES,
                                blank=False,
                                default=BEGINNERRUNNER)
    category_changed = models.BooleanField(default=False, help_text="Has the user changed their category from the default?")
    first_workout_date = models.DateField(null=True, blank=True, help_text="Date of first workout - used for auto-promotion")
    workout_days_count = models.IntegerField(default=0, help_text="Number of unique days with workouts - used for auto-promotion")
    current_streak = models.IntegerField(default=0, help_text="Current consecutive days with workouts")
    longest_streak = models.IntegerField(default=0, help_text="Longest streak of consecutive workout days achieved")

    def __str__(self):
        return self.cec
    
    def get_parent_category(self):
        """
        Returns the parent category (runner or freestyler) for partner matching.
        """
        if self.category in [BEGINNERRUNNER, RUNNER]:
            return 'runner'
        else:  # beginnerfreestyler or freestyler
            return 'freestyler'
    
    def get_eligible_partners(self):
        """
        Returns a queryset of profiles that can be partners.
        Rules:
        - Must be in same parent category (runners with runners, freestylers with freestylers)
        - Must have completed profile (has CEC)
        - Excludes self
        """
        my_parent = self.get_parent_category()
        
        if my_parent == 'runner':
            eligible_categories = [BEGINNERRUNNER, RUNNER]
        else:
            eligible_categories = [BEGINNERFREESTYLER, FREESTYLER]
        
        return Profile.objects.filter(
            category__in=eligible_categories
        ).exclude(
            user=self.user
        ).exclude(
            cec=''
        ).order_by('cec')
    
    def calculate_streaks(self):
        """
        Calculate current and longest workout streaks for this profile.
        Returns a tuple: (current_streak, longest_streak)
        """
        from datetime import timedelta
        
        # Get all unique workout dates for this profile, ordered by date
        workout_dates = Workout.objects.filter(
            belongs_to=self
        ).dates('date_time', 'day').order_by('date_time__date')
        
        if not workout_dates:
            return 0, 0
        
        # Convert to list for easier processing
        dates_list = list(workout_dates)
        
        # Calculate longest streak
        longest = 1
        current = 1
        
        for i in range(1, len(dates_list)):
            # Check if dates are consecutive (difference of 1 day)
            if (dates_list[i] - dates_list[i-1]).days == 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        
        # Calculate current streak (from most recent date backwards)
        from django.utils import timezone
        today = timezone.now().date()
        
        current_streak = 0
        if dates_list:
            most_recent = dates_list[-1]
            
            # Only count as current streak if it includes today or yesterday
            days_since_last = (today - most_recent).days
            
            if days_since_last <= 1:
                # Start from most recent and go backwards
                current_streak = 1
                for i in range(len(dates_list) - 2, -1, -1):
                    if (dates_list[i+1] - dates_list[i]).days == 1:
                        current_streak += 1
                    else:
                        break
            # If more than 1 day since last workout, streak is broken
            else:
                current_streak = 0
        
        return current_streak, longest


class ProfileForm(ModelForm):
    # Only show Runner and Freestyler in the wizard (not beginner categories)
    # Users will be auto-assigned to beginner categories and promoted after 42km
    WIZARD_CATEGORY_CHOICES = (
        (RUNNER, 'Runner'),
        (FREESTYLER, 'Freestyler'),
    )
    
    category = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=WIZARD_CATEGORY_CHOICES
    )
    
    class Meta:
        model = Profile
        fields = ['cec', 'user_goal_km', 'category']
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Auto-assign to beginner category based on selection
        # This prevents gaming the system - everyone starts as beginner
        if instance.category == RUNNER:
            instance.category = BEGINNERRUNNER
        elif instance.category == FREESTYLER:
            instance.category = BEGINNERFREESTYLER
        
        if commit:
            instance.save()
        return instance


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
    edition = models.IntegerField(default=2025)
    distance = models.DecimalField(verbose_name="KM",
                                   default=0.00,
                                   max_digits=5,
                                   decimal_places=2,
                                   validators=[validate_distance])
    photo_evidence = models.ImageField(verbose_name="Evidence",
                                       validators=[validate_file_size],
                                       storage=PrivateMediaStorage())
    date_time = models.DateTimeField(verbose_name="Date")
    time = models.TimeField(verbose_name="Type",
                            help_text='Workout/Gift',
                          
                            default='00:00')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, default=1)  # Running
    intensity = models.ForeignKey(IntensityLevel, on_delete=models.CASCADE, default=1)  # Light

    is_audited = models.BooleanField(verbose_name="Audited?",
                                  help_text="Already audited?",
                                  default=False)
    is_gift = models.BooleanField(verbose_name="Gift?", help_text="Was this a gift (extra kms)?", default=False)
    
    # Partner Workout Fields
    is_partner_workout = models.BooleanField(
        verbose_name="Partner Workout?",
        help_text="Is this a partner workout (1.5x distance bonus)?",
        default=False
    )
    partner_profile = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='partner_workouts_received',
        help_text="The partner who trained with you"
    )
    partner_confirmed = models.BooleanField(
        verbose_name="Partner Confirmed?",
        help_text="Has the partner confirmed this workout?",
        default=False
    )
    partner_workout_group = models.UUIDField(
        null=True,
        blank=True,
        editable=False,
        help_text="Shared UUID linking both partner workouts together"
    )
    base_distance = models.DecimalField(
        verbose_name="Base Distance (before bonus)",
        default=0.00,
        max_digits=5,
        decimal_places=2,
        help_text="Original distance before 1.5x partner bonus"
    )
    
    def get_parent_category(self):
        """
        Returns the parent category (runner or freestyler) for this workout's profile.
        Used for partner workout validation.
        """
        if self.belongs_to.category in [BEGINNERRUNNER, RUNNER]:
            return 'runner'
        else:  # beginnerfreestyler or freestyler
            return 'freestyler'
    
    def can_partner_with(self, other_profile):
        """
        Validates if the current workout's profile can partner with another profile.
        Rules:
        - Both must be in same parent category (runners or freestylers)
        - Other profile must exist and have a CEC (completed registration)
        - Cannot partner with yourself
        """
        if not other_profile or not other_profile.cec:
            return False, "Partner must have a complete profile with CEC"
        
        if self.belongs_to.user == other_profile.user:
            return False, "Cannot partner with yourself"
        
        # Check parent category match
        my_parent = self.get_parent_category()
        
        if other_profile.category in [BEGINNERRUNNER, RUNNER]:
            partner_parent = 'runner'
        else:
            partner_parent = 'freestyler'
        
        if my_parent != partner_parent:
            return False, f"Partner must be in the same category family (both runners or both freestylers)"
        
        return True, "Valid partner"
    
    def is_expired(self):
        """
        Check if unconfirmed partner workout has expired (older than 2 days)
        """
        from django.utils import timezone
        from datetime import timedelta
        
        if not self.is_partner_workout or self.partner_confirmed:
            return False
        
        expiration_date = self.uploaded_at + timedelta(days=2)
        return timezone.now() > expiration_date
    
    def time_until_expiration(self):
        """
        Return timedelta until expiration (for display purposes)
        Returns None if already expired or not applicable
        """
        from django.utils import timezone
        from datetime import timedelta
        
        if not self.is_partner_workout or self.partner_confirmed:
            return None
        
        expiration_date = self.uploaded_at + timedelta(days=2)
        remaining = expiration_date - timezone.now()
        
        if remaining.total_seconds() <= 0:
            return None  # Already expired
        
        return remaining
    
    def get_expiration_status(self):
        """
        Returns human-readable expiration status
        """
        if not self.is_partner_workout or self.partner_confirmed:
            return None
        
        remaining = self.time_until_expiration()
        
        if remaining is None:
            return "Expired"
        
        hours = int(remaining.total_seconds() // 3600)
        
        if hours < 1:
            minutes = int(remaining.total_seconds() // 60)
            return f"{minutes} minutes remaining"
        elif hours < 24:
            return f"{hours} hours remaining"
        else:
            days = hours // 24
            return f"{days} day{'s' if days != 1 else ''} remaining"
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_goal = models.BooleanField(default=False)
    user_goal_km = models.DecimalField(default=42.00,
                                   max_digits=10,
                                   decimal_places=2,
                                   validators=[validate_min_goal])
    avatar = models.CharField(max_length=400, blank=True, default="https://ciscorunning2023.s3.us-east-1.amazonaws.com/static/img/user.png")
    cec = models.CharField(max_length=30, blank=True, validators=[validate_cec])
    distance = models.DecimalField(default=0.00,
                                   max_digits=10,
                                   decimal_places=2)

    category = models.CharField(max_length=20,
                                choices=CATEGORY_CHOICES,
                                blank=False,
                                default=BEGINNERRUNNER)
    category_changed = models.BooleanField(default=False, help_text="Has the user changed their category from the default?")
    first_workout_date = models.DateField(null=True, blank=True, help_text="Date of first workout - used for auto-promotion")
    workout_days_count = models.IntegerField(default=0, help_text="Number of unique days with workouts - used for auto-promotion")
    current_streak = models.IntegerField(default=0, help_text="Current consecutive days with workouts")
    longest_streak = models.IntegerField(default=0, help_text="Longest streak of consecutive workout days achieved")

    def __str__(self):
        return self.cec
    
    def get_parent_category(self):
        """
        Returns the parent category (runner or freestyler) for partner matching.
        """
        if self.category in [BEGINNERRUNNER, RUNNER]:
            return 'runner'
        else:  # beginnerfreestyler or freestyler
            return 'freestyler'
    
    def get_eligible_partners(self):
        """
        Returns a queryset of profiles that can be partners.
        Rules:
        - Must be in same parent category (runners with runners, freestylers with freestylers)
        - Must have completed profile (has CEC)
        - Excludes self
        """
        my_parent = self.get_parent_category()
        
        if my_parent == 'runner':
            eligible_categories = [BEGINNERRUNNER, RUNNER]
        else:
            eligible_categories = [BEGINNERFREESTYLER, FREESTYLER]
        
        return Profile.objects.filter(
            category__in=eligible_categories
        ).exclude(
            user=self.user
        ).exclude(
            cec=''
        ).order_by('cec')
    
    def calculate_streaks(self):
        """
        Calculate current and longest workout streaks for this profile.
        Returns a tuple: (current_streak, longest_streak)
        """
        from datetime import timedelta
        
        # Get all unique workout dates for this profile, ordered by date
        workout_dates = Workout.objects.filter(
            belongs_to=self
        ).dates('date_time', 'day').order_by('date_time__date')
        
        if not workout_dates:
            return 0, 0
        
        # Convert to list for easier processing
        dates_list = list(workout_dates)
        
        # Calculate longest streak
        longest = 1
        current = 1
        
        for i in range(1, len(dates_list)):
            # Check if dates are consecutive (difference of 1 day)
            if (dates_list[i] - dates_list[i-1]).days == 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        
        # Calculate current streak (from most recent date backwards)
        from django.utils import timezone
        today = timezone.now().date()
        
        current_streak = 0
        if dates_list:
            most_recent = dates_list[-1]
            
            # Only count as current streak if it includes today or yesterday
            days_since_last = (today - most_recent).days
            
            if days_since_last <= 1:
                # Start from most recent and go backwards
                current_streak = 1
                for i in range(len(dates_list) - 2, -1, -1):
                    if (dates_list[i+1] - dates_list[i]).days == 1:
                        current_streak += 1
                    else:
                        break
            # If more than 1 day since last workout, streak is broken
            else:
                current_streak = 0
        
        return current_streak, longest


class ProfileForm(ModelForm):
    # Only show Runner and Freestyler in the wizard (not beginner categories)
    # Users will be auto-assigned to beginner categories and promoted after 42km
    WIZARD_CATEGORY_CHOICES = (
        (RUNNER, 'Runner'),
        (FREESTYLER, 'Freestyler'),
    )
    
    category = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=WIZARD_CATEGORY_CHOICES
    )
    
    class Meta:
        model = Profile
        fields = ['cec', 'user_goal_km', 'category']
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Auto-assign to beginner category based on selection
        # This prevents gaming the system - everyone starts as beginner
        if instance.category == RUNNER:
            instance.category = BEGINNERRUNNER
        elif instance.category == FREESTYLER:
            instance.category = BEGINNERFREESTYLER
        
        if commit:
            instance.save()
        return instance


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
    edition = models.IntegerField(default=2025)
    distance = models.DecimalField(verbose_name="KM",
                                   default=0.00,
                                   max_digits=5,
                                   decimal_places=2,
                                   validators=[validate_distance])
    photo_evidence = models.ImageField(verbose_name="Evidence",
                                       validators=[validate_file_size],
                                       storage=PrivateMediaStorage())
    date_time = models.DateTimeField(verbose_name="Date")
    time = models.TimeField(verbose_name="Type",
                            help_text='Workout/Gift',
                          
                            default='00:00')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, default=1)  # Running
    intensity = models.ForeignKey(IntensityLevel, on_delete=models.CASCADE, default=1)  # Light

    is_audited = models.BooleanField(verbose_name="Audited?",
                                  help_text="Already audited?",
                                  default=False)
    is_gift = models.BooleanField(verbose_name="Gift?", help_text="Was this a gift (extra kms)?", default=False)
    
    # Partner Workout Fields
    is_partner_workout = models.BooleanField(
        verbose_name="Partner Workout?",
        help_text="Is this a partner workout (1.5x distance bonus)?",
        default=False
    )
    partner_profile = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='partner_workouts_received',
        help_text="The partner who trained with you"
    )
    partner_confirmed = models.BooleanField(
        verbose_name="Partner Confirmed?",
        help_text="Has the partner confirmed this workout?",
        default=False
    )
    partner_workout_group = models.UUIDField(
        null=True,
        blank=True,
        editable=False,
        help_text="Shared UUID linking both partner workouts together"
    )
    base_distance = models.DecimalField(
        verbose_name="Base Distance (before bonus)",
        default=0.00,
        max_digits=5,
        decimal_places=2,
        help_text="Original distance before 1.5x partner bonus"
    )
    
    def get_parent_category(self):
        """
        Returns the parent category (runner or freestyler) for this workout's profile.
        Used for partner workout validation.
        """
        if self.belongs_to.category in [BEGINNERRUNNER, RUNNER]:
            return 'runner'
        else:  # beginnerfreestyler or freestyler
            return 'freestyler'
    
    def can_partner_with(self, other_profile):
        """
        Validates if the current workout's profile can partner with another profile.
        Rules:
        - Both must be in same parent category (runners or freestylers)
        - Other profile must exist and have a CEC (completed registration)
        - Cannot partner with yourself
        """
        if not other_profile or not other_profile.cec:
            return False, "Partner must have a complete profile with CEC"
        
        if self.belongs_to.user == other_profile.user:
            return False, "Cannot partner with yourself"
        
        # Check parent category match
        my_parent = self.get_parent_category()
        
        if other_profile.category in [BEGINNERRUNNER, RUNNER]:
            partner_parent = 'runner'
        else:
            partner_parent = 'freestyler'
        
        if my_parent != partner_parent:
            return False, f"Partner must be in the same category family (both runners or both freestylers)"
        
        return True, "Valid partner"
    
    def is_expired(self):
        """
        Check if unconfirmed partner workout has expired (older than 2 days)
        """
        from django.utils import timezone
        from datetime import timedelta
        
        if not self.is_partner_workout or self.partner_confirmed:
            return False
        
        expiration_date = self.uploaded_at + timedelta(days=2)
        return timezone.now() > expiration_date
    
    def time_until_expiration(self):
        """
        Return timedelta until expiration (for display purposes)
        Returns None if already expired or not applicable
        """
        from django.utils import timezone
        from datetime import timedelta
        
        if not self.is_partner_workout or self.partner_confirmed:
            return None
        
        expiration_date = self.uploaded_at + timedelta(days=2)
        remaining = expiration_date - timezone.now()
        
        if remaining.total_seconds() <= 0:
            return None  # Already expired
        
        return remaining
    
    def get_expiration_status(self):
        """
        Returns human-readable expiration status
        """
        if not self.is_partner_workout or self.partner_confirmed:
            return None
        
        remaining = self.time_until_expiration()
        
        if remaining is None:
            return "Expired"
        
        hours = int(remaining.total_seconds() // 3600)
        
        if hours < 1:
            minutes = int(remaining.total_seconds() // 60)
            return f"{minutes} minutes remaining"
        elif hours < 24:
            return f"{hours} hours remaining"
        else:
            days = hours // 24
            return f"{days} day{'s' if days != 1 else ''} remaining"
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_goal = models.BooleanField(default=False)
    user_goal_km = models.DecimalField(default=42.00,
                                   max_digits=10,
                                   decimal_places=2,
                                   validators=[validate_min_goal])
    avatar = models.CharField(max_length=400, blank=True, default="https://ciscorunning2023.s3.us-east-1.amazonaws.com/static/img/user.png")
    cec = models.CharField(max_length=30, blank=True, validators=[validate_cec])
    distance = models.DecimalField(default=0.00,
                                   max_digits=10,
                                   decimal_places=2)

    category = models.CharField(max_length=20,
                                choices=CATEGORY_CHOICES,
                                blank=False,
                                default=BEGINNERRUNNER)
    category_changed = models.BooleanField(default=False, help_text="Has the user changed their category from the default?")
    first_workout_date = models.DateField(null=True, blank=True, help_text="Date of first workout - used for auto-promotion")
    workout_days_count = models.IntegerField(default=0, help_text="Number of unique days with workouts - used for auto-promotion")
    current_streak = models.IntegerField(default=0, help_text="Current consecutive days with workouts")
    longest_streak = models.IntegerField(default=0, help_text="Longest streak of consecutive workout days achieved")

    def __str__(self):
        return self.cec
    
    def get_parent_category(self):
        """
        Returns the parent category (runner or freestyler) for partner matching.
        """
        if self.category in [BEGINNERRUNNER, RUNNER]:
            return 'runner'
        else:  # beginnerfreestyler or freestyler
            return 'freestyler'
    
    def get_eligible_partners(self):
        """
        Returns a queryset of profiles that can be partners.
        Rules:
        - Must be in same parent category (runners with runners, freestylers with freestylers)
        - Must have completed profile (has CEC)
        - Excludes self
        """
        my_parent = self.get_parent_category()
        
        if my_parent == 'runner':
            eligible_categories = [BEGINNERRUNNER, RUNNER]
        else:
            eligible_categories = [BEGINNERFREESTYLER, FREESTYLER]
        
        return Profile.objects.filter(
            category__in=eligible_categories
        ).exclude(
            user=self.user
        ).exclude(
            cec=''
        ).order_by('cec')
    
    def calculate_streaks(self):
        """
        Calculate current and longest workout streaks for this profile.
        Returns a tuple: (current_streak, longest_streak)
        """
        from datetime import timedelta
        
        # Get all unique workout dates for this profile, ordered by date
        workout_dates = Workout.objects.filter(
            belongs_to=self
        ).dates('date_time', 'day').order_by('date_time__date')
        
        if not workout_dates:
            return 0, 0
        
        # Convert to list for easier processing
        dates_list = list(workout_dates)
        
        # Calculate longest streak
        longest = 1
        current = 1
        
        for i in range(1, len(dates_list)):
            # Check if dates are consecutive (difference of 1 day)
            if (dates_list[i] - dates_list[i-1]).days == 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        
        # Calculate current streak (from most recent date backwards)
        from django.utils import timezone
        today = timezone.now().date()
        
        current_streak = 0
        if dates_list:
            most_recent = dates_list[-1]
            
            # Only count as current streak if it includes today or yesterday
            days_since_last = (today - most_recent).days
            
            if days_since_last <= 1:
                # Start from most recent and go backwards
                current_streak = 1
                for i in range(len(dates_list) - 2, -1, -1):
                    if (dates_list[i+1] - dates_list[i]).days == 1:
                        current_streak += 1
                    else:
                        break
            # If more than 1 day since last workout, streak is broken
            else:
                current_streak = 0
        
        return current_streak, longest


class ProfileForm(ModelForm):
    # Only show Runner and Freestyler in the wizard (not beginner categories)
    # Users will be auto-assigned to beginner categories and promoted after 42km
    WIZARD_CATEGORY_CHOICES = (
        (RUNNER, 'Runner'),
        (FREESTYLER, 'Freestyler'),
    )
    
    category = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=WIZARD_CATEGORY_CHOICES
    )
    
    class Meta:
        model = Profile
        fields = ['cec', 'user_goal_km', 'category']
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Auto-assign to beginner category based on selection
        # This prevents gaming the system - everyone starts as beginner
        if instance.category == RUNNER:
            instance.category = BEGINNERRUNNER
        elif instance.category == FREESTYLER:
            instance.category = BEGINNERFREESTYLER
        
        if commit:
            instance.save()
        return instance


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
    edition = models.IntegerField(default=2025)
    distance = models.DecimalField(verbose_name="KM",
                                   default=0.00,
                                   max_digits=5,
                                   decimal_places=2,
                                   validators=[validate_distance])
    photo_evidence = models.ImageField(verbose_name="Evidence",
                                       validators=[validate_file_size],
                                       storage=PrivateMediaStorage())
    date_time = models.DateTimeField(verbose_name="Date")
    time = models.TimeField(verbose_name="Type",
                            help_text='Workout/Gift',
                          
                            default='00:00')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, default=1)  # Running
    intensity = models.ForeignKey(IntensityLevel, on_delete=models.CASCADE, default=1)  # Light

    is_audited = models.BooleanField(verbose_name="Audited?",
                                  help_text="Already audited?",
                                  default=False)
    is_gift = models.BooleanField(verbose_name="Gift?", help_text="Was this a gift (extra kms)?", default=False)
    
    # Partner Workout Fields
    is_partner_workout = models.BooleanField(
        verbose_name="Partner Workout?",
        help_text="Is this a partner workout (1.5x distance bonus)?",
        default=False
    )
    partner_profile = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='partner_workouts_received',
        help_text="The partner who trained with you"
    )
    partner_confirmed = models.BooleanField(
        verbose_name="Partner Confirmed?",
        help_text="Has the partner confirmed this workout?",
        default=False
    )
    partner_workout_group = models.UUIDField(
        null=True,
        blank=True,
        editable=False,
        help_text="Shared UUID linking both partner workouts together"
    )
    base_distance = models.DecimalField(
        verbose_name="Base Distance (before bonus)",
        default=0.00,
        max_digits=5,
        decimal_places=2,
        help_text="Original distance before 1.5x partner bonus"
    )
    
    def get_parent_category(self):
        """
        Returns the parent category (runner or freestyler) for this workout's profile.
        Used for partner workout validation.
        """
        if self.belongs_to.category in [BEGINNERRUNNER, RUNNER]:
            return 'runner'
        else:  # beginnerfreestyler or freestyler
            return 'freestyler'
    
    def can_partner_with(self, other_profile):
        """
        Validates if the current workout's profile can partner with another profile.
        Rules:
        - Both must be in same parent category (runners or freestylers)
        - Other profile must exist and have a CEC (completed registration)
        - Cannot partner with yourself
        """
        if not other_profile or not other_profile.cec:
            return False, "Partner must have a complete profile with CEC"
        
        if self.belongs_to.user == other_profile.user:
            return False, "Cannot partner with yourself"
        
        # Check parent category match
        my_parent = self.get_parent_category()
        
        if other_profile.category in [BEGINNERRUNNER, RUNNER]:
            partner_parent = 'runner'
        else:
            partner_parent = 'freestyler'
        
        if my_parent != partner_parent:
            return False, f"Partner must be in the same category family (both runners or both freestylers)"
        
        return True, "Valid partner"
    
    def is_expired(self):
        """
        Check if unconfirmed partner workout has expired (older than 2 days)
        """
        from django.utils import timezone
        from datetime import timedelta
        
        if not self.is_partner_workout or self.partner_confirmed:
            return False
        
        expiration_date = self.uploaded_at + timedelta(days=2)
        return timezone.now() > expiration_date
    
    def time_until_expiration(self):
        """
        Return timedelta until expiration (for display purposes)
        Returns None if already expired or not applicable
        """
        from django.utils import timezone
        from datetime import timedelta
        
        if not self.is_partner_workout or self.partner_confirmed:
            return None
        
        expiration_date = self.uploaded_at + timedelta(days=2)
        remaining = expiration_date - timezone.now()
        
        if remaining.total_seconds() <= 0:
            return None  # Already expired
        
        return remaining
    
    def get_expiration_status(self):
        """
        Returns human-readable expiration status
        """
        if not self.is_partner_workout or self.partner_confirmed:
            return None
        
        remaining = self.time_until_expiration()
        
        if remaining is None:
            return "Expired"
        
        hours = int(remaining.total_seconds() // 3600)
        
        if hours < 1:
            minutes = int(remaining.total_seconds() // 60)
            return f"{minutes} minutes remaining"
        elif hours < 24:
            return f"{hours} hours remaining"
        else:
            days = hours // 24
            return f"{days} day{'s' if days != 1 else ''} remaining"
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_goal = models.BooleanField(default=False)
    user_goal_km = models.DecimalField(default=42.00,
                                   max_digits=10,
                                   decimal_places=2,
                                   validators=[validate_min_goal])
    avatar = models.CharField(max_length=400, blank=True, default="https://ciscorunning2023.s3.us-east-1.amazonaws.com/static/img/user.png")
    cec = models.CharField(max_length=30, blank=True, validators=[validate_cec])
    distance = models.DecimalField(default=0.00,
                                   max_digits=10,
                                   decimal_places=2)

    category = models.CharField(max_length=20,
                                choices=CATEGORY_CHOICES,
                                blank=False,
                                default=BEGINNERRUNNER)
    category_changed = models.BooleanField(default=False, help_text="Has the user changed their category from the default?")
    first_workout_date = models.DateField(null=True, blank=True, help_text="Date of first workout - used for auto-promotion")
    workout_days_count = models.IntegerField(default=0, help_text="Number of unique days with workouts - used for auto-promotion")
    current_streak = models.IntegerField(default=0, help_text="Current consecutive days with workouts")
    longest_streak = models.IntegerField(default=0, help_text="Longest streak of consecutive workout days achieved")

    def __str__(self):
        return self.cec
    
    def get_parent_category(self):
        """
        Returns the parent category (runner or freestyler) for partner matching.
        """
        if self.category in [BEGINNERRUNNER, RUNNER]:
            return 'runner'
        else:  # beginnerfreestyler or freestyler
            return 'freestyler'
    
    def get_eligible_partners(self):
        """
        Returns a queryset of profiles that can be partners.
        Rules:
        - Must be in same parent category (runners with runners, freestylers with freestylers)
        - Must have completed profile (has CEC)
        - Excludes self
        """
        my_parent = self.get_parent_category()
        
        if my_parent == 'runner':
            eligible_categories = [BEGINNERRUNNER, RUNNER]
        else:
            eligible_categories = [BEGINNERFREESTYLER, FREESTYLER]
        
        return Profile.objects.filter(
            category__in=eligible_categories
        ).exclude(
            user=self.user
        ).exclude(
            cec=''
        ).order_by('cec')
    
    def calculate_streaks(self):
        """
        Calculate current and longest workout streaks for this profile.
        Returns a tuple: (current_streak, longest_streak)
        """
        from datetime import timedelta
        
        # Get all unique workout dates for this profile, ordered by date
        workout_dates = Workout.objects.filter(
            belongs_to=self
        ).dates('date_time', 'day').order_by('date_time__date')
        
        if not workout_dates:
            return 0, 0
        
        # Convert to list for easier processing
        dates_list = list(workout_dates)
        
        # Calculate longest streak
        longest = 1
        current = 1
        
        for i in range(1, len(dates_list)):
            # Check if dates are consecutive (difference of 1 day)
            if (dates_list[i] - dates_list[i-1]).days == 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        
        # Calculate current streak (from most recent date backwards)
        from django.utils import timezone
        today = timezone.now().date()
        
        current_streak = 0
        if dates_list:
            most_recent = dates_list[-1]
            
            # Only count as current streak if it includes today or yesterday
            days_since_last = (today - most_recent).days
            
            if days_since_last <= 1:
                # Start from most recent and go backwards
                current_streak = 1
                for i in range(len(dates_list) - 2, -1, -1):
                    if (dates_list[i+1] - dates_list[i]).days == 1:
                        current_streak += 1
                    else:
                        break
            # If more than 1 day since last workout, streak is broken
            else:
                current_streak = 0
        
        return current_streak, longest


class ProfileForm(ModelForm):
    # Only show Runner and Freestyler in the wizard (not beginner categories)
    # Users will be auto-assigned to beginner categories and promoted after 42km
    WIZARD_CATEGORY_CHOICES = (
        (RUNNER, 'Runner'),
        (FREESTYLER, 'Freestyler'),
    )
    
    category = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=WIZARD_CATEGORY_CHOICES
    )
    
    class Meta:
        model = Profile
        fields = ['cec', 'user_goal_km', 'category']
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Auto-assign to beginner category based on selection
        # This prevents gaming the system - everyone starts as beginner
        if instance.category == RUNNER:
            instance.category = BEGINNERRUNNER
        elif instance.category == FREESTYLER:
            instance.category = BEGINNERFREESTYLER
        
        if commit:
            instance.save()
        return instance


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
    edition = models.IntegerField(default=2025)
    distance = models.DecimalField(verbose_name="KM",
                                   default=0.00,
                                   max_digits=5,
                                   decimal_places=2,
                                   validators=[validate_distance])
    photo_evidence = models.ImageField(verbose_name="Evidence",
                                       validators=[validate_file_size],
                                       storage=PrivateMediaStorage())
    date_time = models.DateTimeField(verbose_name="Date")
    time = models.TimeField(verbose_name="Type",
                            help_text='Workout/Gift',
                          
                            default='00:00')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, default=1)  # Running
    intensity = models.ForeignKey(IntensityLevel, on_delete=models.CASCADE, default=1)  # Light

    is_audited = models.BooleanField(verbose_name="Audited?",
                                  help_text="Already audited?",
                                  default=False)
    is_gift = models.BooleanField(verbose_name="Gift?", help_text="Was this a gift (extra kms)?", default=False)
    
    # Partner Workout Fields
    is_partner_workout = models.BooleanField(
        verbose_name="Partner Workout?",
        help_text="Is this a partner workout (1.5x distance bonus)?",
        default=False
    )
    partner_profile = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='partner_workouts_received',
        help_text="The partner who trained with you"
    )
    partner_confirmed = models.BooleanField(
        verbose_name="Partner Confirmed?",
        help_text="Has the partner confirmed this workout?",
        default=False
    )
    partner_workout_group = models.UUIDField(
        null=True,
        blank=True,
        editable=False,
        help_text="Shared UUID linking both partner workouts together"
    )
    base_distance = models.DecimalField(
        verbose_name="Base Distance (before bonus)",
        default=0.00,
        max_digits=5,
        decimal_places=2,
        help_text="Original distance before 1.5x partner bonus"
    )
    
    def get_parent_category(self):
        """
        Returns the parent category (runner or freestyler) for this workout's profile.
        Used for partner workout validation.
        """
        if self.belongs_to.category in [BEGINNERRUNNER, RUNNER]:
            return 'runner'
        else:  # beginnerfreestyler or freestyler
            return 'freestyler'
    
    def can_partner_with(self, other_profile):
        """
        Validates if the current workout's profile can partner with another profile.
        Rules:
        - Both must be in same parent category (runners or freestylers)
        - Other profile must exist and have a CEC (completed registration)
        - Cannot partner with yourself
        """
        if not other_profile or not other_profile.cec:
            return False, "Partner must have a complete profile with CEC"
        
        if self.belongs_to.user == other_profile.user:
            return False, "Cannot partner with yourself"
        
        # Check parent category match
        my_parent = self.get_parent_category()
        
        if other_profile.category in [BEGINNERRUNNER, RUNNER]:
            partner_parent = 'runner'
        else:
            partner_parent = 'freestyler'
        
        if my_parent != partner_parent:
            return False, f"Partner must be in the same category family (both runners or both freestylers)"
        
        return True, "Valid partner"
    
    def is_expired(self):
        """
        Check if unconfirmed partner workout has expired (older than 2 days)
        """
        from django.utils import timezone
        from datetime import timedelta
        
        if not self.is_partner_workout or self.partner_confirmed:
            return False
        
        expiration_date = self.uploaded_at + timedelta(days=2)
        return timezone.now() > expiration_date
    
    def time_until_expiration(self):
        """
        Return timedelta until expiration (for display purposes)
        Returns None if already expired or not applicable
        """
        from django.utils import timezone
        from datetime import timedelta
        
        if not self.is_partner_workout or self.partner_confirmed:
            return None
        
        expiration_date = self.uploaded_at + timedelta(days=2)
        remaining = expiration_date - timezone.now()
        
        if remaining.total_seconds() <= 0:
            return None  # Already expired
        
        return remaining
    
    def get_expiration_status(self):
        """
        Returns human-readable expiration status
        """
        if not self.is_partner_workout or self.partner_confirmed:
            return None
        
        remaining = self.time_until_expiration()
        
        if remaining is None:
            return "Expired"
        
        hours = int(remaining.total_seconds() // 3600)
        
        if hours < 1:
            minutes = int(remaining.total_seconds() // 60)
            return f"{minutes} minutes remaining"
        elif hours < 24:
            return f"{hours} hours remaining"
        else:
            days = hours // 24
            return f"{days} day{'s' if days != 1 else ''} remaining"
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_goal = models.BooleanField(default=False)
    user_goal_km = models.DecimalField(default=42.00,
                                   max_digits=10,
                                   decimal_places=2,
                                   validators=[validate_min_goal])
    avatar = models.CharField(max_length=400, blank=True, default="https://ciscorunning2023.s3.us-east-1.amazonaws.com/static/img/user.png")
    cec = models.CharField(max_length=30, blank=True, validators=[validate_cec])
    distance = models.DecimalField(default=0.00,
                                   max_digits=10,
                                   decimal_places=2)

    category = models.CharField(max_length=20,
                                choices=CATEGORY_CHOICES,
                                blank=False,
                                default=BEGINNERRUNNER)
    category_changed = models.BooleanField(default=False, help_text="Has the user changed their category from the default?")
    first_workout_date = models.DateField(null=True, blank=True, help_text="Date of first workout - used for auto-promotion")
    workout_days_count = models.IntegerField(default=0, help_text="Number of unique days with workouts - used for auto-promotion")
    current_streak = models.IntegerField(default=0, help_text="Current consecutive days with workouts")
    longest_streak = models.IntegerField(default=0, help_text="Longest streak of consecutive workout days achieved")

    def __str__(self):
        return self.cec
    
    def get_parent_category(self):
        """
        Returns the parent category (runner or freestyler) for partner matching.
        """
        if self.category in [BEGINNERRUNNER, RUNNER]:
            return 'runner'
        else:  # beginnerfreestyler or freestyler
            return 'freestyler'
    
    def get_eligible_partners(self):
        """
        Returns a queryset of profiles that can be partners.
        Rules:
        - Must be in same parent category (runners with runners, freestylers with freestylers)
        - Must have completed profile (has CEC)
        - Excludes self
        """
        my_parent = self.get_parent_category()
        
        if my_parent == 'runner':
            eligible_categories = [BEGINNERRUNNER, RUNNER]
        else:
            eligible_categories = [BEGINNERFREESTYLER, FREESTYLER]
        
        return Profile.objects.filter(
            category__in=eligible_categories
        ).exclude(
            user=self.user
        ).exclude(
            cec=''
        ).order_by('cec')
    
    def calculate_streaks(self):
        """
        Calculate current and longest workout streaks for this profile.
        Returns a tuple: (current_streak, longest_streak)
        """
        from datetime import timedelta
        
        # Get all unique workout dates for this profile, ordered by date
        workout_dates = Workout.objects.filter(
            belongs_to=self
        ).dates('date_time', 'day').order_by('date_time__date')
        
        if not workout_dates:
            return 0, 0
        
        # Convert to list for easier processing
        dates_list = list(workout_dates)
        
        # Calculate longest streak
        longest = 1
        current = 1
        
        for i in range(1, len(dates_list)):
            # Check if dates are consecutive (difference of 1 day)
            if (dates_list[i] - dates_list[i-1]).days == 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        
        # Calculate current streak (from most recent date backwards)
        from django.utils import timezone
        today = timezone.now().date()
        
        current_streak = 0
        if dates_list:
            most_recent = dates_list[-1]
            
            # Only count as current streak if it includes today or yesterday
            days_since_last = (today - most_recent).days
            
            if days_since_last <= 1:
                # Start from most recent and go backwards
                current_streak = 1
                for i in range(len(dates_list) - 2, -1, -1):
                    if (dates_list[i+1] - dates_list[i]).days == 1:
                        current_streak += 1
                    else:
                        break
            # If more than 1 day since last workout, streak is broken
            else:
                current_streak = 0
        
        return current_streak, longest


class ProfileForm(ModelForm):
    # Only show Runner and Freestyler in the wizard (not beginner categories)
    # Users will be auto-assigned to beginner categories and promoted after 42km
    WIZARD_CATEGORY_CHOICES = (
        (RUNNER, 'Runner'),
        (FREESTYLER, 'Freestyler'),
    )
    
    category = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=WIZARD_CATEGORY_CHOICES
    )
    
    class Meta:
        model = Profile
        fields = ['cec', 'user_goal_km', 'category']
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Auto-assign to beginner category based on selection
        # This prevents gaming the system - everyone starts as beginner
        if instance.category == RUNNER:
            instance.category = BEGINNERRUNNER
        elif instance.category == FREESTYLER:
            instance.category = BEGINNERFREESTYLER
        
        if commit:
            instance.save()
        return instance


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
    edition = models.IntegerField(default=2025)
    distance = models.DecimalField(verbose_name="KM",
                                   default=0.00,
                                   max_digits=5,
                                   decimal_places=2,
                                   validators=[validate_distance])
    photo_evidence = models.ImageField(verbose_name="Evidence",
                                       validators=[validate_file_size],
                                       storage=PrivateMediaStorage())
    date_time = models.DateTimeField(verbose_name="Date")
    time = models.TimeField(verbose_name="Type",
                            help_text='Workout/Gift',
                          
                            default='00:00')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, default=1)  # Running
    intensity = models.ForeignKey(IntensityLevel, on_delete=models.CASCADE, default=1)  # Light

    is_audited = models.BooleanField(verbose_name="Audited?",
                                  help_text="Already audited?",
                                  default=False)
    is_gift = models.BooleanField(verbose_name="Gift?", help_text="Was this a gift (extra kms)?", default=False)
    
    # Partner Workout Fields
    is_partner_workout = models.BooleanField(
        verbose_name="Partner Workout?",
        help_text="Is this a partner workout (1.5x distance bonus)?",
        default=False
    )
    partner_profile = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='partner_workouts_received',
        help_text="The partner who trained with you"
    )
    partner_confirmed = models.BooleanField(
        verbose_name="Partner Confirmed?",
        help_text="Has the partner confirmed this workout?",
        default=False
    )
    partner_workout_group = models.UUIDField(
        null=True,
        blank=True,
        editable=False,
        help_text="Shared UUID linking both partner workouts together"
    )
    base_distance = models.DecimalField(
        verbose_name="Base Distance (before bonus)",
        default=0.00,
        max_digits=5,
        decimal_places=2,
        help_text="Original distance before 1.5x partner bonus"
    )
    
    def get_parent_category(self):
        """
        Returns the parent category (runner or freestyler) for this workout's profile.
        Used for partner workout validation.
        """
        if self.belongs_to.category in [BEGINNERRUNNER, RUNNER]:
            return 'runner'
        else:  # beginnerfreestyler or freestyler
            return 'freestyler'
    
    def can_partner_with(self, other_profile):
        """
        Validates if the current workout's profile can partner with another profile.
        Rules:
        - Both must be in same parent category (runners or freestylers)
        - Other profile must exist and have a CEC (completed registration)
        - Cannot partner with yourself
        """
        if not other_profile or not other_profile.cec:
            return False, "Partner must have a complete profile with CEC"
        
        if self.belongs_to.user == other_profile.user:
            return False, "Cannot partner with yourself"
        
        # Check parent category match
        my_parent = self.get_parent_category()
        
        if other_profile.category in [BEGINNERRUNNER, RUNNER]:
            partner_parent = 'runner'
        else:
            partner_parent = 'freestyler'
        
        if my_parent != partner_parent:
            return False, f"Partner must be in the same category family (both runners or both freestylers)"
        
        return True, "Valid partner"
    
    def is_expired(self):
        """
        Check if unconfirmed partner workout has expired (older than 2 days)
        """
        from django.utils import timezone
        from datetime import timedelta
        
        if not self.is_partner_workout or self.partner_confirmed:
            return False
        
        expiration_date = self.uploaded_at + timedelta(days=2)
        return timezone.now() > expiration_date
    
    def time_until_expiration(self):
        """
        Return timedelta until expiration (for display purposes)
        Returns None if already expired or not applicable
        """
        from django.utils import timezone
        from datetime import timedelta
        
        if not self.is_partner_workout or self.partner_confirmed:
            return None
        
        expiration_date = self.uploaded_at + timedelta(days=2)
        remaining = expiration_date - timezone.now()
        
        if remaining.total_seconds() <= 0:
            return None  # Already expired
        
        return remaining
    
    def get_expiration_status(self):
        """
        Returns human-readable expiration status
        """
        if not self.is_partner_workout or self.partner_confirmed:
            return None
        
        remaining = self.time_until_expiration()
        
        if remaining is None:
            return "Expired"
        
        hours = int(remaining.total_seconds() // 3600)
        
        if hours < 1:
            minutes = int(remaining.total_seconds() // 60)
            return f"{minutes} minutes remaining"
        elif hours < 24:
            return f"{hours} hours remaining"
        else:
            days = hours // 24
            return f"{days} day{'s' if days != 1 else ''} remaining"
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_goal = models.BooleanField(default=False)
    user_goal_km = models.DecimalField(default=42.00,
                                   max_digits=10,
                                   decimal_places=2,
                                   validators=[validate_min_goal])
    avatar = models.CharField(max_length=400, blank=True, default="https://ciscorunning2023.s3.us-east-1.amazonaws.com/static/img/user.png")
    cec = models.CharField(max_length=30, blank=True, validators=[validate_cec])
    distance = models.DecimalField(default=0.00,
                                   max_digits=10,
                                   decimal_places=2)

    category = models.CharField(max_length=20,
                                choices=CATEGORY_CHOICES,
                                blank=False,
                                default=BEGINNERRUNNER)
    category_changed = models.BooleanField(default=False, help_text="Has the user changed their category from the default?")
    first_workout_date = models.DateField(null=True, blank=True, help_text="Date of first workout - used for auto-promotion")
    workout_days_count = models.IntegerField(default=0, help_text="Number of unique days with workouts - used for auto-promotion")
    current_streak = models.IntegerField(default=0, help_text="Current consecutive days with workouts")
    longest_streak = models.IntegerField(default=0, help_text="Longest streak of consecutive workout days achieved")

    def __str__(self):
        return self.cec
    
    def get_parent_category(self):
        """
        Returns the parent category (runner or freestyler) for partner matching.
        """
        if self.category in [BEGINNERRUNNER, RUNNER]:
            return 'runner'
        else:  # beginnerfreestyler or freestyler
            return 'freestyler'
    
    def get_eligible_partners(self):
        """
        Returns a queryset of profiles that can be partners.
        Rules:
        - Must be in same parent category (runners with runners, freestylers with freestylers)
        - Must have completed profile (has CEC)
        - Excludes self
        """
        my_parent = self.get_parent_category()
        
        if my_parent == 'runner':
            eligible_categories = [BEGINNERRUNNER, RUNNER]
        else:
            eligible_categories = [BEGINNERFREESTYLER, FREESTYLER]
        
        return Profile.objects.filter(
            category__in=eligible_categories
        ).exclude(
            user=self.user
        ).exclude(
            cec=''
        ).order_by('cec')
    
    def calculate_streaks(self):
        """
        Calculate current and longest workout streaks for this profile.
        Returns a tuple: (current_streak, longest_streak)
        """
        from datetime import timedelta
        
        # Get all unique workout dates for this profile, ordered by date
        workout_dates = Workout.objects.filter(
            belongs_to=self
        ).dates('date_time', 'day').order_by('date_time__date')
        
        if not workout_dates:
            return 0, 0
        
        # Convert to list for easier processing
        dates_list = list(workout_dates)
        
        # Calculate longest streak
        longest = 1
        current = 1
        
        for i in range(1, len(dates_list)):
            # Check if dates are consecutive (difference of 1 day)
            if (dates_list[i] - dates_list[i-1]).days == 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        
        # Calculate current streak (from most recent date backwards)
        from django.utils import timezone
        today = timezone.now().date()
        
        current_streak = 0
        if dates_list:
            most_recent = dates_list[-1]
            
            # Only count as current streak if it includes today or yesterday
            days_since_last = (today - most_recent).days
            
            if days_since_last <= 1:
                # Start from most recent and go backwards
                current_streak = 1
                for i in range(len(dates_list) - 2, -1, -1):
                    if (dates_list[i+1] - dates_list[i]).days == 1:
                        current_streak += 1
                    else:
                        break
            # If more than 1 day since last workout, streak is broken
            else:
                current_streak = 0
        
        return current_streak, longest


class ProfileForm(ModelForm):
    # Only show Runner and Freestyler in the wizard (not beginner categories)
    # Users will be auto-assigned to beginner categories and promoted after 42km
    WIZARD_CATEGORY_CHOICES = (
        (RUNNER, 'Runner'),
        (FREESTYLER, 'Freestyler'),
    )
    
    category = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=WIZARD_CATEGORY_CHOICES
    )
    
    class Meta:
        model = Profile
        fields = ['cec', 'user_goal_km', 'category']
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Auto-assign to beginner category based on selection
        # This prevents gaming the system - everyone starts as beginner
        if instance.category == RUNNER:
            instance.category = BEGINNERRUNNER
        elif instance.category == FREESTYLER:
            instance.category = BEGINNERFREESTYLER
        
        if commit:
            instance.save()
        return instance


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
    edition = models.IntegerField(default=2025)
    distance = models.DecimalField(verbose_name="KM",
                                   default=0.00,
                                   max_digits=5,
                                   decimal_places=2,
                                   validators=[validate_distance])
    photo_evidence = models.ImageField(verbose_name="Evidence",
                                       validators=[validate_file_size],
                                       storage=PrivateMediaStorage())
    date_time = models.DateTimeField(verbose_name="Date")
    time = models.TimeField(verbose_name="Type",
                            help_text='Workout/Gift',
                          
                            default='00:00')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, default=1)  # Running
    intensity = models.ForeignKey(IntensityLevel, on_delete=models.CASCADE, default=1)  # Light

    is_audited = models.BooleanField(verbose_name="Audited?",
                                  help_text="Already audited?",
                                  default=False)
    is_gift = models.BooleanField(verbose_name="Gift?", help_text="Was this a gift (extra kms)?", default=False)
    
    # Partner Workout Fields
    is_partner_workout = models.BooleanField(
        verbose_name="Partner Workout?",
        help_text="Is this a partner workout (1.5x distance bonus)?",
        default=False
    )
    partner_profile = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='partner_workouts_received',
        help_text="The partner who trained with you"
    )
    partner_confirmed = models.BooleanField(
        verbose_name="Partner Confirmed?",
        help_text="Has the partner confirmed this workout?",
        default=False
    )
    partner_workout_group = models.UUIDField(
        null=True,
        blank=True,
        editable=False,
        help_text="Shared UUID linking both partner workouts together"
    )
    base_distance = models.DecimalField(
        verbose_name="Base Distance (before bonus)",
        default=0.00,
        max_digits=5,
        decimal_places=2,
        help_text="Original distance before 1.5x partner bonus"
    )
    
    def get_parent_category(self):
        """
        Returns the parent category (runner or freestyler) for this workout's profile.
        Used for partner workout validation.
        """
        if self.belongs_to.category in [BEGINNERRUNNER, RUNNER]:
            return 'runner'
        else:  # beginnerfreestyler or freestyler
            return 'freestyler'
    
    def can_partner_with(self, other_profile):
        """
        Validates if the current workout's profile can partner with another profile.
        Rules:
        - Both must be in same parent category (runners or freestylers)
        - Other profile must exist and
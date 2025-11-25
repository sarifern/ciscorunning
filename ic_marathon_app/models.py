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

class WorkoutForm(ModelForm):
    
    class Meta:
        model = Workout
        fields = ['distance', 'date_time',  'photo_evidence']
        widgets = {
            'date_time': DateTimePickerInput(),
        }

    def clean_date_time(self):
        return validate_date(self.cleaned_data['date_time'])


class PartnerWorkoutForm(ModelForm):
    """Form for submitting partner workouts (Runner category)"""
    partner_profile = forms.ModelChoiceField(
        queryset=Profile.objects.none(),  # Will be set dynamically
        required=True,
        label="Training Partner",
        help_text="Select who you trained with",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Workout
        fields = ['distance', 'date_time', 'photo_evidence', 'partner_profile']
        widgets = {
            'date_time': DateTimePickerInput(),
        }
    
    def __init__(self, *args, **kwargs):
        # Get the current user's profile to filter eligible partners
        user_profile = kwargs.pop('user_profile', None)
        super().__init__(*args, **kwargs)
        
        if user_profile:
            # Set queryset to only eligible partners in same parent category
            self.fields['partner_profile'].queryset = user_profile.get_eligible_partners()
            self.fields['partner_profile'].label_from_instance = lambda obj: f"{obj.user.get_full_name()} ({obj.cec})" if obj.user.get_full_name() else obj.cec
    
    def clean_date_time(self):
        return validate_date(self.cleaned_data['date_time'])
    
    def clean(self):
        cleaned_data = super().clean()
        partner = cleaned_data.get('partner_profile')
        
        if partner and hasattr(self, 'user_profile'):
            # Validate partner compatibility
            temp_workout = Workout(belongs_to=self.user_profile)
            can_partner, message = temp_workout.can_partner_with(partner)
            
            if not can_partner:
                raise forms.ValidationError(message)
        
        return cleaned_data
    


class FSWorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['date_time','time','sport', 'intensity', 'photo_evidence']
        widgets = {
            'date_time': DateTimePickerInput(),
            'time': TimePickerInput(),
        }
    def clean_date_time(self):
        return validate_date(self.cleaned_data['date_time'])


class FSPartnerWorkoutForm(ModelForm):
    """Form for submitting partner workouts (Freestyler category)"""
    partner_profile = forms.ModelChoiceField(
        queryset=Profile.objects.none(),  # Will be set dynamically
        required=True,
        label="Training Partner",
        help_text="Select who you trained with",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Workout
        fields = ['date_time', 'time', 'sport', 'intensity', 'photo_evidence', 'partner_profile']
        widgets = {
            'date_time': DateTimePickerInput(),
            'time': TimePickerInput(),
        }
    
    def __init__(self, *args, **kwargs):
        # Get the current user's profile to filter eligible partners
        user_profile = kwargs.pop('user_profile', None)
        super().__init__(*args, **kwargs)
        
        if user_profile:
            # Set queryset to only eligible partners in same parent category
            self.fields['partner_profile'].queryset = user_profile.get_eligible_partners()
            self.fields['partner_profile'].label_from_instance = lambda obj: f"{obj.user.get_full_name()} ({obj.cec})" if obj.user.get_full_name() else obj.cec
    
    def clean_date_time(self):
        return validate_date(self.cleaned_data['date_time'])
    
    def clean(self):
        cleaned_data = super().clean()
        partner = cleaned_data.get('partner_profile')
        
        if partner and hasattr(self, 'user_profile'):
            # Validate partner compatibility
            temp_workout = Workout(belongs_to=self.user_profile)
            can_partner, message = temp_workout.can_partner_with(partner)
            
            if not can_partner:
                raise forms.ValidationError(message)
        
        return cleaned_data

class WorkoutSerializer(serializers.HyperlinkedModelSerializer):
    belongs_to = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Workout
        fields = ['uuid', 'belongs_to', 'distance', 'date_time', 'time','sport', 'intensity', 'photo_evidence', 'uploaded_at', 'edition']
        read_only_fields = ['uuid', 'belongs_to', 'uploaded_at', 'edition']  # Auto-set fields
    
    def to_representation(self, instance):
        """Return only newly awarded badges after workout creation"""
        # If this is a create operation (has context with newly_awarded_badges)
        if hasattr(self, 'context') and 'newly_awarded_badges' in self.context:
            badges_data = []
            for badge in self.context['newly_awarded_badges']:
                badges_data.append({
                    'slug': badge.badge.slug,
                    'name': badge.badge.name,
                    'description': badge.badge.description,
                    'awarded_at': badge.awarded_at.isoformat() if hasattr(badge, 'awarded_at') else None
                })
            # Return only the badges, not the full workout representation
            return {'newly_awarded_badges': badges_data}
        
        # For non-create operations (GET, PUT, PATCH), return full representation
        return super().to_representation(instance)


@extend_schema(
    tags=['Workouts'],
    description="""
    Manage workouts for the authenticated user.
    
    All workouts are automatically associated with the authenticated user's profile.
    The `belongs_to` field is read-only and set automatically from the auth token.
    """,
)
class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter workouts to only show current user's workouts"""
        # Ensure user has a profile
        if not hasattr(self.request.user, 'profile'):
            return Workout.objects.none()
        
        return Workout.objects.filter(belongs_to=self.request.user.profile).order_by('-date_time')
    
    @extend_schema(
        summary="Create a new workout",
        description="""
        Create a new workout for the authenticated user.
        
        The workout will be automatically associated with your profile.
        After creation, the response will include any newly awarded badges.
        
        **Note:** Use FormData (multipart/form-data) when uploading photo evidence.
        """,
        request=WorkoutSerializer,
        responses={
            201: WorkoutSerializer,
            400: OpenApiTypes.OBJECT,
            403: OpenApiTypes.OBJECT,
        },
    )
    def create(self, request, *args, **kwargs):
        """Create workout with automatic user association"""
        # Check if user has a profile
        if not hasattr(request.user, 'profile'):
            return Response({
                'error': 'Profile required',
                'detail': 'You must create a profile before adding workouts. Use POST /api/profiles/me/'
            }, status=400)
        
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        """Create workout and check for newly awarded badges"""
        # Automatically set belongs_to from authenticated user
        workout = serializer.save(belongs_to=self.request.user.profile)
        
        # Import here to avoid circular dependency
        from ic_marathon_app.views import check_badges
        
        # Check for newly awarded badges after workout is saved
        user = workout.belongs_to.user
        newly_awarded_badges = check_badges(user)
        
        # Store badges in serializer context so they can be included in response
        serializer.context['newly_awarded_badges'] = newly_awarded_badges
        
        # Log new badges
        if newly_awarded_badges:
            badge_names = ', '.join([b.badge.name for b in newly_awarded_badges])
            print(f"🏆 {user.profile.cec} earned new badges: {badge_names}")
    
    @extend_schema(
        summary="Delete a workout",
        description="""
        Delete a workout and recalculate badges.
        
        This will also remove any badges that were only earned because of this workout.
        """,
        responses={
            204: None,
            403: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
    )
    def destroy(self, request, *args, **kwargs):
        """Delete workout with proper authorization check"""
        instance = self.get_object()
        
        # Ensure user owns this workout
        if instance.belongs_to.user != request.user:
            return Response({
                'error': 'Permission denied',
                'detail': 'You can only delete your own workouts'
            }, status=403)
        
        return super().destroy(request, *args, **kwargs)
    
    def perform_destroy(self, instance):
        """Delete workout and strip badges if needed"""
        user = instance.belongs_to.user
        
        # Delete the workout (this triggers signals that update distance/streaks)
        instance.delete()
        
        # Import here to avoid circular dependency
        from ic_marathon_app.views import strip_badges
        
        # Remove badges that no longer apply
        strip_badges(user)



class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    # Only allow selection of Runner or Freestyler via API
    # Backend will auto-assign to beginner categories
    WIZARD_CATEGORY_CHOICES = (
        (RUNNER, 'Runner'),
        (FREESTYLER, 'Freestyler'),
    )
    
    category = serializers.ChoiceField(choices=WIZARD_CATEGORY_CHOICES)
    actual_category = serializers.CharField(read_only=True, help_text="Current progression level (includes beginner status)")
    awarded_badges = serializers.ListField(read_only=True, help_text="List of all badges earned")
   
    class Meta:
        model = Profile
        fields = [
            'user', 'cec', 'category', 'actual_category', 'user_goal_km', 
            'distance', 'current_streak', 'longest_streak', 'workout_days_count',
            'category_changed', 'avatar', 'awarded_badges'
        ]
        read_only_fields = [
            'user', 'distance', 'category_changed', 'current_streak', 
            'longest_streak', 'workout_days_count', 'actual_category', 'awarded_badges'
        ]  # auto-calculated fields
        extra_kwargs = {
            'avatar': {'required': False},  # Make avatar optional
            'cec': {'required': True, 'help_text': 'Your Cisco CEC ID'},
            'category': {'required': True, 'help_text': 'Choose Runner or Freestyler'},
            'user_goal_km': {'required': True, 'help_text': 'Your distance goal in kilometers'},
        }
    
    def validate(self, data):
        # Check if trying to create (not update) and user already has profile
        if not self.instance and self.context.get('request'):
            user = self.context['request'].user
            if Profile.objects.filter(user=user).exists():
                raise serializers.ValidationError(
                    "You already have a profile. Use PUT/PATCH to update it instead of POST."
                )
        
        # Check if user is trying to change category when it's already been changed
        if self.instance and 'category' in data:
            # Get the "intent" category (runner or freestyler)
            new_category_intent = data['category']
            
            # Determine what the current intent is based on actual category
            if self.instance.category in [BEGINNERRUNNER, RUNNER]:
                old_category_intent = RUNNER
            else:  # beginnerfreestyler or freestyler
                old_category_intent = FREESTYLER
            
            # If the intent is changing and has already been changed before
            if old_category_intent != new_category_intent and self.instance.category_changed:
                raise serializers.ValidationError({
                    "category": "You have already changed your category once. Category can only be updated one time.",
                    "current_category": "Runner" if old_category_intent == RUNNER else "Freestyler",
                    "attempted_category": "Runner" if new_category_intent == RUNNER else "Freestyler"
                })
        
        return data
    
    def create(self, validated_data):
        # Auto-assign to beginner category based on selection
        # This prevents gaming the system - everyone starts as beginner
        category = validated_data.get('category')
        if category == RUNNER:
            validated_data['category'] = BEGINNERRUNNER
        elif category == FREESTYLER:
            validated_data['category'] = BEGINNERFREESTYLER
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Track if category intent is being changed
        if 'category' in validated_data:
            new_category = validated_data['category']
            
            # Determine current category intent
            if instance.category in [BEGINNERRUNNER, RUNNER]:
                old_category_intent = RUNNER
            else:
                old_category_intent = FREESTYLER
            
            # If switching between runner and freestyler tracks
            if old_category_intent != new_category:
                validated_data['category_changed'] = True
                # Assign to beginner of the new track
                if new_category == RUNNER:
                    validated_data['category'] = BEGINNERRUNNER
                else:
                    validated_data['category'] = BEGINNERFREESTYLER
            # If staying in same track, don't modify the actual category
            else:
                # Remove category from update to keep current progression
                del validated_data['category']
        
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        # Return the "intent" category (Runner or Freestyler) not the actual beginner status
        ret = super().to_representation(instance)
        
        # Map actual category to intent category for API response
        if instance.category in [BEGINNERRUNNER, RUNNER]:
            ret['category'] = RUNNER
        else:  # beginnerfreestyler or freestyler
            ret['category'] = FREESTYLER
        
        # Add a read-only field showing actual progression
        ret['actual_category'] = instance.get_category_display()
        
        # Add all awarded badges with full details
        from badgify.models import Award
        awarded_badges = Award.objects.filter(user=instance.user).select_related('badge')
        
        badges_data = []
        for award in awarded_badges:
            badges_data.append({
                'slug': award.badge.slug,
                'name': award.badge.name,
                'description': award.badge.description,
                'awarded_at': award.awarded_at.isoformat() if hasattr(award, 'awarded_at') else None
            })
        
        ret['awarded_badges'] = badges_data
        
        return ret

@extend_schema(
    tags=['Profiles'],
    description="""
    Manage your profile via the authenticated user's token.
    
    The profile is automatically associated with the authenticated user.
    Use the `/api/profiles/me/` endpoint for all profile operations.
    """,
)
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Users can only see/edit their own profile"""
        return Profile.objects.filter(user=self.request.user)
    
    def get_serializer_context(self):
        """Make sure request is available in serializer context"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    @extend_schema(
        summary="List all profiles grouped by category",
        description="""
        Returns all profiles grouped by category and sorted by distance (highest to lowest).
        
        Response format:
        ```json
        {
          "beginnerrunner": [...],
          "runner": [...],
          "freestyler": [...],
          "beginnerfreestyler": [...]
        }
        ```
        
        Each profile includes user information and statistics.
        """,
        responses={
            200: OpenApiTypes.OBJECT
        }
    )
    def list(self, request, *args, **kwargs):
        """
        List all profiles grouped by category and sorted by distance.
        Returns profiles organized by category with highest distance first.
        """
        # Get all profiles ordered by distance (highest first)
        all_profiles = Profile.objects.all().select_related('user').order_by('-distance')
        
        # Group profiles by category
        grouped_profiles = {
            BEGINNERRUNNER: [],
            RUNNER: [],
            FREESTYLER: [],
            BEGINNERFREESTYLER: []
        }
        
        for profile in all_profiles:
            serializer = self.get_serializer(profile)
            grouped_profiles[profile.category].append(serializer.data)
        
        # Return grouped data
        return Response(grouped_profiles)
    
    @extend_schema(
        summary="Get, create, update, or delete your own profile",
        description="""
        Manage your own profile using this convenient endpoint.
        
        - **GET**: Retrieve your profile information
        - **POST**: Create a new profile (same as PUT if profile doesn't exist)
        - **PUT**: Create or update your profile (upsert)
        - **PATCH**: Partially update your existing profile
        - **DELETE**: Delete your profile and all associated workouts
        
        Note: The authenticated user is automatically associated with the profile.
        """,
        responses={
            200: ProfileSerializer,
            201: ProfileSerializer,
            204: None,
            404: OpenApiTypes.OBJECT,
        }
    )
    @action(detail=False, methods=['get', 'post', 'put', 'patch', 'delete'], url_path='me')
    def me(self, request):
        """
        Custom endpoint to get/create/update/delete the current user's profile.
        Access via: GET/POST/PUT/PATCH/DELETE /api/profiles/me/
        
        POST and PUT will create the profile if it doesn't exist (upsert behavior)
        """
        try:
            profile = Profile.objects.get(user=request.user)
            profile_exists = True
        except Profile.DoesNotExist:
            profile = None
            profile_exists = False
        
        if request.method == 'GET':
            if not profile_exists:
                return Response({
                    "error": "Profile not found",
                    "detail": "You don't have a profile yet. Use POST/PUT /api/profiles/me/ to create one."
                }, status=404)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        
        elif request.method in ['POST', 'PUT', 'PATCH']:
            if profile_exists:
                # Update existing profile
                partial = request.method == 'PATCH'
                serializer = self.get_serializer(profile, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            else:
                # Create new profile (POST or PUT, but not PATCH)
                if request.method == 'PATCH':
                    return Response({
                        "error": "Profile not found",
                        "detail": "Cannot PATCH a non-existent profile. Use POST/PUT /api/profiles/me/ to create one first."
                    }, status=404)
                
                # Create profile with POST or PUT
                print(f"DEBUG: Creating NEW profile for user: {request.user} via {request.method} /api/profiles/me/")
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(user=request.user)
                print(f"DEBUG: Profile created successfully")
                return Response(serializer.data, status=201)
        
        elif request.method == 'DELETE':
            if not profile_exists:
                return Response({
                    "error": "Profile not found",
                    "detail": "No profile to delete."
                }, status=404)
            
            workout_count = profile.workout_set.count()
            print(f"DEBUG: Deleting profile ID: {profile.id}, CEC: {profile.cec}, User: {profile.user.username}")
            print(f"DEBUG: Deleting profile will also delete {workout_count} associated workouts")
            profile.delete()
            print(f"DEBUG: Profile deleted successfully")
            return Response(status=204)
    
    def perform_create(self, serializer):
        # Debug: Check if user is authenticated
        print(f"DEBUG: Authenticated user: {self.request.user}")
        print(f"DEBUG: Is authenticated: {self.request.user.is_authenticated}")
        
        # Check if user already has a profile
        existing_profiles = Profile.objects.filter(user=self.request.user)
        print(f"DEBUG: Existing profiles count: {existing_profiles.count()}")
        
        if existing_profiles.exists():
            existing_profile = existing_profiles.first()
            print(f"DEBUG: User {self.request.user} already has profile ID: {existing_profile.id}, CEC: {existing_profile.cec}")
            raise ValidationError({
                "error": "Profile already exists",
                "detail": f"User '{self.request.user.username}' already has a profile (ID: {existing_profile.id}, CEC: {existing_profile.cec})",
                "suggestion": "Use GET/PUT/PATCH/DELETE /api/profiles/me/ to access your profile."
            })
        
        # Automatically set the user to the authenticated user when creating a profile
        print(f"DEBUG: Creating NEW profile for user: {self.request.user}")
        serializer.save(user=self.request.user)
        print(f"DEBUG: Profile created successfully")
    
    def perform_destroy(self, instance):
        # Debug: Check which profile is being deleted
        print(f"DEBUG: Deleting profile ID: {instance.id}, CEC: {instance.cec}, User: {instance.user.username}")
        
        # Verify the user owns this profile
        if instance.user != self.request.user:
            print(f"DEBUG: Permission denied - user {self.request.user} tried to delete profile of {instance.user}")
            raise ValidationError({
                "error": "Permission denied",
                "detail": "You can only delete your own profile."
            })
        
        # Delete associated workouts will be handled automatically by CASCADE
        workout_count = instance.workout_set.count()
        print(f"DEBUG: Deleting profile will also delete {workout_count} associated workouts")
        
        # Perform the deletion
        instance.delete()
        print(f"DEBUG: Profile deleted successfully")

@receiver(post_delete, sender=Workout)
def delete_workout(sender, instance, **kwargs):
    # If this is a confirmed partner workout, also delete the partner's matching workout
    if instance.is_partner_workout and instance.partner_confirmed and instance.partner_workout_group:
        # Find and delete the partner's workout
        partner_workouts = Workout.objects.filter(
            partner_workout_group=instance.partner_workout_group
        ).exclude(uuid=instance.uuid)
        partner_workouts.delete()
    
    # Update personal distance (only if it was confirmed/counted)
    profile = instance.belongs_to
    if not (instance.is_partner_workout and not instance.partner_confirmed):
        profile.distance -= instance.distance

    if profile.distance < profile.user_goal_km:
        profile.user_goal = False
    
    # Recalculate unique workout days after deletion
    unique_days = Workout.objects.filter(
        belongs_to=profile
    ).dates('date_time', 'day').count()
    profile.workout_days_count = unique_days
    
    # Recalculate streaks after deletion
    current_streak, longest_streak = profile.calculate_streaks()
    profile.current_streak = current_streak
    profile.longest_streak = longest_streak
    
    # If no workouts left, reset first workout date
    if unique_days == 0:
        profile.first_workout_date = None
    
    profile.save()

    # Delete image from S3
    try:
        default_storage.delete(instance.photo_evidence.name)
    except Exception:
        q("Can't delete the file {} in S3".format(
            instance.photo_evidence.name))


@receiver(post_save, sender=Workout)
def save_workout(sender, instance, **kwargs):
    if instance.is_audited:
        return
    
    # Skip distance updates for unconfirmed partner workouts
    # Distance will be added when partner confirms
    if instance.is_partner_workout and not instance.partner_confirmed:
        return
    
    # Update personal distance
    profile = instance.belongs_to
    profile.distance += Decimal(instance.distance)
    
    # Track first workout date
    if not profile.first_workout_date:
        profile.first_workout_date = instance.date_time.date()
    
    # Count unique workout days for this profile
    unique_days = Workout.objects.filter(
        belongs_to=profile
    ).dates('date_time', 'day').count()
    profile.workout_days_count = unique_days
    
    # Calculate and update streaks
    current_streak, longest_streak = profile.calculate_streaks()
    profile.current_streak = current_streak
    profile.longest_streak = longest_streak
    
    # Log streak milestones
    if current_streak > 0 and current_streak % 7 == 0:
        print(f"🔥 {profile.cec} hit a {current_streak}-day streak!")
    if longest_streak > profile.longest_streak:
        print(f"🏆 {profile.cec} set a new personal record: {longest_streak}-day streak!")
    
    # Anti-sandbagging logic: Detect skilled runners trying to stay in beginner category
    # Calculate average distance per workout to identify experienced runners
    total_workouts = Workout.objects.filter(belongs_to=profile).count()
    avg_distance_per_workout = profile.distance / total_workouts if total_workouts > 0 else 0
    
    # Auto-upgrade logic with MULTIPLE triggers to catch sandbaggers:
    # Path 1: High total distance + consistency (genuine progression)
    high_distance_and_consistent = (
        profile.distance >= 84.0 and
        profile.workout_days_count >= 10
    )
    
    # Path 2: High performance level (experienced runner detected)
    # If averaging 7km+ per workout with at least 5 workouts = clearly experienced
    experienced_runner_detected = (
        total_workouts >= 5 and
        avg_distance_per_workout >= 7.0
    )
    
    # Path 3: Moderate distance but very consistent (dedicated participant)
    # 42km over 15 days = clearly committed and should compete with others
    moderate_but_very_consistent = (
        profile.distance >= 42.0 and
        profile.workout_days_count >= 15
    )
    
    # Promote beginnerrunner to runner if ANY condition is met
    should_promote_runner = (
        profile.category == "beginnerrunner" and
        (high_distance_and_consistent or experienced_runner_detected or moderate_but_very_consistent)
    )
    
    # Promote beginnerfreestyler to freestyler if ANY condition is met
    should_promote_freestyler = (
        profile.category == "beginnerfreestyler" and
        (high_distance_and_consistent or experienced_runner_detected or moderate_but_very_consistent)
    )
    
    if should_promote_runner:
        profile.category = "runner"
        promotion_reason = (
            f"High distance" if high_distance_and_consistent else
            f"Experienced (avg {avg_distance_per_workout:.1f}km/workout)" if experienced_runner_detected else
            f"Very consistent"
        )
        print(f"🎉 Auto-promoted {profile.cec} to Runner! Reason: {promotion_reason} ({profile.distance}km over {profile.workout_days_count} days)")
    
    if should_promote_freestyler:
        profile.category = "freestyler"
        promotion_reason = (
            f"High distance" if high_distance_and_consistent else
            f"Experienced (avg {avg_distance_per_workout:.1f}km/workout)" if experienced_runner_detected else
            f"Very consistent"
        )
        print(f"🎉 Auto-promoted {profile.cec} to Freestyler! Reason: {promotion_reason} ({profile.distance}km over {profile.workout_days_count} days)")
    
    # Check if user reached their goal
    if profile.distance >= profile.user_goal_km:
        profile.user_goal = True
    
    profile.save()

# Reference Data ViewSet - Single endpoint for all workout reference data
@extend_schema(
    tags=['Reference Data'],
    description='Get all workout reference data in a single call'
)
class ReferenceDataViewSet(viewsets.ViewSet):
    """
    API endpoint that returns all reference data needed for workout tracking.
    Returns sports, intensity levels, and their mappings in a single response.
    Read-only endpoint - no authentication required.
    """
    permission_classes = []  # No authentication required
    
    @extend_schema(
        summary="Get all reference data",
        description="""
        Returns all reference data needed for workout tracking in a single call:
        - **sports**: List of available sports
        - **intensity_levels**: List of intensity levels (Light, Moderate, High)
        - **mappings**: Sport-intensity combinations with km/hour equivalents
        
        """,
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'sports': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'name': {'type': 'string'}
                            }
                        }
                    },
                    'intensity_levels': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'name': {'type': 'string'}
                            }
                        }
                    },
                    'mappings': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'sport_id': {'type': 'integer'},
                                'sport_name': {'type': 'string'},
                                'intensity_id': {'type': 'integer'},
                                'intensity_name': {'type': 'string'},
                                'km_per_hour': {'type': 'number'}
                            }
                        }
                    }
                }
            }
        }
    )
    def list(self, request):
        """
        Get all reference data in a single response.
        """
        # Get all sports
        sports = Sport.objects.all().order_by('name')
        sports_data = [{'id': s.id, 'name': s.name} for s in sports]
        
        # Get all intensity levels
        intensities = IntensityLevel.objects.all().order_by('name')
        intensities_data = [{'id': i.id, 'name': i.name} for i in intensities]
        
        # Get all sport-intensity mappings
        mappings = SportIntensityMapping.objects.all().select_related('sport', 'intensity').order_by('sport__name', 'intensity__name')
        mappings_data = [{
            'sport_id': m.sport.id,
            'sport_name': m.sport.name,
            'intensity_id': m.intensity.id,
            'intensity_name': m.intensity.name,
            'km_per_hour': m.km_per_hour
        } for m in mappings]
        
        return Response({
            'sports': sports_data,
            'intensity_levels': intensities_data,
            'mappings': mappings_data
        })

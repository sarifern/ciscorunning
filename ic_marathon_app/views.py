from allauth.socialaccount.models import SocialAccount
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import ProfileForm, Profile, SportIntensityMapping, Workout, WorkoutForm, FSWorkoutForm
from badgify.models import Award, Badge
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .tables import WorkoutTable, ProfileTable
from datetime import datetime
from django_tables2.config import RequestConfig
from django_tables2.paginators import LazyPaginator
from webexteamssdk import WebexTeamsAPI
from webexteamssdk import ApiError
import decimal
import itertools
import os
import pytz as tz
from django.http import JsonResponse
import uuid

WTAPI = WebexTeamsAPI(access_token=os.environ.get("WT_TOKEN"))

DATE_START = datetime(2025, 12, 12, 1, 0, 0).replace(
    tzinfo=tz.timezone("America/Mexico_City")
)
DATE_END = datetime(2026, 1, 7, 0, 0, 0).replace(
    tzinfo=tz.timezone("America/Mexico_City")
)

ACTIVE = False
DATE = datetime.now().replace(tzinfo=tz.timezone("America/Mexico_City"))


@login_required
def home(request):
    global DATE, ACTIVE
    DATE = datetime.now().replace(tzinfo=tz.timezone("America/Mexico_City"))
    if os.environ.get("DEBUG_PREF") == "True":
        # this is on BETA bypass
        DATE = datetime(2025, 12, 15, 0, 0, 0).replace(
            tzinfo=tz.timezone("America/Mexico_City")
        )
    if DATE >= DATE_START and DATE <= DATE_END:
        ACTIVE = True
    else:
        ACTIVE = False
    try:
        if request.user.profile.cec:
            return my_workouts(request)
        else:
            return profile_wizard(request)
    except ObjectDoesNotExist:
        try:
            account_picture = SocialAccount.objects.get(
                user=request.user
            ).extra_data.get(
                "profile",
                "https://ciscorunning2023.s3.us-east-1.amazonaws.com/static/img/user.png",
            )
        except ObjectDoesNotExist:
            account_picture = "https://ciscorunning2023.s3.us-east-1.amazonaws.com/static/img/user.png"
        profile = Profile.objects.get_or_create(user=request.user)[0]
        profile.avatar = account_picture
        profile.save()
        request.user.profile = profile
        request.user.save()
        return profile_wizard(request)


@login_required
def my_profile(request):
    """Returns My Profile information (workouts, distance, remaining days from the Marathon, current position
    in leaderboard)

    Arguments:
        request {Request} -- Request from browser

    Returns:
        rendered template -- Rendered template (my_profile.html) with Profile information as dict
        variables
        {
        'earned_awards': awards,
        'active': ACTIVE,
        'position': position,
        'workout_count': len(workouts),
        'aggr_distance': request.user.profile.distance,
        'remaining_days_per': int(((remaining_days.days)/26)*100), <<percentage for gauge
        'remaining_days': remaining_days.days,
        }
    """
    global DATE, DATE_END, ACTIVE
    
    # Handle category change POST request
    if request.method == "POST" and "change_category" in request.POST:
        from django.utils import timezone
        
        profile = request.user.profile
        new_category = request.POST.get("new_category")
        
        # Check if user can change category
        if not profile.category_changed and new_category in ["runner", "freestyler"]:
            # Determine current category intent
            current_is_runner = profile.category in ["beginnerrunner", "runner"]
            new_is_runner = new_category == "runner"
            
            # Only allow change if switching between runner and freestyler tracks
            if current_is_runner != new_is_runner:
                # ANTI-GAMING MEASURE: Distance limit - only allow change before 40km
                if profile.distance > 40.0:
                    messages.error(
                        request, 
                        f"Cannot change category with {profile.distance}km completed. "
                        f"Category changes are only allowed before reaching 40km to ensure fair competition."
                    )
                    return redirect("my_profile")
                
                # All checks passed - allow the change
                profile.category_changed = True
                
                # Assign to beginner category of new track
                if new_category == "runner":
                    profile.category = "beginnerrunner"
                else:  # freestyler
                    profile.category = "beginnerfreestyler"
                
                profile.save()
                messages.success(
                    request, 
                    f"Your category has been changed to {new_category.title()}! "
                    f"You're now in the Beginner {new_category.title()} category and will progress as you complete workouts. "
                    f"Remember: You can only change once!"
                )
            else:
                messages.warning(request, "You are already in that category track.")
        elif profile.category_changed:
            messages.error(request, "You have already changed your category once. No more changes allowed.")
        else:
            messages.error(request, "Invalid category selection.")
        
        return redirect("my_profile")
    
    # need workouts count, distance count, remaining days
    try:
        workouts = Workout.objects.filter(belongs_to=request.user.profile)
        awards = Award.objects.filter(user=request.user)
        remaining_days = DATE_END - DATE
        list_in_category = Profile.objects.filter(
            category=request.user.profile.category
        ).order_by("-distance")
        list_cec_in_category = list(
            existing_profile for existing_profile in list_in_category
        )
        index = list_cec_in_category.index(request.user.profile) + 1

    except ObjectDoesNotExist:
        workouts = {}
        awards = {}
    
    # Determine current category intent for display
    profile = request.user.profile
    current_category_intent = "runner" if profile.category in ["beginnerrunner", "runner"] else "freestyler"
    
    return render(
        request,
        "ic_marathon_app/my_profile.html",
        {
            "earned_awards": awards,
            "active": ACTIVE,
            "position": index,
            "workout_count": len(workouts),
            "aggr_distance": request.user.profile.distance,
            "aggr_distance_per": int((request.user.profile.distance / 168) * 100),
            "remaining_days_per": int(((remaining_days.days) / 26) * 100),
            "remaining_days": remaining_days.days,
            "current_category_intent": current_category_intent,
            "can_change_category": not profile.category_changed,
        },
    )


@login_required
def my_workouts(request):
    """Returns the Profile's workouts as a table, the profile's awards, and when the challenge is active, it enables
    the Workout Add button (with the ENV variable as STAGE or PROD)

    Arguments:
        request {Request} -- Request from the browser

    Returns:
        Rendered Template -- Rendered template (my workouts) with dictionary

        {
        'workouts': workouts_table,
        'earned_awards': awards,
        'active': active,
        }
    """
    global ACTIVE
    try:
        workouts = Workout.objects.filter(belongs_to=request.user.profile).order_by(
            "date_time"
        )
        workouts_table = WorkoutTable(workouts)

        awards = Award.objects.filter(user=request.user)
        
        # Check for pending partner workout requests (requests received, not expired)
        from django.utils import timezone
        from datetime import timedelta
        expiration_threshold = timezone.now() - timedelta(days=2)
        pending_requests_count = Workout.objects.filter(
            partner_profile=request.user.profile,
            is_partner_workout=True,
            partner_confirmed=False,
            uploaded_at__gte=expiration_threshold
        ).count()

    except ObjectDoesNotExist:
        workouts = {}
        awards = {}
        pending_requests_count = 0
    return render(
        request,
        "ic_marathon_app/my_workouts.html",
        {
            "workouts": workouts_table,
            "earned_awards": awards,
            "active": ACTIVE,
            "category": request.user.profile.category,
            "pending_requests_count": pending_requests_count,
        },
    )

def convert_to_km(sport_name, intensity_name, duration_minutes):
    try:
        mapping = SportIntensityMapping.objects.get(
            sport__name=sport_name,
            intensity__name=intensity_name
        )
        return mapping.km_per_hour * (duration_minutes / 60.0)
    except SportIntensityMapping.DoesNotExist:
        return None  # or handle gracefully

@login_required
def add_workout_fs(request):
    """View to handle the Add Workout form for freestyle category

    Arguments:
        request {Request} -- The Request from the browser

    Returns:
        rendered template -- Rendered template regarding successful or failed workout add
    """
    if request.method == "POST":
        form = FSWorkoutForm(request.POST, request.FILES)
        form.instance.belongs_to = request.user.profile
        if form.is_valid():
            form.instance.distance = convert_to_km(form.instance.sport, form.instance.intensity, form.instance.time.hour * 60 + form.instance.time.minute)
            
            form.save()
            new_badges = check_badges(request.user)
            if new_badges:
                try:
                    for badge in new_badges:
                        if badge.slug == "ownK":
                            WTAPI.messages.create(
                                roomId=os.environ.get("WT_ROOMID"),
                                markdown=f"Congratulations <@personEmail:{request.user.profile.cec}@cisco.com> for achieving your badge!\n Keep it up!"
                            )
                    pass
                except ApiError:
                    pass
                return render(
                    request,
                    "ic_marathon_app/add_workoutfs.html",
                    {
                        "form": form,
                        "new_badges": new_badges,
                    },
                )
            else:
                return redirect("home")
        else:
            return render(
                request,
                "ic_marathon_app/add_workoutfs.html",
                {
                    "form": form,
                },
            )
    else:
        form = FSWorkoutForm()
        return render(
            request,
            "ic_marathon_app/add_workoutfs.html",
            {
                "form": form,
            },
        )


@login_required
def add_workout(request):
    """View to handle the Add Workout form

    Arguments:
        request {Request} -- The Request from the browser

    Returns:
        rendered template -- Rendered template regarding successful or failed workout add
    """
    if request.method == "POST":
        form = WorkoutForm(request.POST, request.FILES)
        form.instance.belongs_to = request.user.profile
        if form.is_valid():
            form.save()
            new_badges = check_badges(request.user)
            if new_badges:
                try:
                    for badge in new_badges:
                        if badge.slug == "ownK":
                            WTAPI.messages.create(
                                roomId=os.environ.get("WT_ROOMID"),
                                markdown=f"Congratulations <@personEmail:{request.user.profile.cec}@cisco.com> for achieving your badge!\n Keep it up!"
                                
                            )
                except ApiError:
                    pass
                return render(
                    request,
                    "ic_marathon_app/add_workout.html",
                    {
                        "form": form,
                        "new_badges": new_badges,
                    },
                )
            else:
                return redirect("home")
        else:
            return render(
                request,
                "ic_marathon_app/add_workout.html",
                {
                    "form": form,
                },
            )
    else:
        form = WorkoutForm()
        return render(
            request,
            "ic_marathon_app/add_workout.html",
            {
                "form": form,
            },
        )


@login_required
def delete_workout(request, uuid):
    """View to handle the Delete Workout form

    Arguments:
        request {Request} -- The Request from the browser

    Returns:
        rendered template -- Redirect to My Workouts
    """
    if uuid:
        workout = get_object_or_404(Workout, uuid=uuid)
        workout.delete()
        request.user.profile.save()
        strip_badges(request.user)
        return redirect("home")


# ========== PARTNER WORKOUT VIEWS ==========

@login_required
def add_partner_workout(request):
    """View to handle partner workout submission for runners
    
    Arguments:
        request {Request} -- The Request from the browser
    
    Returns:
        rendered template -- Rendered template for partner workout submission
    """
    from .models import PartnerWorkoutForm
    from decimal import Decimal
    
    if request.method == "POST":
        form = PartnerWorkoutForm(request.POST, request.FILES, user_profile=request.user.profile)
        form.instance.belongs_to = request.user.profile
        
        if form.is_valid():
            # Save the workout with partner workout flag
            workout = form.save(commit=False)
            workout.is_partner_workout = True
            workout.partner_confirmed = False
            workout.base_distance = workout.distance  # Store base distance
            workout.partner_workout_group = uuid.uuid4()  # Generate group ID
            workout.save()
            
            messages.success(
                request,
                f"Partner workout submitted! Waiting for {workout.partner_profile.cec} to confirm. "
                f"Once confirmed, you'll both receive {float(workout.base_distance) * 1.5}km!"
            )
            
            return redirect("pending_partner_requests")
        else:
            return render(
                request,
                "ic_marathon_app/add_partner_workout.html",
                {"form": form},
            )
    else:
        form = PartnerWorkoutForm(user_profile=request.user.profile)
        return render(
            request,
            "ic_marathon_app/add_partner_workout.html",
            {"form": form},
        )


@login_required
def add_partner_workoutfs(request):
    """View to handle partner workout submission for freestylers
    
    Arguments:
        request {Request} -- The Request from the browser
    
    Returns:
        rendered template -- Rendered template for freestyler partner workout submission
    """
    from .models import FSPartnerWorkoutForm
    from decimal import Decimal
    
    if request.method == "POST":
        form = FSPartnerWorkoutForm(request.POST, request.FILES, user_profile=request.user.profile)
        form.instance.belongs_to = request.user.profile
        
        if form.is_valid():
            # Calculate distance from time, sport, and intensity
            form.instance.distance = convert_to_km(
                form.instance.sport,
                form.instance.intensity,
                form.instance.time.hour * 60 + form.instance.time.minute
            )
            
            # Save the workout with partner workout flag
            workout = form.save(commit=False)
            workout.is_partner_workout = True
            workout.partner_confirmed = False
            workout.base_distance = workout.distance  # Store base distance
            workout.partner_workout_group = uuid.uuid4()  # Generate group ID
            workout.save()
            
            messages.success(
                request,
                f"Partner workout submitted! Waiting for {workout.partner_profile.cec} to confirm. "
                f"Once confirmed, you'll both receive {float(workout.base_distance) * 1.5}km!"
            )
            
            return redirect("pending_partner_requests")
        else:
            return render(
                request,
                "ic_marathon_app/add_partner_workoutfs.html",
                {"form": form},
            )
    else:
        form = FSPartnerWorkoutForm(user_profile=request.user.profile)
        return render(
            request,
            "ic_marathon_app/add_partner_workoutfs.html",
            {"form": form},
        )


def convert_partner_to_solo_workout(workout):
    """
    Helper function to convert a partner workout to a regular solo workout
    
    Arguments:
        workout {Workout} -- The workout to convert
    
    Returns:
        workout {Workout} -- The converted workout
    """
    workout.is_partner_workout = False
    workout.partner_confirmed = False
    workout.distance = workout.base_distance  # Use base distance only (no bonus)
    workout.partner_profile = None
    workout.partner_workout_group = None
    workout.save()
    return workout


@login_required
def confirm_partner_workout(request, workout_uuid):
    """View to handle partner workout confirmation
    
    Arguments:
        request {Request} -- The Request from the browser
        workout_uuid {UUID} -- UUID of the workout to confirm
    
    Returns:
        rendered template -- Confirmation page or redirect after confirmation
    """
    from decimal import Decimal
    
    # Get the original workout
    original_workout = get_object_or_404(Workout, uuid=workout_uuid)
    
    # Check if expired
    if original_workout.is_expired():
        # Convert to regular solo workout (no bonus)
        convert_partner_to_solo_workout(original_workout)
        messages.warning(
            request, 
            f"This partner workout request has expired (older than 2 days). "
            f"It has been converted to a solo workout with {float(original_workout.base_distance)}km (no bonus)."
        )
        return redirect("home")
    
    # Verify the current user is the tagged partner
    if original_workout.partner_profile.user != request.user:
        messages.error(request, "You are not authorized to confirm this workout.")
        return redirect("home")
    
    # Check if already confirmed
    if original_workout.partner_confirmed:
        messages.info(request, "This partner workout has already been confirmed.")
        return redirect("home")
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "confirm":
            # Mark original as confirmed
            original_workout.partner_confirmed = True
            original_workout.distance = original_workout.base_distance * Decimal("1.5")
            original_workout.save()
            
            # Create matching workout for partner
            partner_workout = Workout.objects.create(
                belongs_to=request.user.profile,
                distance=original_workout.distance,  # Same distance with 1.5x bonus
                base_distance=original_workout.base_distance,
                photo_evidence=original_workout.photo_evidence,  # Share same photo
                date_time=original_workout.date_time,
                time=original_workout.time,
                sport=original_workout.sport,
                intensity=original_workout.intensity,
                is_partner_workout=True,
                partner_confirmed=True,
                partner_profile=original_workout.belongs_to,  # Link back to original user
                partner_workout_group=original_workout.partner_workout_group,  # Share same group ID
                is_audited=False
            )
            
            messages.success(
                request,
                f"🤝 Partner workout confirmed! You both earned {float(original_workout.distance)}km "
                f"({float(original_workout.base_distance)}km × 1.5 bonus)"
            )
            
            # Check for new badges for both users
            check_badges(request.user)
            check_badges(original_workout.belongs_to.user)
            
            return redirect("home")
        
        elif action == "decline":
            # Convert to regular solo workout (no bonus) instead of deleting
            convert_partner_to_solo_workout(original_workout)
            messages.info(
                request, 
                f"Partner workout request declined. The workout has been converted to a solo workout "
                f"for {original_workout.belongs_to.cec} with {float(original_workout.base_distance)}km (no bonus)."
            )
            return redirect("home")
    
    # GET request - show confirmation page with expiration info
    return render(
        request,
        "ic_marathon_app/confirm_partner_workout.html",
        {
            "workout": original_workout,
            "bonus_distance": float(original_workout.base_distance) * 1.5,
            "expiration_status": original_workout.get_expiration_status(),
        },
    )


@login_required
def pending_partner_requests(request):
    """View to show pending partner workout requests
    
    Arguments:
        request {Request} -- The Request from the browser
    
    Returns:
        rendered template -- List of pending partner workout requests
    """
    from django.utils import timezone
    from datetime import timedelta
    
    # Calculate expiration threshold (2 days ago)
    expiration_threshold = timezone.now() - timedelta(days=2)
    
    # Workouts initiated by current user (waiting for partner confirmation)
    # Exclude expired workouts
    requests_sent = Workout.objects.filter(
        belongs_to=request.user.profile,
        is_partner_workout=True,
        partner_confirmed=False,
        uploaded_at__gte=expiration_threshold  # Only workouts less than 2 days old
    ).select_related('partner_profile').order_by('-uploaded_at')
    
    # Add bonus_distance and expiration info to each workout for template
    for workout in requests_sent:
        workout.bonus_distance = float(workout.base_distance) * 1.5
        workout.expiration_status = workout.get_expiration_status()
    
    # Workouts where current user is tagged as partner (needs to confirm)
    # Exclude expired workouts
    requests_received = Workout.objects.filter(
        partner_profile=request.user.profile,
        is_partner_workout=True,
        partner_confirmed=False,
        uploaded_at__gte=expiration_threshold  # Only workouts less than 2 days old
    ).select_related('belongs_to').order_by('-uploaded_at')
    
    # Add bonus_distance and expiration info to each workout for template
    for workout in requests_received:
        workout.bonus_distance = float(workout.base_distance) * 1.5
        workout.expiration_status = workout.get_expiration_status()
    
    return render(
        request,
        "ic_marathon_app/pending_partner_requests.html",
        {
            "requests_sent": requests_sent,
            "requests_received": requests_received,
            "active": ACTIVE,
        },
    )


@login_required
def get_category_members(request):
    """API endpoint to get eligible partners for the current user
    
    Arguments:
        request {Request} -- The Request from the browser
    
    Returns:
        JsonResponse -- List of eligible partners
    """
    eligible_partners = request.user.profile.get_eligible_partners()
    
    partners_data = [
        {
            "id": profile.id,
            "cec": profile.cec,
            "category": profile.get_category_display(),
            "distance": float(profile.distance),
        }
        for profile in eligible_partners
    ]
    
    return JsonResponse({"partners": partners_data})


@login_required
def leaderboard(request):
    """View to handle the Delete Workout form

    Arguments:
        request {Request} -- The Request from the browser

    Returns:
        rendered template -- Rendered templates with 3 tables (sorted by descending distance)
    """
    try:
        earned_awards = Award.objects.filter(user=request.user)
    except ObjectDoesNotExist:
        earned_awards = {}

    
    leaders_br = Profile.objects.filter(category="beginnerrunner").order_by("-distance")
    leaders_r = Profile.objects.filter(category="runner").order_by("-distance")
    leaders_bf = Profile.objects.filter(category="beginnerfreestyler").order_by("-distance")
    leaders_f = Profile.objects.filter(category="freestyler").order_by("-distance")

    total_workouts = Workout.objects.all()
    total_kms = 0
    for workout in total_workouts:
        total_kms += workout.distance
    table_leaders_br = ProfileTable(leaders_br, prefix="leaders-br-")
    table_leaders_r = ProfileTable(leaders_r, prefix="leaders-r-")
    table_leaders_bf = ProfileTable(leaders_bf, prefix="leaders-bf-")
    table_leaders_f = ProfileTable(leaders_f, prefix="leaders-f-")
    RequestConfig(request, paginate={"per_page": 10}).configure(table_leaders_br)
    RequestConfig(request, paginate={"per_page": 10}).configure(table_leaders_r)
    RequestConfig(request, paginate={"per_page": 10}).configure(table_leaders_bf)
    RequestConfig(request, paginate={"per_page": 10}).configure(table_leaders_f)

    list_tables = [(table_leaders_br,len(leaders_br),"Beginner Runners"),
                   (table_leaders_r,len(leaders_r),"Advanced Runners"),
                   (table_leaders_bf,len(leaders_bf),"Beginner Freestylers"),
                   (table_leaders_f,len(leaders_f),"Advanced Freestylers")]

    match request.user.profile.category:
        case "beginnerrunner":
            list_tables.insert(0, list_tables.pop(0))
        case "runner":
            list_tables.insert(0, list_tables.pop(1))
        case "beginnerfreestyler":
            list_tables.insert(0, list_tables.pop(2))
        case "freestyler":
            list_tables.insert(0, list_tables.pop(3))


    return render(
        request,
        "ic_marathon_app/leaderboard.html",
        {
            "tables": list_tables,
            "earned_awards": earned_awards,
            "total_kms": total_kms,
        },
    )


@login_required
def profile_wizard(request):
    """View to fill Profile form

    Arguments:
        request {Request} -- The Request from the browser

    Returns:
        rendered template -- Render to My workouts, with modal for successful activation
    """
    profile = Profile.objects.get_or_create(user=request.user)[0]
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            wtFlag = False
            wtParticipantFlag = False
            try:
                WTAPI.memberships.create(
                    roomId=os.environ.get("WT_ROOMID"),
                    personEmail=profile.cec + "@cisco.com",
                    isModerator=False,
                )
                WTAPI.messages.create(
                    roomId=os.environ.get("WT_ROOMID"),
                    markdown=f"Let's welcome <@personEmail:{profile.cec}@cisco.com> to the challenge! \nGive your best!"
                )
            except ApiError as api_error:
                if "User is already a participant" in api_error.error_message:
                    wtParticipantFlag = True
                else:
                    wtFlag = True
            return render(
                request,
                "ic_marathon_app/profile_wizard.html",
                {"form": form, "activation": True, "wtFlag": wtFlag,
                 "wtParticipantFlag": wtParticipantFlag},
            )
    else:
        form = ProfileForm(instance=profile)
    return render(
        request,
        "ic_marathon_app/profile_wizard.html",
        {
            "form": form,
        },
    )


def check_badges(user):
    """Check awarded badges for each user

    Arguments:
        user {User} -- Session user

    Returns:
        new_badges {[Award]} -- list of Award objects
    """
    distance = user.profile.distance
    current_streak = user.profile.current_streak
    longest_streak = user.profile.longest_streak
    
    new_badges = []
    
    # Distance badges
    if distance >= 10.0:
        new_badge = award_badge(user=user, slug="10K")
        if new_badge:
            new_badges.append(new_badge)
    if distance >= 21.0:
        new_badge = award_badge(user=user, slug="21K")
        if new_badge:
            new_badges.append(new_badge)
    if distance >= 42.0:
        new_badge = award_badge(user=user, slug="42K")
        if new_badge:
            new_badges.append(new_badge)
    if distance >= 84.0:
        new_badge = award_badge(user=user, slug="84K")
        if new_badge:
            new_badges.append(new_badge)
    if distance >= 126.0:
        new_badge = award_badge(user=user, slug="126K")
        if new_badge:
            new_badges.append(new_badge)
    if distance >= 168.0:
        new_badge = award_badge(user=user, slug="168K")
        if new_badge:
            new_badges.append(new_badge)
    if distance >= user.profile.user_goal_km:
        new_badge = award_badge(user=user, slug="ownK")
        if new_badge:
            new_badges.append(new_badge)
    
    # Streak badges (based on longest streak achieved, not current)
    if longest_streak >= 7:
        new_badge = award_badge(user=user, slug="7day-streak")
        if new_badge:
            new_badges.append(new_badge)
    if longest_streak >= 14:
        new_badge = award_badge(user=user, slug="14day-streak")
        if new_badge:
            new_badges.append(new_badge)
    if longest_streak >= 21:
        new_badge = award_badge(user=user, slug="21day-streak")
        if new_badge:
            new_badges.append(new_badge)

    return new_badges


def strip_badges(user):
    """Strip badges if workouts are deleted (if applicable)

    Arguments:
        user {User} -- Session User
    """
    distance = user.profile.distance
    longest_streak = user.profile.longest_streak
    
    # Distance badges
    if distance < 168.0 and get_award(user, slug="168K"):
        get_award(user, slug="168K").delete()
    if distance < 126.0 and get_award(user, slug="126K"):
        get_award(user, slug="126K").delete()
    if distance < 84.0 and get_award(user, slug="84K"):
        get_award(user, slug="84K").delete()
    if distance < 42.0 and get_award(user, slug="42K"):
        get_award(user, slug="42K").delete()
    if distance < 21.0 and get_award(user, slug="21K"):
        get_award(user, slug="21K").delete()
    if distance < 10.0 and get_award(user, slug="10K"):
        get_award(user, slug="10K").delete()
    if distance < user.profile.user_goal_km and get_award(user, slug="ownK"):
        get_award(user, slug="ownK").delete()
    
    # Streak badges (based on longest streak, never removed once earned)
    # Note: longest_streak never decreases, so these badges stay forever
    if longest_streak < 21 and get_award(user, slug="21day-streak"):
        get_award(user, slug="21day-streak").delete()
    if longest_streak < 14 and get_award(user, slug="14day-streak"):
        get_award(user, slug="14day-streak").delete()
    if longest_streak < 7 and get_award(user, slug="7day-streak"):
        get_award(user, slug="7day-streak").delete()


def award_badge(user, slug):
    """Award new badge if applicable

    Arguments:
        user {User} -- Request User
        slug {string} -- Unique slug for each badge

    Returns:
        new_badge -- New Award for the User, if it is created return new_badge, if not return None
    """
    new_badge = Badge.objects.get(slug=slug)
    obj, created = Award.objects.get_or_create(user=user, badge=new_badge)
    if created:
        return new_badge
    else:
        return None


def get_award(user, slug):
    """Get awarded badge for user and unique slug

    Arguments:
        user {Request} -- Session user
        slug {string} -- Unique slug name of Badge

    Returns:
        award -- Award if found, if not return None
    """
    try:
        old_badge = Badge.objects.get(slug=slug)
        return Award.objects.get(user=user, badge=old_badge)
    except:
        # Award not granted
        return None


def float_to_decimal(f):
    "Convert a floating point number to a Decimal with no loss of information"
    n, d = f.as_integer_ratio()
    numerator, denominator = decimal.Decimal(n), decimal.Decimal(d)
    ctx = decimal.Context(prec=60)
    result = ctx.divide(numerator, denominator)
    while ctx.flags[decimal.Inexact]:
        ctx.flags[decimal.Inexact] = False
        ctx.prec *= 2
        result = ctx.divide(numerator, denominator)
    return result

def get_sport_intensity_mappings(request):
    """Return all sport intensity mappings as JSON for frontend calculations"""
    mappings = SportIntensityMapping.objects.select_related('sport', 'intensity').all()
    data = {}
    for mapping in mappings:
        sport_name = mapping.sport.name
        intensity_name = mapping.intensity.name
        if sport_name not in data:
            data[sport_name] = {}
        data[sport_name][intensity_name] = float(mapping.km_per_hour)
    return JsonResponse(data)

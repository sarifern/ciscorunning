from social_django.views import _do_login
from social_core.actions import do_auth, do_complete, do_disconnect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import ProfileForm, Profile, Workout, WorkoutForm, FSWorkoutForm
from badgify.models import Award, Badge
from django.shortcuts import redirect, render, get_object_or_404
from .tables import WorkoutTable, ProfileTable
from datetime import datetime
from django_tables2.config import RequestConfig
from django_tables2.paginators import LazyPaginator
from webexteamssdk import WebexTeamsAPI
from webexteamssdk import ApiError
from decimal import *
import itertools
import os
import pytz as tz

WTAPI = WebexTeamsAPI(access_token=os.environ.get('WT_TOKEN'))

DATE_START = datetime(2022, 12, 12, 1, 0,
                      0).replace(tzinfo=tz.timezone('America/Mexico_City'))
DATE_END = datetime(2023, 1, 7, 0, 0,
                    0).replace(tzinfo=tz.timezone('America/Mexico_City'))



    




# Create your views here.


def login(request):
    """Login view, implements Django Auth Package

    Arguments:
        request {Request} -- Request from the browser.

    Returns:
        rendered template -- Rendered template depending on successful or failed auth.
    """
    return render(request, 'registration/login.html')


@login_required
def home(request):
    DATE = datetime.now().replace(tzinfo=tz.timezone('America/Mexico_City'))
    if os.environ.get('DEBUG_PREF') == 'True':
        # this is on BETA bypass
        DATE = datetime(2022, 12, 15, 0, 0,
                    0).replace(tzinfo=tz.timezone('America/Mexico_City'))
    if DATE >= DATE_START and DATE <= DATE_END:
        active = True
    else:
        active = False
    if request.user.profile.cec:
        return my_workouts(request,active)
    else:
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
    # need workouts count, distance count, remaining days
    try:
        workouts = Workout.objects.filter(belongs_to=request.user.profile)
        awards = Award.objects.filter(user=request.user)
        remaining_days = DATE_END - DATE
        list_in_category = Profile.objects.filter(
            category=request.user.profile.category).order_by('-distance')
        list_cec_in_category = list(existing_profile
                                    for existing_profile in list_in_category)
        index = list_cec_in_category.index(request.user.profile) + 1

    except ObjectDoesNotExist:
        workouts = {}
        awards = {}
    return render(
        request, 'ic_marathon_app/my_profile.html', {
            'earned_awards': awards,
            'active': ACTIVE,
            'position': index,
            'workout_count': len(workouts),
            'aggr_distance': request.user.profile.distance,
            'aggr_distance_per': int(
                (request.user.profile.distance / 168) * 100),
            'remaining_days_per': int(((remaining_days.days) / 26) * 100),
            'remaining_days': remaining_days.days,
        })


@login_required
def my_workouts(request,active):
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
    try:
        workouts = Workout.objects.filter(
            belongs_to=request.user.profile).order_by('date_time')
        workouts_table = WorkoutTable(workouts)

        awards = Award.objects.filter(user=request.user)

    except ObjectDoesNotExist:
        workouts = {}
        awards = {}
    return render(
        request, 'ic_marathon_app/my_workouts.html', {
            'workouts': workouts_table,
            'earned_awards': awards,
            'active': active,
            'category': request.user.profile.category
        })


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
            # add table
            if form.instance.intensity == "light":
                factor = 0.7
            elif form.instance.intensity == "medium":
                factor = 0.85
            elif form.instance.intensity == "high":
                factor = 1
            form.instance.distance = float_to_decimal(
                (form.instance.time.hour * 60 + form.instance.time.minute) /
                12 * factor)
            form.save()
            new_badges = check_badges(request.user)
            if new_badges:
                try:
                    for badge in new_badges:
                        if badge.slug == "ownK":
                            WTAPI.messages.create(
                                roomId=os.environ.get('WT_ROOMID'),
                                text="Congratulations " +
                                request.user.first_name + " (" +
                                request.user.profile.cec +
                                ") for achieving your badge!\n Keep it up!",
                                files=[badge.image.url])
                    pass
                except ApiError:
                    pass
                return render(request, 'ic_marathon_app/add_workoutfs.html', {
                    'form': form,
                    'new_badges': new_badges,
                })
            else:
                return redirect('home')
        else:
            return render(request, 'ic_marathon_app/add_workoutfs.html', {
                'form': form,
            })
    else:
        form = FSWorkoutForm()
        return render(request, 'ic_marathon_app/add_workoutfs.html', {
            'form': form,
        })


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
                                roomId=os.environ.get('WT_ROOMID'),
                                text="Congratulations " +
                                request.user.first_name + " (" +
                                request.user.profile.cec +
                                ") for achieving your badge!\n Keep it up!",
                                files=[badge.image.url])
                except ApiError:
                    pass
                return render(request, 'ic_marathon_app/add_workout.html', {
                    'form': form,
                    'new_badges': new_badges,
                })
            else:
                return redirect('home')
        else:
            return render(request, 'ic_marathon_app/add_workout.html', {
                'form': form,
            })
    else:
        form = WorkoutForm()
        return render(request, 'ic_marathon_app/add_workout.html', {
            'form': form,
        })


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
        return redirect('home')


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
    leaders_br = Profile.objects.filter(
        category="beginnerrunner").order_by('-distance')
    leaders_r = Profile.objects.filter(category="runner").order_by('-distance')
    leaders_b = Profile.objects.filter(category="biker").order_by('-distance')
    leaders_d = Profile.objects.filter(
        category="duathloner").order_by('-distance')
    leaders_f = Profile.objects.filter(
        category="freestyler").order_by('-distance')

    total_workouts = Workout.objects.all()
    total_kms = 0
    for workout in total_workouts:
        total_kms += workout.distance
    table_leaders_br = ProfileTable(leaders_br, prefix="leaders-br-")
    table_leaders_r = ProfileTable(leaders_r, prefix="leaders-r-")
    table_leaders_b = ProfileTable(leaders_b, prefix="leaders-b-")
    table_leaders_d = ProfileTable(leaders_d, prefix="leaders-d-")
    table_leaders_f = ProfileTable(leaders_f, prefix="leaders-f-")
    RequestConfig(request, paginate={
        "per_page": 10
    }).configure(table_leaders_br)
    RequestConfig(request, paginate={
        "per_page": 10
    }).configure(table_leaders_r)
    RequestConfig(request, paginate={
        "per_page": 10
    }).configure(table_leaders_b)
    RequestConfig(request, paginate={
        "per_page": 10
    }).configure(table_leaders_d)
    RequestConfig(request, paginate={
        "per_page": 10
    }).configure(table_leaders_f)

    return render(
        request, 'ic_marathon_app/leaderboard.html', {
            'leaders_br': table_leaders_br,
            'leaders_br_c': len(leaders_br),
            'leaders_r': table_leaders_r,
            'leaders_r_c': len(leaders_r),
            'leaders_b': table_leaders_b,
            'leaders_b_c': len(leaders_b),
            'leaders_d': table_leaders_d,
            'leaders_d_c': len(leaders_d),
            'leaders_f': table_leaders_f,
            'leaders_f_c': len(leaders_f),
            'earned_awards': earned_awards,
            'total_kms': total_kms
        })


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
            try:
                WTAPI.memberships.create(roomId=os.environ.get('WT_ROOMID'),
                                         personEmail=profile.cec +
                                         "@cisco.com",
                                         isModerator=False)
                WTAPI.messages.create(
                    roomId=os.environ.get('WT_ROOMID'),
                    text="Let's welcome " + request.user.first_name + " (" +
                    profile.cec + ") to the challenge! \nGive your best!",
                    markdown=None)
            except ApiError:
                wtFlag = True
            return render(request, 'ic_marathon_app/profile_wizard.html', {
                'form': form,
                'activation': True,
                'wtFlag': wtFlag
            })
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'ic_marathon_app/profile_wizard.html', {
        'form': form,
    })


def check_badges(user):
    """Check awarded badges for each user

    Arguments:
        user {User} -- Session user

    Returns:
        new_badges {[Award]} -- list of Award objects
    """
    distance = user.profile.distance
    new_badges = []
    if distance >= 10.0:
        new_badge = award_badge(user=user, slug='10K')
        if new_badge:
            new_badges.append(new_badge)
    if distance >= 21.0:
        new_badge = award_badge(user=user, slug='21K')
        if new_badge:
            new_badges.append(new_badge)
    if distance >= 42.0:
        new_badge = award_badge(user=user, slug='42K')
        if new_badge:
            new_badges.append(new_badge)
    if distance >= 84.0:
        new_badge = award_badge(user=user, slug='84K')
        if new_badge:
            new_badges.append(new_badge)
    if distance >= 126.0:
        new_badge = award_badge(user=user, slug='126K')
        if new_badge:
            new_badges.append(new_badge)
    if distance >= 168.0:
        new_badge = award_badge(user=user, slug='168K')
        if new_badge:
            new_badges.append(new_badge)
    if distance >= user.profile.user_goal_km:
        new_badge = award_badge(user=user, slug="ownK")
        if new_badge:
            new_badges.append(new_badge)

    return new_badges


def strip_badges(user):
    """Strip badges if workouts are deleted (if applicable)

    Arguments:
        user {User} -- Session User
    """
    distance = user.profile.distance
    if distance < 168.0 and get_award(user, slug='168K'):
        get_award(user, slug='168K').delete()
    if distance < 126.0 and get_award(user, slug='126K'):
        get_award(user, slug='126K').delete()
    if distance < 84.0 and get_award(user, slug='84K'):
        get_award(user, slug='84K').delete()
    if distance < 42.0 and get_award(user, slug='42K'):
        get_award(user, slug='42K').delete()
    if distance < 21.0 and get_award(user, slug='21K'):
        get_award(user, slug='21K').delete()
    if distance < 10.0 and get_award(user, slug='10K'):
        get_award(user, slug='10K').delete()
    if distance < user.profile.user_goal_km and get_award(user, slug='ownK'):
        get_award(user, slug='ownK').delete()
    

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


NAMESPACE = 'social'
REDIRECT_FIELD_NAME = 'next'


def complete(request, backend, *args, **kwargs):
    """Authentication complete view OVERRIDE

    Arguments:
        request {Request} -- Request from Browser
        backend {string} -- Authentication Backend

    """
    return do_complete(request.backend,
                       _do_login,
                       user=None,
                       redirect_name=REDIRECT_FIELD_NAME,
                       request=request,
                       *args,
                       **kwargs)


def float_to_decimal(f):
    "Convert a floating point number to a Decimal with no loss of information"
    n, d = f.as_integer_ratio()
    numerator, denominator = Decimal(n), Decimal(d)
    ctx = Context(prec=60)
    result = ctx.divide(numerator, denominator)
    while ctx.flags[Inexact]:
        ctx.flags[Inexact] = False
        ctx.prec *= 2
        result = ctx.divide(numerator, denominator)
    return result
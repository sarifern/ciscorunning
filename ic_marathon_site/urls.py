"""ic_marathon_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from ic_marathon_app import views
from ic_marathon_app import auth_views as ic_auth_views
from rest_framework import routers
from ic_marathon_app import models
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView




router = routers.DefaultRouter()
router.register(r'workouts', models.WorkoutViewSet, 'workout')
router.register(r'profiles', models.ProfileViewSet, 'profile')
router.register(r'reference-data', models.ReferenceDataViewSet, 'reference-data')
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Routes
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    
    # API Authentication
    path('api/auth/strava/', ic_auth_views.strava_token_auth, name='strava-token-auth'),
    
    # API Documentation (Swagger UI - Modern, interactive API docs)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Legacy Web Routes (for admin/auditing only)
    path("", views.home, name="home"),
    path("profile_wizard/", views.profile_wizard, name="profile_wizard"),
    path("my_workouts/", views.my_workouts, name="my_workouts"),
    path("my_profile/", views.my_profile, name="my_profile"),
    path("add_workout/", views.add_workout, name="add_workout"),
    path("add_workout_fs/", views.add_workout_fs, name="add_workout_fs"),
    path("delete_workout/<uuid>/", views.delete_workout, name="delete_workout"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),

    path('accounts/', include('allauth.urls')),
    path('select2/', include('django_select2.urls')),
    path('badges/',include('badgify.urls')),
]

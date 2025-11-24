from django.contrib import admin
from .models import Workout, Profile
from django.utils.html import format_html
# Register your models here.

from .models import Sport, IntensityLevel, SportIntensityMapping

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(IntensityLevel)
class IntensityLevelAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(SportIntensityMapping)
class SportIntensityMappingAdmin(admin.ModelAdmin):
    list_display = ['sport', 'intensity', 'km_per_hour']
    list_filter = ['sport', 'intensity']
    search_fields = ['sport__name']
    
class WorkoutAdmin(admin.ModelAdmin):
    list_display = (
        'is_audited', 
        'date_time', 
        'uploaded_at', 
        'belongs_to', 
        'distance', 
        'partner_status',
        'image_tag'
    )
    list_filter = [
        'is_audited', 
        'is_partner_workout',
        'partner_confirmed',
        'belongs_to', 
        'uploaded_at', 
        'date_time'
    ]
    search_fields = ['belongs_to__cec', 'partner_profile__cec']
    
    def partner_status(self, obj):
        """Display partner workout status with color coding"""
        if not obj.is_partner_workout:
            return format_html('<span style="color: gray;">Regular</span>')
        elif obj.partner_confirmed:
            partner_name = obj.partner_profile.cec if obj.partner_profile else "Unknown"
            return format_html(
                '<span style="color: green;">✓ Partner</span><br/>'
                '<small>with {}</small><br/>'
                '<small>Base: {}km × 1.5 = {}km</small>',
                partner_name,
                obj.base_distance,
                obj.distance
            )
        else:
            partner_name = obj.partner_profile.cec if obj.partner_profile else "Unknown"
            return format_html(
                '<span style="color: orange;">⏳ Pending</span><br/>'
                '<small>Waiting for {}</small>',
                partner_name
            )
    partner_status.short_description = 'Partner Status'

    def image_tag(self, obj):
        if obj.photo_evidence:
            return format_html(
            '<img src="{}" width="600px" height="600px"/>'.format(
                obj.photo_evidence.url))


admin.site.register(Workout, WorkoutAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'cec', 'user_goal', 'distance')
    list_filter = ['user', 'cec']


admin.site.register(Profile, ProfileAdmin)

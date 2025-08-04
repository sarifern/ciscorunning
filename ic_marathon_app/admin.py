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
    list_display = ('is_audited', 'date_time', 'uploaded_at', 'belongs_to', 'distance', 'image_tag')
    list_filter = ['is_audited', 'belongs_to', 'uploaded_at', 'date_time']

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

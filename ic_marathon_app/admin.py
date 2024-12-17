from django.contrib import admin
from .models import Workout, Profile
from django.utils.html import format_html
# Register your models here.


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('is_audited', 'date_time', 'belongs_to', 'distance', 'image_tag')
    list_filter = ['is_audited', 'belongs_to', 'date_time']

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

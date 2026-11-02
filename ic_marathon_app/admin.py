from django.contrib import admin
from .models import Workout, Profile
from django.utils.html import format_html
from django.utils.safestring import mark_safe
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
        'evidence_photos'
    )
    readonly_fields = ('evidence_photos_large',)
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
        """Display partner workout status with color coding and expiration info"""
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
        elif obj.is_expired():
            partner_name = obj.partner_profile.cec if obj.partner_profile else "Unknown"
            return format_html(
                '<span style="color: red;">✗ Expired</span><br/>'
                '<small>Was waiting for {}</small>',
                partner_name
            )
        else:
            partner_name = obj.partner_profile.cec if obj.partner_profile else "Unknown"
            expiration_status = obj.get_expiration_status()
            return format_html(
                '<span style="color: orange;">⏳ Pending</span><br/>'
                '<small>Waiting for {}</small><br/>'
                '<small style="color: #ff6b00;">{}</small>',
                partner_name,
                expiration_status
            )
    partner_status.short_description = 'Partner Status'

    EVIDENCE_FIELDS = (
        ('photo_evidence', 'My Evidence'),
        ('partner_photo_evidence', 'Their Evidence'),
        ('partner_selfie', 'Our Selfie'),
    )

    def _render_evidence(self, obj, size):
        cells = []
        for field_name, label in self.EVIDENCE_FIELDS:
            image = getattr(obj, field_name, None)
            if image:
                cells.append(format_html(
                    '<div style="display:inline-block;text-align:center;'
                    'margin-right:10px;vertical-align:top;">'
                    '<div><small><strong>{}</strong></small></div>'
                    '<a href="{}" target="_blank" rel="noopener">'
                    '<img src="{}" style="width:{}px;height:{}px;'
                    'object-fit:cover;border:1px solid #ccc;"/></a></div>',
                    label, image.url, image.url, size, size
                ))
            else:
                cells.append(format_html(
                    '<div style="display:inline-block;text-align:center;'
                    'margin-right:10px;vertical-align:top;">'
                    '<div><small><strong>{}</strong></small></div>'
                    '<div style="width:{}px;height:{}px;border:1px dashed #ccc;'
                    'color:#999;font-size:11px;display:flex;align-items:center;'
                    'justify-content:center;">None</div></div>',
                    label, size, size
                ))
        return format_html('<div style="white-space:nowrap;">{}</div>',
                           mark_safe(''.join(cells)))

    def evidence_photos(self, obj):
        return self._render_evidence(obj, 120)
    evidence_photos.short_description = 'Evidence (Mine / Theirs / Selfie)'

    def evidence_photos_large(self, obj):
        return self._render_evidence(obj, 400)
    evidence_photos_large.short_description = 'Evidence (Mine / Theirs / Selfie)'


admin.site.register(Workout, WorkoutAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'cec', 'user_goal', 'distance')
    list_filter = ['user', 'cec']


admin.site.register(Profile, ProfileAdmin)

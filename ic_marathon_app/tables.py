import django_tables2 as tables
from django_tables2 import TemplateColumn
from django.utils.html import format_html
from .models import Workout, Profile
from badgify.models import Award
from pytz import timezone
import itertools


class ProfileTable(tables.Table):
    award = tables.Column(empty_values=())
    position = tables.Column(verbose_name="#", empty_values=(), 
                             orderable=False)

    def render_position(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count())
        return int(next(self.row_counter))+self.page.start_index()
    
    def render_award(self, value, record):
        awards_html = ""
        earned_awards = Award.objects.filter(
            user=record.user).order_by('-awarded_at')
        if earned_awards:
            awards_html += '<img src="{}" height="42" width="42"/>'.format(
                earned_awards[0].badge.image.url)
        return format_html(awards_html)

    def render_avatar(self, value, record):
        return format_html('<img src="{}" height="42" width="42"/>', value)

    class Meta:
        model = Profile
        template = "django_tables2/bootstrap-responsive.html"
        attrs = {"class": "table table--striped table--wrapped"}
        fields = ("position", "avatar", "cec", "distance", "award")


class WorkoutTable(tables.Table):
    delete = TemplateColumn(
        template_name='tables/workout_delete_column.html')

    def render_date_time(self, value):
        return format_html("{}", value.astimezone(timezone('America/Mexico_City')).strftime("%Y-%m-%d"))

    def render_time(self,record ):
        if record.is_gift:
            return format_html("GIFT KM")
        else:
            return format_html("Workout")

    def render_distance(self, value):
        return format_html("{} K", value)

    def render_photo_evidence(self, value):
        return format_html('<img src="{}" height="42" width="42"/>', value.url)

        
    class Meta:
        model = Workout
        template = "django_tables2/bootstrap-responsive.html"
        attrs = {"class": "table table--striped"}
        fields = ("date_time", "distance","time",  "delete")

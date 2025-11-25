# Partner Workouts - 2-Day Expiration Implementation Guide

## 📋 Overview
This document outlines how to add a 2-day expiration mechanism to partner workout requests. If User B doesn't confirm or reject within 2 days, the partner workout request will automatically expire and be deleted.

## 🎯 What Changes Are Needed

### 1. **Database Changes** (OPTI2. Add a new job to run every 10 minutes or hourly:
   ```
   python manage.py cleanup_expired_partner_workouts --settings=ic_marathon_site.$ENVIRONMENT
   ``` - `uploaded_at` already exists!)
✅ **Good news**: The `Workout` model already has### Step 2: Create Management Command
1. Create the directory structure if it doesn't exist:
   ```bash
   mkdir -p ic_marathon_app/management/commands
   echo. > ic_marathon_app/management/__init__.py
   echo. > ic_marathon_app/management/commands/__init__.py
   ```

2. Create `cleanup_expired_partner_workouts.py` file

3. Test it:
   ```bash
   python manage.py cleanup_expired_partner_workouts --dry-run --settings=ic_marathon_site.$env:ENVIRONMENT
   ```at` field that tracks when workouts are created. We can use this for expiration logic without any database changes!

No migration needed! The existing field:
```python
uploaded_at = models.DateTimeField(auto_now_add=True)
```

### 2. **Add Helper Methods to Workout Model**

Add these methods to the `Workout` model in `ic_marathon_app/models.py`:

```python
from django.utils import timezone
from datetime import timedelta

class Workout(models.Model):
    # ...existing fields...
    
    def is_expired(self):
        """
        Check if unconfirmed partner workout has expired (older than 2 days)
        """
        if not self.is_partner_workout or self.partner_confirmed:
            return False
        
        expiration_date = self.uploaded_at + timedelta(days=2)
        return timezone.now() > expiration_date
    
    def time_until_expiration(self):
        """
        Return timedelta until expiration (for display purposes)
        Returns None if already expired or not applicable
        """
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
```

### 3. **Create Management Command for Cleanup**

Create a Django management command to automatically delete expired partner workouts.

**File**: `ic_marathon_app/management/commands/cleanup_expired_partner_workouts.py`

```python
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from ic_marathon_app.models import Workout

class Command(BaseCommand):
    help = 'Delete expired unconfirmed partner workout requests (older than 2 days)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Find unconfirmed partner workouts older than 2 days
        expiration_threshold = timezone.now() - timedelta(days=2)
        
        expired_workouts = Workout.objects.filter(
            is_partner_workout=True,
            partner_confirmed=False,
            uploaded_at__lt=expiration_threshold
        )
        
        count = expired_workouts.count()
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'[DRY RUN] Would delete {count} expired partner workout(s)')
            )
            for workout in expired_workouts:
                self.stdout.write(
                    f'  - Workout {workout.uuid} from {workout.belongs_to.cec} '
                    f'to {workout.partner_profile.cec} '
                    f'(created {workout.uploaded_at})'
                )
        else:
            expired_workouts.delete()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {count} expired partner workout(s)')
            )
```

**How to run the command:**
```bash
# Dry run (see what would be deleted)
python manage.py cleanup_expired_partner_workouts --dry-run --settings=ic_marathon_site.$env:ENVIRONMENT

# Actually delete expired workouts
python manage.py cleanup_expired_partner_workouts --settings=ic_marathon_site.$env:ENVIRONMENT
```

### 4. **Update Views to Filter Expired Workouts**

**Update `pending_partner_requests` view** in `ic_marathon_app/views.py`:

```python
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
```

**Update `confirm_partner_workout` view** in `ic_marathon_app/views.py`:

```python
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
        messages.error(request, "This partner workout request has expired (older than 2 days).")
        original_workout.delete()  # Clean up expired workout
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
                distance=original_workout.distance,
                base_distance=original_workout.base_distance,
                photo_evidence=original_workout.photo_evidence,
                date_time=original_workout.date_time,
                time=original_workout.time,
                sport=original_workout.sport,
                intensity=original_workout.intensity,
                is_partner_workout=True,
                partner_confirmed=True,
                partner_profile=original_workout.belongs_to,
                partner_workout_group=original_workout.partner_workout_group,
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
            # Delete the original workout
            original_workout.delete()
            messages.info(request, "Partner workout request declined and removed.")
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
```

### 5. **Update Templates to Show Expiration Info**

**Update `pending_partner_requests.html`** to show time remaining:

Add expiration warning badges to each pending request:

```html
<!-- In the request cards, add expiration status -->
<div class="card-body">
    <h5 class="card-title">{{ workout.belongs_to.cec }} wants to train with you!</h5>
    
    <!-- Add expiration badge -->
    {% if workout.expiration_status %}
        {% if "hour" in workout.expiration_status or "minute" in workout.expiration_status %}
            <span class="badge badge-warning">⏰ {{ workout.expiration_status }}</span>
        {% else %}
            <span class="badge badge-info">⏰ {{ workout.expiration_status }}</span>
        {% endif %}
    {% endif %}
    
    <p class="card-text">
        <strong>Distance:</strong> {{ workout.base_distance }} km<br>
        <strong>Bonus Distance:</strong> {{ workout.bonus_distance }} km (1.5x)<br>
        <strong>Date:</strong> {{ workout.date_time|date:"M d, Y" }}<br>
        <strong>Requested:</strong> {{ workout.uploaded_at|timesince }} ago
    </p>
    <!-- ...rest of card... -->
</div>
```

**Update `confirm_partner_workout.html`** to show expiration warning:

```html
<!-- Add at the top of the confirmation page -->
{% if expiration_status %}
    <div class="alert alert-warning" role="alert">
        <i class="icon icon-warning"></i>
        <strong>Time Sensitive:</strong> This request will expire in {{ expiration_status }}
    </div>
{% endif %}
```

### 6. **Set Up Automated Cleanup (Cron Job)**

You have several options for running the cleanup command automatically:

#### **Option A: Heroku Scheduler (Recommended for Heroku deployments)**

1. Install Heroku Scheduler add-on:
   ```bash
   heroku addons:create scheduler:standard
   ```

2. Open the scheduler dashboard:
   ```bash
   heroku addons:open scheduler
   ```

3. Add a new job to run every 10 minutes or hourly:
   ```
   python manage.py cleanup_expired_partner_workouts
   ```

#### **Option B: Django-crontab (For server deployments)**

1. Install django-crontab:
   ```bash
   pip install django-crontab
   ```

2. Add to `settings.py`:
   ```python
   INSTALLED_APPS = [
       # ...
       'django_crontab',
   ]
   
   CRONJOBS = [
       # Run every hour
       ('0 * * * *', 'ic_marathon_app.management.commands.cleanup_expired_partner_workouts.Command.handle'),
   ]
   ```

3. Add crontab:
   ```bash
   python manage.py crontab add --settings=ic_marathon_site.$env:ENVIRONMENT
   ```

#### **Option C: Celery Beat (For production with async tasks)**

If you already have Celery set up:

```python
from celery import shared_task
from django.core.management import call_command

@shared_task
def cleanup_expired_workouts():
    call_command('cleanup_expired_partner_workouts')
```

Add to `celery.py`:
```python
from celery.schedules import crontab

app.conf.beat_schedule = {
    'cleanup-expired-partner-workouts': {
        'task': 'ic_marathon_app.tasks.cleanup_expired_workouts',
        'schedule': crontab(minute=0),  # Every hour
    },
}
```

### 7. **Update Admin Interface**

Add expiration indicators in the admin panel.

**Update `ic_marathon_app/admin.py`**:

```python
from django.utils.html import format_html
from django.utils import timezone

class WorkoutAdmin(admin.ModelAdmin):
    # ...existing code...
    
    def partner_status(self, obj):
        """Display partner workout status with color coding"""
        if not obj.is_partner_workout:
            return "-"
        
        if obj.partner_confirmed:
            return format_html(
                '<span style="color: green;">✓ Confirmed</span>'
            )
        elif obj.is_expired():
            return format_html(
                '<span style="color: red;">✗ Expired</span>'
            )
        else:
            status = obj.get_expiration_status()
            return format_html(
                '<span style="color: orange;">⏳ Pending ({})</span>',
                status
            )
    
    partner_status.short_description = 'Partner Status'
    
    # Add to list_display
    list_display = ['uuid', 'belongs_to', 'distance', 'date_time', 'partner_status', ...]
```

## 🚀 Implementation Steps

### Step 1: Add Model Methods
1. Add the three helper methods to the `Workout` model
2. No migration needed (uses existing `uploaded_at` field)

### Step 2: Create Management Command
1. Create the directory structure if it doesn't exist:
   ```bash
   mkdir -p ic_marathon_app/management/commands
   echo. > ic_marathon_app/management/__init__.py
   echo. > ic_marathon_app/management/commands/__init__.py
   ```

2. Create `cleanup_expired_partner_workouts.py` file

3. Test it:
   ```bash
   python manage.py cleanup_expired_partner_workouts --dry-run
   ```

### Step 3: Update Views
1. Update `pending_partner_requests()` to filter expired workouts
2. Update `confirm_partner_workout()` to check expiration
3. Test the views

### Step 4: Update Templates
1. Add expiration badges to `pending_partner_requests.html`
2. Add expiration warning to `confirm_partner_workout.html`

### Step 5: Update Admin (Optional but Recommended)
1. Add expiration status to admin interface
2. Helps auditors see expired requests

### Step 6: Set Up Automation
1. Choose your preferred method (Heroku Scheduler, cron, Celery)
2. Configure to run at least once per hour
3. Test the automation

## 📊 Testing the Expiration Feature

### Test Case 1: Create and Let Expire
```python
# In Django shell
from ic_marathon_app.models import Workout
from django.utils import timezone
from datetime import timedelta

# Create a test partner workout
workout = Workout.objects.create(
    # ...your workout data...
    is_partner_workout=True,
    partner_confirmed=False
)

# Manually set uploaded_at to 3 days ago (for testing)
workout.uploaded_at = timezone.now() - timedelta(days=3)
workout.save()

# Test expiration check
print(workout.is_expired())  # Should return True
print(workout.get_expiration_status())  # Should return "Expired"

# Run cleanup command
from django.core.management import call_command
call_command('cleanup_expired_partner_workouts', '--dry-run')
```

### Test Case 2: Verify Time Remaining Display
```python
# Create recent partner workout
workout = Workout.objects.create(
    # ...your workout data...
    is_partner_workout=True,
    partner_confirmed=False
)

# Check time remaining
print(workout.time_until_expiration())  # Should show ~2 days
print(workout.get_expiration_status())  # Should show "1 day remaining" or similar
```

### Test Case 3: Try to Confirm Expired Workout
1. Create a partner workout
2. Manually set `uploaded_at` to 3 days ago
3. Try to access the confirmation page
4. Should redirect with "expired" message

## 📝 Summary of Changes

| Component | Change Type | Description |
|-----------|-------------|-------------|
| **Workout Model** | Modify | Add 3 helper methods for expiration logic |
| **Management Command** | Create New | `cleanup_expired_partner_workouts.py` |
| **Views** | Modify | Add expiration checks in 2 views |
| **Templates** | Modify | Add expiration status display |
| **Admin** | Modify | Show expiration in admin panel |
| **Scheduler** | Configure | Set up automated cleanup task |

## ⚠️ Important Notes

1. **No Migration Required**: Uses existing `uploaded_at` field
2. **Backward Compatible**: Existing workouts will work fine
3. **Graceful Degradation**: If scheduler fails, workouts just stay longer
4. **Manual Cleanup**: Admins can always run cleanup command manually
5. **User Notification**: Users see time remaining on pending requests

## 🎯 Benefits of This Approach

✅ **Simple**: Minimal code changes
✅ **Efficient**: Leverages existing database field
✅ **User-Friendly**: Shows countdown timers
✅ **Maintainable**: Easy to adjust expiration period
✅ **Testable**: Management command has dry-run mode
✅ **Visible**: Both users and admins see expiration status

## 🔧 Configuration Options

To change the expiration period, update the `timedelta(days=2)` in:
- `Workout.is_expired()`
- `Workout.time_until_expiration()`
- `pending_partner_requests()` view
- `confirm_partner_workout()` view
- Cleanup management command

You could even make it configurable via Django settings:
```python
# settings.py
PARTNER_WORKOUT_EXPIRATION_DAYS = 2

# Then in code:
from django.conf import settings
expiration_threshold = timezone.now() - timedelta(
    days=settings.PARTNER_WORKOUT_EXPIRATION_DAYS
)
```

---

**Ready to implement?** Start with Step 1 and work through each step. The changes are incremental and can be tested at each stage!

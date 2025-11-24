# Partner Workouts Feature - Implementation Guide

## Overview
This feature allows users in the same parent category (runners or freestylers) to submit partner workouts together, earning a 1.5x distance bonus when both confirm the activity.

---

## Phase 1: Backend Models & Database ✅ COMPLETED

### Database Changes

#### New Fields Added to `Workout` Model:

1. **`is_partner_workout`** (BooleanField)
   - Flags if this is a partner workout
   - Default: `False`

2. **`partner_profile`** (ForeignKey to Profile)
   - Links to the training partner's profile
   - `null=True`, `blank=True`
   - `on_delete=SET_NULL` (keeps workout if partner deletes profile)
   - `related_name='partner_workouts_received'`

3. **`partner_confirmed`** (BooleanField)
   - Tracks if partner has confirmed the workout
   - Default: `False`

4. **`partner_workout_group`** (UUIDField)
   - Shared UUID linking both partner workouts together
   - Allows querying both workouts as a pair
   - Auto-generated, not editable

5. **`base_distance`** (DecimalField)
   - Stores original distance before 1.5x bonus
   - Used for auditing and recalculations

### Model Methods Added

#### `Workout.get_parent_category()`
Returns 'runner' or 'freestyler' based on the profile's category.

#### `Workout.can_partner_with(other_profile)`
Validates partner compatibility:
- ✅ Both in same parent category (runners with runners, freestylers with freestylers)
- ✅ Partner has complete profile (CEC filled)
- ✅ Cannot partner with yourself
- Returns: `(True/False, "message")`

#### `Profile.get_parent_category()`
Returns 'runner' or 'freestyler' for the profile.

#### `Profile.get_eligible_partners()`
Returns QuerySet of profiles that can be partners:
- Same parent category
- Has CEC (completed registration)
- Excludes self
- Ordered by CEC

### Forms Created

#### `PartnerWorkoutForm` (Runner Category)
- Fields: `distance`, `date_time`, `photo_evidence`, `partner_profile`
- Partner dropdown dynamically populated with eligible partners
- Validates partner compatibility

#### `FSPartnerWorkoutForm` (Freestyler Category)
- Fields: `date_time`, `time`, `sport`, `intensity`, `photo_evidence`, `partner_profile`
- Partner dropdown dynamically populated with eligible partners
- Validates partner compatibility

### Business Rules Enforced

✅ **Category Matching:**
- Beginner Runner + Runner = ✅ Compatible
- Beginner Runner + Freestyler = ❌ Incompatible
- Beginner Freestyler + Freestyler = ✅ Compatible
- Beginner Freestyler + Runner = ❌ Incompatible

✅ **Profile Requirements:**
- Partner must have logged in and completed profile (has CEC)
- Partner can have zero workouts (new users welcome)
- Cannot select yourself as partner

✅ **Distance Bonus:**
- Base distance stored in `base_distance` field
- Display distance = `base_distance × 1.5`
- Bonus only applied after partner confirmation

---

## Phase 2: Views & Logic ✅ COMPLETED

### Views Implemented:

1. ✅ **`add_partner_workout(request)`**
   - Handles partner workout submission for runners
   - Creates initial workout with `partner_confirmed=False`
   - Generates `partner_workout_group` UUID
   - Stores base distance
   - Shows success message with expected bonus

2. ✅ **`add_partner_workoutfs(request)`**
   - Handles partner workout submission for freestylers
   - Calculates distance from time/sport/intensity
   - Creates workout with partner flag

3. ✅ **`confirm_partner_workout(request, workout_uuid)`**
   - Partner confirmation page
   - Validates partner is the tagged user
   - Creates matching workout for partner
   - Applies 1.5x bonus to both workouts
   - Links via `partner_workout_group`
   - Checks badges for both users

4. ✅ **`pending_partner_requests(request)`**
   - Lists workouts awaiting partner confirmation
   - Shows both sent and received requests
   - Displays workout details and requester info

5. ✅ **`get_category_members(request)`** (API)
   - JSON endpoint returning eligible partners
   - For AJAX/dynamic dropdown population

### Signal Updates Completed:

✅ Updated `save_workout` signal:
- Skips distance calculation for unconfirmed partner workouts
- Distance only added when partner confirms
- Ensures no gaming by requiring confirmation

✅ Updated `delete_workout` signal:
- Deletes partner's matching workout when one is deleted
- Properly updates distance only for confirmed workouts
- Maintains data integrity

### Table & Admin Updates:

✅ **WorkoutTable enhancements:**
- Shows 🤝 Partner indicator with partner name
- Displays base distance and 1.5x calculation
- Shows ⏳ Pending status for unconfirmed

✅ **WorkoutAdmin enhancements:**
- Added `partner_status` column with color coding
- Added filters for `is_partner_workout` and `partner_confirmed`
- Shows partner details and bonus calculations
- Search by partner CEC

---

## Phase 3: Frontend Templates (TO BE IMPLEMENTED)

### Templates to Create:

1. **`add_partner_workout.html`**
   - Partner workout submission form
   - Partner selection dropdown
   - Info box explaining 1.5x bonus

2. **`add_partner_workoutfs.html`**
   - Freestyler partner workout form
   - Sport/intensity selection + partner

3. **`confirm_partner_workout.html`**
   - Partner confirmation page
   - Show workout details and requester
   - Confirm/Decline buttons

4. **`pending_partner_requests.html`**
   - List pending confirmations
   - Notification badge count

### UI Updates Needed:

1. **Add Workout Page:**
   - Add tab/button: `[Regular Workout] [Partner Workout]`

2. **My Workouts Table:**
   - Display partner indicator: `🤝 Partner with [Name]`
   - Show confirmation status if pending

3. **Navigation:**
   - Notification badge for pending requests

---

## Phase 4: Admin Enhancements (TO BE IMPLEMENTED)

### Admin Updates:

1. **`WorkoutAdmin` enhancements:**
   - Add to `list_display`: `is_partner_workout`, `partner_profile`, `partner_confirmed`
   - Add filters: Partner workout status
   - Color coding: Green=confirmed, Yellow=pending
   - Show linked partner workout

2. **Custom Admin Actions:**
   - Approve/reject partner workouts in bulk
   - View both workouts side-by-side

---

## Migration Applied

**Migration:** `0010_add_partner_workout_fields`

Applied successfully with new fields:
- `is_partner_workout`
- `partner_profile_id`
- `partner_confirmed`
- `partner_workout_group`
- `base_distance`

---

## Testing Checklist

### Unit Tests (To Be Created):
- [ ] `Workout.can_partner_with()` validation
- [ ] `Profile.get_eligible_partners()` filtering
- [ ] Partner workout creation
- [ ] Partner confirmation flow
- [ ] Distance calculation (1.5x bonus)
- [ ] Category matching rules

### Integration Tests (To Be Created):
- [ ] Full partner workout submission flow
- [ ] Partner confirmation creates matching workout
- [ ] Distance bonus correctly applied
- [ ] Linked workouts share UUID
- [ ] Pending requests display correctly

### Manual Testing Scenarios:
1. **Happy Path:**
   - User A (Runner) submits partner workout with User B (Runner)
   - User B confirms → both get 1.5x bonus
   
2. **Cross-Category Prevention:**
   - User A (Runner) cannot select User B (Freestyler)
   
3. **Profile Requirement:**
   - Cannot select user without CEC
   - Can select user with CEC but zero workouts

---

## Next Steps

1. ✅ Phase 1: Database & Models - **COMPLETED**
2. ✅ Phase 2: Views & Business Logic - **COMPLETED**
3. ⏳ Phase 3: Frontend Templates & UI - **IN PROGRESS**
4. ⏳ Phase 4: Testing & Documentation
5. ⏳ Phase 5: Polish & Refinements

---

## API Endpoints (Future Enhancement)

Consider adding REST API endpoints for mobile apps:
- `POST /api/partner-workouts/` - Submit partner workout
- `GET /api/partner-workouts/pending/` - List pending confirmations
- `POST /api/partner-workouts/{uuid}/confirm/` - Confirm partner workout
- `GET /api/profiles/eligible-partners/` - Get list of eligible partners

---

## Notes & Considerations

### Anti-Gaming Measures (Future):
- Limit max 3 partner workouts per week
- Max 50% of total distance from partner workouts
- Admin flag for suspicious patterns

### Notification System:
- Email notification when tagged as partner
- Reminder if not confirmed within 48 hours
- Auto-expire unconfirmed workouts after 7 days

### Audit Trail:
- Log who initiated partner workout
- Track confirmation timestamps
- Monitor frequent partnering patterns

---

**Status:** Phase 1 Complete ✅  
**Branch:** `feature/partner-workouts`  
**Last Updated:** 2025-11-24

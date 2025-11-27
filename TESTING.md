# Testing Guide - Cisco Running Challenge 2025

This document provides comprehensive testing procedures for both **end users** and **administrators** of the Cisco Running Challenge application.

---

## 📋 Table of Contents

- [User Testing](#user-testing)
  - [1. Registration & Authentication](#1-registration--authentication)
  - [2. Profile Management](#2-profile-management)
  - [3. Solo Workout Submission](#3-solo-workout-submission)
  - [4. Partner Workout Submission](#4-partner-workout-submission)
  - [5. Badge Achievements](#5-badge-achievements)
  - [6. Streak Tracking](#6-streak-tracking)
  - [7. Category Progression](#7-category-progression)
  - [8. Leaderboards](#8-leaderboards)
- [Admin Testing](#admin-testing)
  - [1. Workout Auditing](#1-workout-auditing)
  - [2. User Management](#2-user-management)
  - [3. Partner Workout Management](#3-partner-workout-management)
  - [4. Badge Administration](#4-badge-administration)
  - [5. Reference Data Management](#5-reference-data-management)
  - [6. System Monitoring](#6-system-monitoring)
- [API Testing](#api-testing)
- [Performance Testing](#performance-testing)
- [Security Testing](#security-testing)

---

## 👤 User Testing

### 1. Registration & Authentication

#### Test Case 1.1: Strava OAuth Flow
**Objective:** Verify user can authenticate via Strava

**Steps:**
1. Navigate to application home page
2. Click "Login with Strava" button
3. Authorize application on Strava (if first time)
4. Get redirected back to application

**Expected Outcome:**
- ✅ Redirected to Strava authorization page
- ✅ Permission scopes clearly displayed (activity:read_all)
- ✅ After authorization, redirected back to application
- ✅ User is logged in
- ✅ Username matches Strava username

**API Test:**
```bash
# Step 1: Get Strava token (manual via OAuth flow)

# Step 2: Authenticate with backend
curl -X POST https://ciscorunning.herokuapp.com/api/auth/strava/ \
  -H "Content-Type: application/json" \
  -d '{"strava_access_token": "YOUR_STRAVA_TOKEN"}'

# Expected: {"token": "abc123...", "user": "username"}
```

#### Test Case 1.2: Session Persistence
**Objective:** Verify user stays logged in across page refreshes

**Steps:**
1. Log in via Strava
2. Refresh page
3. Navigate to different page
4. Close browser and reopen

**Expected Outcome:**
- ✅ User remains logged in after page refresh
- ✅ User remains logged in across different pages
- ✅ Session persists after browser close/reopen (unless cleared)

---

### 2. Profile Management

#### Test Case 2.1: First-Time Profile Creation
**Objective:** Verify user can create initial profile

**Steps:**
1. Log in as new user (no existing profile)
2. System redirects to profile wizard
3. Enter CEC ID
4. Set personal goal (e.g., 42km)
5. Select category (Runner or Freestyler)
6. Submit profile

**Expected Outcome:**
- ✅ Profile creation form displayed
- ✅ CEC field validates format (letters/numbers only)
- ✅ Goal must be ≥ 10km
- ✅ Category selection required (Runner or Freestyler)
- ✅ Upon submission, profile created successfully
- ✅ User assigned to "Beginner Runner" or "Beginner Freestyler"
- ✅ Redirected to dashboard/my profile page

**API Test:**
```bash
curl -X POST https://ciscorunning.herokuapp.com/api/profiles/me/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cec": "johndoe",
    "user_goal_km": 42.00,
    "category": "runner"
  }'

# Expected: Profile created, category set to "beginnerrunner"
```

#### Test Case 2.2: Duplicate Profile Prevention
**Objective:** Verify system prevents creating multiple profiles

**Steps:**
1. Log in as user with existing profile
2. Try to access profile creation endpoint again

**Expected Outcome:**
- ✅ Profile wizard not shown (already has profile)
- ✅ API returns error: "You already have a profile"
- ✅ User directed to profile page instead

**API Test:**
```bash
curl -X POST https://ciscorunning.herokuapp.com/api/profiles/me/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cec": "johndoe",
    "user_goal_km": 84.00,
    "category": "freestyler"
  }'

# Expected: 400 Bad Request - "You already have a profile"
```

#### Test Case 2.3: Update Personal Goal
**Objective:** Verify user can change their distance goal

**Steps:**
1. Navigate to My Profile page
2. Click "Update Goal" button
3. Enter new goal (e.g., change from 42km to 84km)
4. Save changes

**Expected Outcome:**
- ✅ Goal update form displayed
- ✅ New goal validated (must be ≥ 10km)
- ✅ Goal saved successfully
- ✅ Dashboard reflects new goal
- ✅ Progress percentage recalculated

**API Test:**
```bash
curl -X PATCH https://ciscorunning.herokuapp.com/api/profiles/me/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_goal_km": 84.00}'

# Expected: Profile updated, user_goal_km now 84.00
```

#### Test Case 2.4: Category Change (First Time)
**Objective:** Verify user can switch category tracks once

**Prerequisites:** User has < 50km distance, hasn't changed before

**Steps:**
1. Navigate to My Profile
2. Click "Change Category" button
3. Review rules and current stats
4. Select new category (e.g., Runner → Freestyler)
5. Confirm change

**Expected Outcome:**
- ✅ Change Category button visible (not disabled)
- ✅ Rules displayed (one-time only, < 50km required)
- ✅ Current distance shown
- ✅ Confirmation dialog appears
- ✅ After confirmation:
  - Category changed to "Beginner Freestyler"
  - Distance preserved
  - All workouts preserved
  - `category_changed` flag set to true

**API Test:**
```bash
curl -X PATCH https://ciscorunning.herokuapp.com/api/profiles/me/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"category": "freestyler"}'

# Expected: Category changed to "beginnerfreestyler", category_changed = true
```

#### Test Case 2.5: Category Change Blocked (Already Changed)
**Objective:** Verify system prevents multiple category changes

**Prerequisites:** User has already changed category once

**Steps:**
1. Navigate to My Profile
2. Attempt to change category again

**Expected Outcome:**
- ✅ Change Category button disabled or hidden
- ✅ Message displayed: "You have already changed your category once"
- ✅ API returns error if attempted via PATCH

**API Test:**
```bash
curl -X PATCH https://ciscorunning.herokuapp.com/api/profiles/me/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"category": "runner"}'

# Expected: 400 Bad Request - "Already changed category once"
```

#### Test Case 2.6: Category Change Blocked (High Distance)
**Objective:** Verify system prevents category change if distance ≥ 50km

**Prerequisites:** User has ≥ 50km distance

**Steps:**
1. Navigate to My Profile
2. Attempt to change category

**Expected Outcome:**
- ✅ Change Category button disabled
- ✅ Message: "Cannot change category with 50+ km completed"
- ✅ API returns error if attempted

**API Test:**
```bash
# User with 75km distance
curl -X PATCH https://ciscorunning.herokuapp.com/api/profiles/me/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"category": "freestyler"}'

# Expected: 400 Bad Request - "Cannot change with 75km completed"
```

---

### 3. Solo Workout Submission

#### Test Case 3.1: Submit Running Workout
**Objective:** Verify user can submit a running workout

**Steps:**
1. Navigate to "Add Workout" page
2. Select sport: Running
3. Select intensity: Moderate
4. Enter time: 30 minutes
5. Enter/calculate distance: 5km
6. Select date/time
7. Upload photo evidence
8. Submit workout

**Expected Outcome:**
- ✅ Form displays all required fields
- ✅ Sport dropdown populated with options
- ✅ Intensity dropdown populated (Light, Moderate, High)
- ✅ Distance auto-calculated based on sport/intensity/time
- ✅ Photo upload accepts JPEG/PNG
- ✅ Workout saved successfully
- ✅ User redirected to workout list
- ✅ Distance added to profile total
- ✅ Success message displayed

**API Test:**
```bash
curl -X POST https://ciscorunning.herokuapp.com/api/workouts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "distance=5.00" \
  -F "date_time=2024-12-15T08:30:00Z" \
  -F "time=00:30:00" \
  -F "sport=1" \
  -F "intensity=2" \
  -F "photo_evidence=@/path/to/photo.jpg"

# Expected: Workout created, distance added to profile
```

#### Test Case 3.2: Submit Freestyle Workout
**Objective:** Verify user can submit a freestyle workout (cycling, swimming, etc.)

**Steps:**
1. Navigate to "Add Workout (Freestyle)" page
2. Select sport: Cycling
3. Select intensity: High
4. Enter time: 60 minutes
5. Distance auto-calculated (e.g., 30km)
6. Select date/time
7. Upload photo
8. Submit workout

**Expected Outcome:**
- ✅ Freestyle form displayed
- ✅ Sport options include Cycling, Swimming, Hiking, etc.
- ✅ Distance calculated using sport-intensity mapping
- ✅ Distance converted to km equivalent
- ✅ Workout saved with correct distance
- ✅ Profile distance updated

**API Test:**
```bash
curl -X POST https://ciscorunning.herokuapp.com/api/workouts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "distance=30.00" \
  -F "date_time=2024-12-15T10:00:00Z" \
  -F "time=01:00:00" \
  -F "sport=2" \
  -F "intensity=3" \
  -F "photo_evidence=@/path/to/photo.jpg"

# Expected: Workout created with cycling distance
```

#### Test Case 3.3: Validation - Missing Photo
**Objective:** Verify system requires photo evidence

**Steps:**
1. Fill out workout form completely
2. Do NOT upload photo
3. Submit workout

**Expected Outcome:**
- ✅ Form validation error: "Photo evidence is required"
- ✅ Workout not saved
- ✅ User stays on form page

**API Test:**
```bash
curl -X POST https://ciscorunning.herokuapp.com/api/workouts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "distance=5.00" \
  -F "date_time=2024-12-15T08:30:00Z" \
  -F "time=00:30:00" \
  -F "sport=1" \
  -F "intensity=2"

# Expected: 400 Bad Request - "photo_evidence is required"
```

#### Test Case 3.4: Edit Existing Workout
**Objective:** Verify user can modify their workout

**Steps:**
1. Navigate to My Workouts page
2. Click "Edit" on a workout
3. Change distance (e.g., 5km → 6km)
4. Save changes

**Expected Outcome:**
- ✅ Edit form pre-populated with existing data
- ✅ Distance updated successfully
- ✅ Profile total distance recalculated
- ✅ Streak recalculated if date changed

**API Test:**
```bash
curl -X PATCH https://ciscorunning.herokuapp.com/api/workouts/{UUID}/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"distance": "6.00"}'

# Expected: Workout updated, profile distance adjusted
```

#### Test Case 3.5: Delete Workout
**Objective:** Verify user can delete their workout

**Steps:**
1. Navigate to My Workouts page
2. Click "Delete" on a workout
3. Confirm deletion

**Expected Outcome:**
- ✅ Confirmation dialog appears
- ✅ After confirmation, workout deleted
- ✅ Distance subtracted from profile total
- ✅ Streak recalculated
- ✅ Photo removed from S3
- ✅ Workout no longer appears in list

**API Test:**
```bash
curl -X DELETE https://ciscorunning.herokuapp.com/api/workouts/{UUID}/ \
  -H "Authorization: Token YOUR_TOKEN"

# Expected: 204 No Content, workout deleted, distance reversed
```

---

### 4. Partner Workout Submission

#### Test Case 4.1: Submit Partner Workout Request
**Objective:** Verify user can request a partner workout

**Prerequisites:** User has at least one eligible partner in same category

**Steps:**
1. Navigate to "Add Partner Workout" page
2. Select partner from dropdown (filtered by category)
3. Enter workout details (distance, date, photo)
4. Submit request

**Expected Outcome:**
- ✅ Partner dropdown shows only users in same track
- ✅ Cannot select self as partner
- ✅ Workout created with `partner_confirmed=False`
- ✅ Base distance stored
- ✅ Distance NOT added to profile yet
- ✅ Partner receives notification/can view pending request
- ✅ Success message: "Partner request sent"

**Web Test:**
Navigate to `/add_partner_workout/` (runner) or `/add_partner_workoutfs/` (freestyler)

#### Test Case 4.2: View Pending Partner Requests (Sent)
**Objective:** Verify user can see their sent partner requests

**Steps:**
1. Navigate to "Pending Partner Requests" page
2. View "Sent Requests" tab

**Expected Outcome:**
- ✅ List of workouts awaiting partner confirmation
- ✅ Shows partner name, distance, date, photo
- ✅ Status: "Awaiting confirmation from [partner name]"
- ✅ No action buttons (can't cancel)

**Web Test:**
Navigate to `/pending_partner_requests/`

#### Test Case 4.3: View Pending Partner Requests (Received)
**Objective:** Verify user can see partner requests sent to them

**Steps:**
1. Navigate to "Pending Partner Requests" page
2. View "Received Requests" tab

**Expected Outcome:**
- ✅ List of requests from other users
- ✅ Shows requester name, distance, date, photo
- ✅ Two action buttons: "Accept" and "Decline"
- ✅ Workout details clearly displayed

**Web Test:**
Navigate to `/pending_partner_requests/`

#### Test Case 4.4: Accept Partner Workout
**Objective:** Verify partner can accept request and both get bonus

**Prerequisites:** User B has pending request from User A for 10km workout

**Steps:**
1. User B navigates to Pending Requests
2. Reviews workout details
3. Clicks "Accept" button
4. Confirms acceptance

**Expected Outcome:**
- ✅ User A's workout:
  - `partner_confirmed` set to `True`
  - Distance updated: 10km × 1.5 = 15km
  - Added to User A's profile total
- ✅ User B's workout:
  - New workout created automatically
  - Distance: 15km (same as User A)
  - Same date, sport, intensity as original
  - Photo copied/linked
  - Added to User B's profile total
- ✅ Both workouts:
  - Share same `partner_workout_group` UUID
  - Show "🤝 Partner with [name]" indicator
- ✅ Success message: "Partner workout confirmed!"

**Web Test:**
Navigate to `/confirm_partner_workout/{UUID}/` and click Accept

#### Test Case 4.5: Decline Partner Workout
**Objective:** Verify partner can decline request

**Prerequisites:** User B has pending request from User A

**Steps:**
1. User B navigates to Pending Requests
2. Clicks "Decline" button on a request
3. Confirms decline

**Expected Outcome:**
- ✅ User A's workout deleted completely
- ✅ User A's distance unchanged (never added)
- ✅ No workout created for User B
- ✅ Request removed from pending list
- ✅ No notification sent to User A (silent decline)
- ✅ Success message: "Partner request declined"

**Web Test:**
Navigate to `/confirm_partner_workout/{UUID}/` and click Decline

#### Test Case 4.6: Category Mismatch Prevention
**Objective:** Verify runner can't partner with freestyler

**Steps:**
1. User A (Runner) navigates to Add Partner Workout
2. Views partner dropdown

**Expected Outcome:**
- ✅ Dropdown only shows users in runner category
- ✅ Freestylers not visible in dropdown
- ✅ Cannot select cross-category partner

**API Test:**
```bash
# Get eligible partners
curl -X GET https://ciscorunning.herokuapp.com/get_category_members/ \
  -H "Authorization: Token YOUR_TOKEN"

# Expected: Only returns users in same parent category
```

---

### 5. Badge Achievements

#### Test Case 5.1: Distance Badge Award (10K)
**Objective:** Verify badge awarded when reaching 10km

**Prerequisites:** User has 8km total distance

**Steps:**
1. Submit workout with 3km distance
2. Total distance reaches 11km
3. Check profile badges

**Expected Outcome:**
- ✅ "10K Record Smashed" badge automatically awarded
- ✅ Badge notification displayed on screen
- ✅ Badge appears in profile badge gallery
- ✅ Badge shows unlock date
- ✅ API response includes badge in `newly_awarded_badges`

**API Test:**
```bash
curl -X POST https://ciscorunning.herokuapp.com/api/workouts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "distance=3.00" \
  -F "date_time=2024-12-15T08:30:00Z" \
  -F "time=00:20:00" \
  -F "sport=1" \
  -F "intensity=2" \
  -F "photo_evidence=@/path/to/photo.jpg"

# Expected Response includes:
# "newly_awarded_badges": [{
#   "slug": "10K",
#   "name": "10K Record Smashed",
#   "description": "...",
#   "awarded_at": "2024-12-15T08:30:15Z"
# }]
```

#### Test Case 5.2: Streak Badge Award (7-Day)
**Objective:** Verify badge awarded for 7 consecutive workout days

**Prerequisites:** User has worked out 6 consecutive days

**Steps:**
1. Submit workout on 7th consecutive day
2. Check profile badges

**Expected Outcome:**
- ✅ "Week Warrior" badge automatically awarded
- ✅ Badge notification displayed
- ✅ Badge appears in profile
- ✅ Based on `longest_streak` (permanent achievement)

**API Test:**
```bash
# Submit 7th consecutive day workout
curl -X POST https://ciscorunning.herokuapp.com/api/workouts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "distance=3.00" \
  -F "date_time=2024-12-20T08:00:00Z" \
  -F "time=00:20:00" \
  -F "sport=1" \
  -F "intensity=2" \
  -F "photo_evidence=@/path/to/photo.jpg"

# Expected: "7day-streak" badge in newly_awarded_badges
```

#### Test Case 5.3: Personal Goal Badge (ownK)
**Objective:** Verify badge awarded when reaching personal goal

**Prerequisites:** User goal is 42km, current distance is 40km

**Steps:**
1. Submit workout with 3km distance
2. Total distance reaches 43km (exceeds goal)
3. Check profile badges

**Expected Outcome:**
- ✅ "My Milestone" badge automatically awarded
- ✅ Badge notification displayed
- ✅ Badge appears in profile
- ✅ WebEx Teams notification sent (if configured)

**API Test:**
```bash
curl -X POST https://ciscorunning.herokuapp.com/api/workouts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "distance=3.00" \
  -F "date_time=2024-12-21T08:00:00Z" \
  -F "time=00:20:00" \
  -F "sport=1" \
  -F "intensity=2" \
  -F "photo_evidence=@/path/to/photo.jpg"

# Expected: "ownK" badge in newly_awarded_badges
```

#### Test Case 5.4: Multiple Badges in One Workout
**Objective:** Verify multiple badges can be awarded simultaneously

**Prerequisites:** User has 20.5km and 6-day streak

**Steps:**
1. Submit 1km workout on 7th consecutive day
2. Total distance: 21.5km, streak: 7 days
3. Check badges

**Expected Outcome:**
- ✅ "21K Award Unlocked" badge awarded
- ✅ "Week Warrior" badge awarded
- ✅ Both badges in notification
- ✅ Both badges in API response `newly_awarded_badges` array

**API Test:**
```bash
# Expected Response:
# "newly_awarded_badges": [
#   {"slug": "21K", "name": "21K Award Unlocked", ...},
#   {"slug": "7day-streak", "name": "Week Warrior", ...}
# ]
```

#### Test Case 5.5: Badge Persistence
**Objective:** Verify badges never disappear

**Steps:**
1. Earn a badge (e.g., 10K)
2. Delete workouts to reduce distance below 10km
3. Check profile badges

**Expected Outcome:**
- ✅ Badge still appears in profile
- ✅ Badge not removed despite lower distance
- ✅ Badges are permanent achievements

---

### 6. Streak Tracking

#### Test Case 6.1: Start New Streak
**Objective:** Verify streak starts when user works out

**Prerequisites:** User has no recent workouts (streak = 0)

**Steps:**
1. Submit workout today
2. Check profile streak

**Expected Outcome:**
- ✅ Current streak: 1
- ✅ Longest streak: 1 (if first ever)
- ✅ Workout days count: 1

**API Test:**
```bash
# Check profile
curl -X GET https://ciscorunning.herokuapp.com/api/profiles/me/ \
  -H "Authorization: Token YOUR_TOKEN"

# Expected: "current_streak": 1, "longest_streak": 1
```

#### Test Case 6.2: Continue Streak
**Objective:** Verify streak increments on consecutive days

**Prerequisites:** User worked out yesterday (streak = 1)

**Steps:**
1. Submit workout today
2. Check profile streak

**Expected Outcome:**
- ✅ Current streak: 2
- ✅ Longest streak: 2 (updated if > previous longest)

**API Test:**
```bash
curl -X GET https://ciscorunning.herokuapp.com/api/profiles/me/ \
  -H "Authorization: Token YOUR_TOKEN"

# Expected: "current_streak": 2, "longest_streak": 2
```

#### Test Case 6.3: Multiple Workouts Same Day
**Objective:** Verify multiple workouts on same day count as one streak day

**Prerequisites:** User has streak = 5

**Steps:**
1. Submit first workout today (morning)
2. Submit second workout today (evening)
3. Check profile streak

**Expected Outcome:**
- ✅ Current streak: 6 (incremented once, not twice)
- ✅ Workout count: 2 new workouts
- ✅ Workout days count: incremented by 1

**API Test:**
```bash
# After both workouts
curl -X GET https://ciscorunning.herokuapp.com/api/profiles/me/ \
  -H "Authorization: Token YOUR_TOKEN"

# Expected: "current_streak": 6 (not 7)
```

#### Test Case 6.4: Streak Broken
**Objective:** Verify streak resets when skipping a day

**Prerequisites:** User has current streak = 10, longest = 12

**Steps:**
1. Skip one day (no workout yesterday)
2. Submit workout today
3. Check profile streak

**Expected Outcome:**
- ✅ Current streak: 1 (reset)
- ✅ Longest streak: 12 (unchanged - preserved)

**API Test:**
```bash
curl -X GET https://ciscorunning.herokuapp.com/api/profiles/me/ \
  -H "Authorization: Token YOUR_TOKEN"

# Expected: "current_streak": 1, "longest_streak": 12
```

#### Test Case 6.5: Longest Streak Never Decreases
**Objective:** Verify longest streak is permanent record

**Prerequisites:** User achieved 14-day streak previously

**Steps:**
1. Break streak (skip days)
2. Build new streak of 5 days
3. Check profile

**Expected Outcome:**
- ✅ Current streak: 5
- ✅ Longest streak: 14 (never decreased)
- ✅ "Fortnight Champion" badge still visible

**API Test:**
```bash
curl -X GET https://ciscorunning.herokuapp.com/api/profiles/me/ \
  -H "Authorization: Token YOUR_TOKEN"

# Expected: "current_streak": 5, "longest_streak": 14
```

---

### 7. Category Progression

#### Test Case 7.1: Auto-Promotion Path 1 (High Distance + Consistency)
**Objective:** Verify promotion after 84km over 10+ days

**Prerequisites:** User is Beginner Runner with 80km over 9 days

**Steps:**
1. Submit 5km workout (10th unique day)
2. Total: 85km over 10 days
3. Check profile category

**Expected Outcome:**
- ✅ Category auto-promoted to "Runner"
- ✅ Notification displayed: "Promoted to Runner!"
- ✅ User appears in Runner leaderboard
- ✅ Promotion reason logged in console

**API Test:**
```bash
# Submit workout to trigger promotion
curl -X POST https://ciscorunning.herokuapp.com/api/workouts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "distance=5.00" \
  -F "date_time=2024-12-25T08:00:00Z" \
  -F "time=00:30:00" \
  -F "sport=1" \
  -F "intensity=2" \
  -F "photo_evidence=@/path/to/photo.jpg"

# Check profile
curl -X GET https://ciscorunning.herokuapp.com/api/profiles/me/ \
  -H "Authorization: Token YOUR_TOKEN"

# Expected: "actual_category": "Runner"
```

#### Test Case 7.2: Auto-Promotion Path 2 (High Performance)
**Objective:** Verify promotion for 5+ workouts averaging 7km+

**Prerequisites:** Beginner Runner with 4 workouts (10km, 9km, 8km, 7km)

**Steps:**
1. Submit 5th workout: 11km
2. Average: 45km / 5 workouts = 9km per workout
3. Check profile category

**Expected Outcome:**
- ✅ Category auto-promoted to "Runner"
- ✅ Promotion reason: "Experienced (avg 9.0km/workout)"
- ✅ Prevents skilled athletes sandbagging

**API Test:**
```bash
# 5th workout submission
curl -X POST https://ciscorunning.herokuapp.com/api/workouts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "distance=11.00" \
  -F "date_time=2024-12-25T08:00:00Z" \
  -F "time=01:00:00" \
  -F "sport=1" \
  -F "intensity=3" \
  -F "photo_evidence=@/path/to/photo.jpg"

# Expected: Auto-promoted to Runner
```

#### Test Case 7.3: Auto-Promotion Path 3 (Super Consistent)
**Objective:** Verify promotion for 42km over 15+ days

**Prerequisites:** Beginner Runner with 40km over 14 days

**Steps:**
1. Submit 3km workout (15th unique day)
2. Total: 43km over 15 days
3. Check profile category

**Expected Outcome:**
- ✅ Category auto-promoted to "Runner"
- ✅ Promotion reason: "Very consistent"
- ✅ Rewards daily participation

**API Test:**
```bash
# Submit 15th day workout
curl -X POST https://ciscorunning.herokuapp.com/api/workouts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "distance=3.00" \
  -F "date_time=2024-12-25T08:00:00Z" \
  -F "time=00:20:00" \
  -F "sport=1" \
  -F "intensity=2" \
  -F "photo_evidence=@/path/to/photo.jpg"

# Expected: Auto-promoted to Runner
```

#### Test Case 7.4: Stay in Beginner Category
**Objective:** Verify true beginners remain in beginner category

**Prerequisites:** User is Beginner Runner

**Steps:**
1. Submit sporadic workouts (3km, 2km, 4km, 3km over 5 days)
2. Total: 12km over 5 days
3. Check category

**Expected Outcome:**
- ✅ Remains in "Beginner Runner" category
- ✅ No promotion triggered
- ✅ Low average (2.4km/workout)
- ✅ Low total distance
- ✅ Limited workout days

---

### 8. Leaderboards

#### Test Case 8.1: View Category Leaderboard
**Objective:** Verify user can see their category leaderboard

**Steps:**
1. Navigate to Leaderboard page
2. View leaderboard for your category

**Expected Outcome:**
- ✅ User's category leaderboard shown first
- ✅ Ranked by total distance
- ✅ Shows: Rank, Name, Distance, Workouts
- ✅ User's position highlighted
- ✅ Only users in same category shown

**Web Test:**
Navigate to `/leaderboard/`

#### Test Case 8.2: View All Leaderboards
**Objective:** Verify all four category leaderboards available

**Steps:**
1. Navigate to Leaderboard page
2. Switch between category tabs

**Expected Outcome:**
- ✅ Four tabs/sections:
  - Beginner Runner
  - Runner
  - Beginner Freestyler
  - Freestyler
- ✅ Each leaderboard shows correct users
- ✅ Rankings independent per category

**Web Test:**
Navigate to `/leaderboard/` and switch tabs

#### Test Case 8.3: Real-Time Ranking Update
**Objective:** Verify leaderboard updates after workout submission

**Prerequisites:** User is rank 5 with 20km

**Steps:**
1. Submit 10km workout (total: 30km)
2. Refresh leaderboard
3. Check new position

**Expected Outcome:**
- ✅ Ranking recalculated
- ✅ User moves up (e.g., rank 5 → rank 3)
- ✅ Distance updated on leaderboard
- ✅ Other rankings adjusted accordingly

---

## 🛡️ Admin Testing

### 1. Workout Auditing

#### Test Case 1.1: Mark Workout as Audited
**Objective:** Verify admin can audit workout submissions

**Steps:**
1. Log into Django admin (/admin)
2. Navigate to Workouts list
3. Open a workout detail
4. Check "Audited" checkbox
5. Save workout

**Expected Outcome:**
- ✅ Admin can access workout detail
- ✅ Photo evidence displayed
- ✅ "is_audited" checkbox available
- ✅ After saving, workout marked as audited
- ✅ Audit status visible in list view

**Admin URL:**
Navigate to `/admin/ic_marathon_app/workout/`

#### Test Case 1.2: Filter by Audited Status
**Objective:** Verify admin can filter workouts by audit status

**Steps:**
1. Navigate to Workouts list in admin
2. Use filter: "Audited?" → "No"
3. View unaudited workouts

**Expected Outcome:**
- ✅ Filter options available: Yes/No/All
- ✅ Only unaudited workouts shown
- ✅ Can efficiently process audit queue

#### Test Case 1.3: Bulk Audit Workouts
**Objective:** Verify admin can audit multiple workouts at once

**Steps:**
1. Navigate to Workouts list
2. Select multiple workouts (checkboxes)
3. Choose action: "Mark as audited"
4. Execute action

**Expected Outcome:**
- ✅ Multiple workouts can be selected
- ✅ Bulk action available
- ✅ All selected workouts marked as audited
- ✅ Confirmation message displayed

---

### 2. User Management

#### Test Case 2.1: View User Profiles
**Objective:** Verify admin can view all user profiles

**Steps:**
1. Navigate to Profiles list in admin
2. Review profile information

**Expected Outcome:**
- ✅ All profiles listed
- ✅ Shows: User, CEC, Category, Distance, Goal
- ✅ Can search by CEC or username
- ✅ Can filter by category

**Admin URL:**
Navigate to `/admin/ic_marathon_app/profile/`

#### Test Case 2.2: Edit User Profile
**Objective:** Verify admin can modify user profiles

**Steps:**
1. Open a profile detail
2. Change goal (e.g., 42km → 100km)
3. Save profile

**Expected Outcome:**
- ✅ Admin can edit profile fields
- ✅ Goal updated successfully
- ✅ Changes reflected in user dashboard

**Warning:**
- ⚠️ Avoid manually changing `distance` (auto-calculated)
- ⚠️ Avoid manually changing `category` (auto-promoted)

#### Test Case 2.3: Manually Award Badge
**Objective:** Verify admin can manually award badges to users

**Steps:**
1. Navigate to Badgify > Awards
2. Click "Add Award"
3. Select user
4. Select badge
5. Save award

**Expected Outcome:**
- ✅ Award created successfully
- ✅ Badge appears in user profile
- ✅ Badge shown in awarded_badges API response

**Admin URL:**
Navigate to `/admin/badgify/award/`

---

### 3. Partner Workout Management

#### Test Case 3.1: View Partner Workout Status
**Objective:** Verify admin can see partner workout confirmation status

**Steps:**
1. Navigate to Workouts list in admin
2. Look for "Partner Status" column
3. View partner workouts

**Expected Outcome:**
- ✅ Partner Status column visible
- ✅ Color-coded indicators:
  - 🟢 Green: Confirmed
  - 🟠 Orange: Pending
  - ⚪ Blank: Solo workout
- ✅ Shows partner name

**Admin URL:**
Navigate to `/admin/ic_marathon_app/workout/`

#### Test Case 3.2: Filter Partner Workouts
**Objective:** Verify admin can filter by partner workout type

**Steps:**
1. Navigate to Workouts list
2. Use filter: "Is partner workout?" → "Yes"
3. Use filter: "Partner confirmed?" → "No"

**Expected Outcome:**
- ✅ Shows only partner workouts
- ✅ Shows only unconfirmed partner workouts
- ✅ Can identify pending requests

#### Test Case 3.3: Search by Partner CEC
**Objective:** Verify admin can search for partner workouts

**Steps:**
1. Navigate to Workouts list
2. Use search box
3. Enter partner's CEC

**Expected Outcome:**
- ✅ Returns workouts where searched CEC is the partner
- ✅ Can track specific user's partner activity

---

### 4. Badge Administration

#### Test Case 4.1: View All Badges
**Objective:** Verify admin can see all available badges

**Steps:**
1. Navigate to Badgify > Badges
2. Review badge list

**Expected Outcome:**
- ✅ All badges listed:
  - 10K, 21K, 42K, 84K, 126K, 168K, ownK
  - 7day-streak, 14day-streak, 21day-streak
- ✅ Shows badge slug, name, description
- ✅ Can edit badge details

**Admin URL:**
Navigate to `/admin/badgify/badge/`

#### Test Case 4.2: View Badge Awards
**Objective:** Verify admin can see who earned which badges

**Steps:**
1. Navigate to Badgify > Awards
2. Filter by badge or user
3. Review awards

**Expected Outcome:**
- ✅ All awards listed
- ✅ Shows: User, Badge, Award Date
- ✅ Can filter by badge type
- ✅ Can filter by user

**Admin URL:**
Navigate to `/admin/badgify/award/`

#### Test Case 4.3: Remove Badge Award
**Objective:** Verify admin can revoke badges if needed

**Steps:**
1. Navigate to Badgify > Awards
2. Select an award
3. Delete award

**Expected Outcome:**
- ✅ Award deleted successfully
- ✅ Badge removed from user profile
- ✅ Badge no longer in API response

**Use Case:** Fix erroneous badge awards

---

### 5. Reference Data Management

#### Test Case 5.1: Manage Sports
**Objective:** Verify admin can add/edit sports

**Steps:**
1. Navigate to Sports list in admin
2. Add new sport (e.g., "Rock Climbing")
3. Save sport

**Expected Outcome:**
- ✅ Sport added successfully
- ✅ Available in workout form dropdowns
- ✅ Can be mapped to intensity levels

**Admin URL:**
Navigate to `/admin/ic_marathon_app/sport/`

#### Test Case 5.2: Manage Intensity Levels
**Objective:** Verify admin can view intensity levels

**Steps:**
1. Navigate to Intensity Levels list
2. View existing levels (Low, Moderate, High)

**Expected Outcome:**
- ✅ Three levels visible
- ✅ Can edit level names if needed

**Admin URL:**
Navigate to `/admin/ic_marathon_app/intensitylevel/`

#### Test Case 5.3: Manage Sport-Intensity Mappings
**Objective:** Verify admin can set km/hour equivalents

**Steps:**
1. Navigate to Sport Intensity Mappings
2. Add new mapping (e.g., Rock Climbing + Moderate = 3 km/hour)
3. Save mapping

**Expected Outcome:**
- ✅ Mapping created successfully
- ✅ Used in distance calculations for workouts
- ✅ Frontend can fetch via `/api/reference-data/`

**Admin URL:**
Navigate to `/admin/ic_marathon_app/sportintensitymapping/`

---

### 6. System Monitoring

#### Test Case 6.1: Check Application Logs
**Objective:** Verify admin can access server logs

**Steps (Heroku):**
```bash
heroku logs --tail -a ciscorunning
```

**Expected Outcome:**
- ✅ Real-time logs displayed
- ✅ Shows request/response info
- ✅ Shows errors and exceptions
- ✅ Shows promotion events

#### Test Case 6.2: Database Backup
**Objective:** Verify admin can backup database

**Steps (Heroku):**
```bash
heroku pg:backups:capture -a ciscorunning
heroku pg:backups:download -a ciscorunning
```

**Expected Outcome:**
- ✅ Backup created successfully
- ✅ Backup downloaded locally
- ✅ Can restore from backup if needed

#### Test Case 6.3: Check Application Status
**Objective:** Verify application health

**Steps (Heroku):**
```bash
heroku ps -a ciscorunning
heroku releases -a ciscorunning
```

**Expected Outcome:**
- ✅ Dyno status shown (web.1: up)
- ✅ Recent releases listed
- ✅ Can identify current version

---

## 🔌 API Testing

### API Test Case 1: Authentication
```bash
# Test Strava OAuth authentication
curl -X POST https://ciscorunning.herokuapp.com/api/auth/strava/ \
  -H "Content-Type: application/json" \
  -d '{"strava_access_token": "test_token"}'
```

**Expected:** 200 OK with `{"token": "...", "user": "username"}`

### API Test Case 2: Create Profile
```bash
curl -X POST https://ciscorunning.herokuapp.com/api/profiles/me/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cec": "testuser",
    "user_goal_km": 42.00,
    "category": "runner"
  }'
```

**Expected:** 201 Created with profile data

### API Test Case 3: Get Profile
```bash
curl -X GET https://ciscorunning.herokuapp.com/api/profiles/me/ \
  -H "Authorization: Token YOUR_TOKEN"
```

**Expected:** 200 OK with full profile including badges

### API Test Case 4: Submit Workout
```bash
curl -X POST https://ciscorunning.herokuapp.com/api/workouts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "distance=5.00" \
  -F "date_time=2024-12-15T08:30:00Z" \
  -F "time=00:30:00" \
  -F "sport=1" \
  -F "intensity=2" \
  -F "photo_evidence=@photo.jpg"
```

**Expected:** 201 Created with workout data + `newly_awarded_badges`

### API Test Case 5: Get Reference Data
```bash
curl -X GET https://ciscorunning.herokuapp.com/api/reference-data/
```

**Expected:** 200 OK with sports, intensities, and mappings

### API Test Case 6: Invalid Token
```bash
curl -X GET https://ciscorunning.herokuapp.com/api/profiles/me/ \
  -H "Authorization: Token invalid_token"
```

**Expected:** 401 Unauthorized

---

## ⚡ Performance Testing

### Performance Test 1: Page Load Time
**Objective:** Verify pages load within acceptable time

**Tool:** Browser DevTools Network tab

**Steps:**
1. Clear cache
2. Navigate to dashboard
3. Measure load time

**Expected:** Page loads < 3 seconds

### Performance Test 2: API Response Time
**Objective:** Verify API responds quickly

**Tool:** `curl` with `-w` flag

```bash
curl -w "@curl-format.txt" -o /dev/null -s \
  -H "Authorization: Token YOUR_TOKEN" \
  https://ciscorunning.herokuapp.com/api/profiles/me/
```

**Expected:** Response time < 500ms

### Performance Test 3: Image Upload
**Objective:** Verify large image uploads work

**Steps:**
1. Upload 5MB image as workout evidence
2. Monitor upload time

**Expected:** Upload completes < 10 seconds

---

## 🔐 Security Testing

### Security Test 1: Unauthorized Access
**Objective:** Verify endpoints require authentication

**Steps:**
```bash
curl -X GET https://ciscorunning.herokuapp.com/api/profiles/me/
```

**Expected:** 401 Unauthorized (no token provided)

### Security Test 2: Cross-User Data Access
**Objective:** Verify users can't access other users' data

**Steps:**
1. User A gets their profile
2. User A tries to access User B's profile using User B's ID

**Expected:** 403 Forbidden or only returns User A's data

### Security Test 3: SQL Injection Prevention
**Objective:** Verify input sanitization

**Steps:**
```bash
curl -X POST https://ciscorunning.herokuapp.com/api/profiles/me/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cec": "test\"; DROP TABLE profiles; --",
    "user_goal_km": 42,
    "category": "runner"
  }'
```

**Expected:** 400 Bad Request (invalid input) or sanitized string

### Security Test 4: XSS Prevention
**Objective:** Verify HTML/JS injection prevented

**Steps:**
1. Submit workout with `<script>alert('XSS')</script>` in notes
2. View workout in admin/frontend

**Expected:** Script tags escaped, not executed

---

## 📋 Test Summary Checklist

### User Testing
- [ ] Strava OAuth authentication works
- [ ] Profile creation and management
- [ ] Solo workout submission (running & freestyle)
- [ ] Partner workout request and confirmation
- [ ] Badge awards trigger correctly
- [ ] Streak tracking accurate
- [ ] Auto-promotion logic works
- [ ] Leaderboards display correctly

### Admin Testing
- [ ] Workout auditing functional
- [ ] User profile management
- [ ] Partner workout status visible
- [ ] Badge administration works
- [ ] Reference data editable
- [ ] System monitoring accessible

### API Testing
- [ ] All endpoints return expected responses
- [ ] Authentication required where needed
- [ ] Error handling appropriate
- [ ] Swagger docs accessible

### Performance & Security
- [ ] Pages load quickly
- [ ] API responds fast
- [ ] Unauthorized access blocked
- [ ] Input sanitization works

---

## 🎯 Regression Testing

Before each release, run through this checklist:

1. ✅ User Registration Flow (Test Cases 1.1-1.2)
2. ✅ Profile Creation & Updates (Test Cases 2.1-2.6)
3. ✅ Solo Workout Submission (Test Cases 3.1-3.5)
4. ✅ Partner Workout Flow (Test Cases 4.1-4.6)
5. ✅ Badge System (Test Cases 5.1-5.5)
6. ✅ Streak Tracking (Test Cases 6.1-6.5)
7. ✅ Auto-Promotion (Test Cases 7.1-7.4)
8. ✅ Leaderboards (Test Cases 8.1-8.3)
9. ✅ Admin Functions (Admin Test Cases 1.1-6.3)
10. ✅ API Endpoints (API Test Cases 1-6)

---

## 📞 Reporting Issues

If you encounter issues during testing:

1. **Document the issue:**
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Screenshots/logs

2. **Contact administrators:**
   - Sari Fernandez (sarifern@cisco.com)
   - Alfredo Prado (apradoca@cisco.com)
   - Email: gpe-reyes-marathon@cisco.com

3. **Include environment details:**
   - Browser/device
   - API endpoint (if API issue)
   - User role (user/admin)
   - Timestamp

---

**Good luck with testing!** 🧪✅

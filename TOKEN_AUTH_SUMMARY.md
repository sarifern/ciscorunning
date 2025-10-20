# Token Authentication Implementation Summary

## 🎯 Overview

All API endpoints now use **token-based authentication**. The authenticated user is automatically extracted from the token, eliminating the need to manually specify user IDs or profile IDs.

## ✅ Changes Made

### 1. Authentication Endpoint (`/api/auth/strava/`)

**Simplified Request:**
```json
{
  "strava_access_token": "your_token"
}
```

**What Changed:**
- ✅ Removed `username` parameter (auto-extracted from Strava)
- ✅ Users matched by Strava ID (more reliable)
- ✅ Auto-handles username conflicts
- ✅ Updates user info on each login

### 2. Workout Endpoints

**Before (Manual):**
```javascript
formData.append('belongs_to', profileId);  // ❌ Required manual input
```

**After (Automatic):**
```javascript
// belongs_to automatically set from token ✅
// Just include the workout data
formData.append('distance', '5.00');
formData.append('date_time', '2024-12-15T08:30:00Z');
// ...
```

**Key Changes:**
- ✅ `belongs_to` is now **read-only** (auto-set from auth token)
- ✅ Added `id` field to workout responses
- ✅ Only see your own workouts in GET requests
- ✅ Can only delete your own workouts
- ✅ Must have profile before creating workouts

### 3. Profile Endpoints

**All Operations Use Token:**
- `GET /api/profiles/me/` - Get your profile
- `POST /api/profiles/me/` - Create your profile  
- `PATCH /api/profiles/me/` - Update your profile
- `DELETE /api/profiles/me/` - Delete your profile

**Key Changes:**
- ✅ Profile automatically associated with authenticated user
- ✅ Can't access other users' profiles
- ✅ Better error messages when profile missing
- ✅ Added `awarded_badges` to response
- ✅ Added `actual_category` to show progression

## 📋 Updated API Endpoints

### Authentication

```http
POST /api/auth/strava/
Content-Type: application/json

{
  "strava_access_token": "abc123..."
}
```

**Response:**
```json
{
  "token": "django_token_here",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "strava_id": "12345678"
  }
}
```

### Profile Management

```http
GET /api/profiles/me/
Authorization: Token your_token
```

**Response:**
```json
{
  "user": "johndoe",
  "cec": "johndoe",
  "category": "runner",
  "actual_category": "Beginner Runner",
  "user_goal_km": "42.00",
  "distance": "25.50",
  "current_streak": 7,
  "longest_streak": 12,
  "workout_days_count": 18,
  "category_changed": false,
  "avatar": "https://...",
  "awarded_badges": [
    {
      "slug": "10K",
      "name": "10K Record Smashed",
      "description": "Congrats! You set a new 10k personal record",
      "awarded_at": "2024-12-18T10:30:00Z"
    }
  ]
}
```

```http
POST /api/profiles/me/
Authorization: Token your_token
Content-Type: application/json

{
  "cec": "johndoe",
  "user_goal_km": "42.00",
  "category": "runner"
}
```

### Workout Management

```http
GET /api/workouts/
Authorization: Token your_token
```

**Response:** Array of your workouts only

```http
POST /api/workouts/
Authorization: Token your_token
Content-Type: multipart/form-data

distance: 5.00
date_time: 2024-12-15T08:30:00Z
time: 00:30:00
sport: 1
intensity: 2
photo_evidence: [file]
```

**Response:**
```json
{
  "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "belongs_to": 1,
  "distance": "5.00",
  "date_time": "2024-12-15T08:30:00Z",
  "time": "00:30:00",
  "sport": 1,
  "intensity": 2,
  "photo_evidence": "https://...",
  "uploaded_at": "2024-12-15T08:30:00Z",
  "edition": 2025,
  "newly_awarded_badges": [...]
}
```

```http
DELETE /api/workouts/{uuid}/
Authorization: Token your_token
```

## 🔐 How Token Authentication Works

### 1. User Authenticates via Strava
```
Frontend → Strava OAuth → Get access_token → Send to /api/auth/strava/
```

### 2. Backend Returns Django Token
```
Backend validates Strava token → Creates/gets User → Returns Django token
```

### 3. Frontend Stores Token
```javascript
localStorage.setItem('auth_token', token);
```

### 4. All Requests Include Token
```javascript
headers: {
  'Authorization': `Token ${token}`
}
```

### 5. Backend Extracts User from Token
```python
user = request.user  # Automatically from token
profile = user.profile  # Get user's profile
```

## 💡 Benefits of Token Authentication

### Security
- ✅ No user IDs exposed in URLs or requests
- ✅ Can't access other users' data
- ✅ Stateless authentication
- ✅ Token can be revoked if compromised

### Developer Experience
- ✅ Simpler API calls (less parameters)
- ✅ No need to track profile IDs
- ✅ Automatic user association
- ✅ Better error messages

### Reliability
- ✅ Can't accidentally send wrong profile ID
- ✅ No authorization bugs
- ✅ Consistent user experience
- ✅ Easier testing

## 🚫 Common Errors & Solutions

### 401 Unauthorized
**Error:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Solution:**
```javascript
// Make sure to include the Authorization header
headers: {
  'Authorization': `Token ${token}`
}
```

### 400 Bad Request - No Profile
**Error:**
```json
{
  "error": "Profile required",
  "detail": "You must create a profile before adding workouts."
}
```

**Solution:**
```javascript
// Create profile first
await fetch('/api/profiles/me/', {
  method: 'POST',
  headers: {
    'Authorization': `Token ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    cec: 'johndoe',
    user_goal_km: '42.00',
    category: 'runner'
  })
});
```

### 403 Forbidden - Not Your Workout
**Error:**
```json
{
  "error": "Permission denied",
  "detail": "You can only delete your own workouts"
}
```

**Solution:** You can only modify/delete your own workouts. The workout belongs to another user.

### 404 Not Found - No Profile
**Error:**
```json
{
  "error": "Profile not found",
  "detail": "You don't have a profile yet."
}
```

**Solution:** Create a profile using `POST /api/profiles/me/`

## 🔧 Frontend Code Examples

### Complete Authentication Flow

```javascript
// 1. Authenticate with Strava
const stravaData = await fetch('https://www.strava.com/oauth/token', {
  method: 'POST',
  body: JSON.stringify({
    client_id: STRAVA_CLIENT_ID,
    client_secret: STRAVA_CLIENT_SECRET,
    code: authCode,
    grant_type: 'authorization_code'
  })
}).then(r => r.json());

// 2. Get Django token
const backendAuth = await fetch('/api/auth/strava/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    strava_access_token: stravaData.access_token
  })
}).then(r => r.json());

// 3. Store token
localStorage.setItem('auth_token', backendAuth.token);

// 4. Check for profile
const profileCheck = await fetch('/api/profiles/me/', {
  headers: { 'Authorization': `Token ${backendAuth.token}` }
});

if (profileCheck.status === 404) {
  // 5. Create profile
  await fetch('/api/profiles/me/', {
    method: 'POST',
    headers: {
      'Authorization': `Token ${backendAuth.token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      cec: 'johndoe',
      user_goal_km: '42.00',
      category: 'runner'
    })
  });
}

// 6. Ready to use API
```

### Create Workout

```javascript
const createWorkout = async (workoutData, photoFile) => {
  const token = localStorage.getItem('auth_token');
  
  const formData = new FormData();
  formData.append('distance', workoutData.distance);
  formData.append('date_time', workoutData.dateTime);
  formData.append('time', workoutData.time);
  formData.append('sport', workoutData.sportId);
  formData.append('intensity', workoutData.intensityId);
  formData.append('photo_evidence', photoFile);
  
  const response = await fetch('/api/workouts/', {
    method: 'POST',
    headers: {
      'Authorization': `Token ${token}`
    },
    body: formData
  });
  
  const result = await response.json();
  
  // Check for newly awarded badges
  if (result.newly_awarded_badges?.length > 0) {
    showBadgeNotification(result.newly_awarded_badges);
  }
  
  return result;
};
```

### Get User's Workouts

```javascript
const getWorkouts = async () => {
  const token = localStorage.getItem('auth_token');
  
  const response = await fetch('/api/workouts/', {
    headers: {
      'Authorization': `Token ${token}`
    }
  });
  
  return response.json();
};
```

### Update Profile

```javascript
const updateGoal = async (newGoal) => {
  const token = localStorage.getItem('auth_token');
  
  const response = await fetch('/api/profiles/me/', {
    method: 'PATCH',
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_goal_km: newGoal
    })
  });
  
  return response.json();
};
```

## 📊 Database Changes

No database migrations required! The changes are in:
- **Serializers** - Made `belongs_to` read-only
- **ViewSets** - Auto-set user from token
- **Permissions** - Already using `IsAuthenticated`

## ✅ Testing Checklist

### Backend Testing
- [x] Token authentication configured
- [x] Workouts filtered by authenticated user
- [x] Profile operations use authenticated user
- [x] Can't access other users' data
- [x] Proper error messages

### Frontend Testing
- [ ] Authentication flow works
- [ ] Profile creation works
- [ ] Workout creation without `belongs_to` works
- [ ] Can view own workouts
- [ ] Can delete own workouts
- [ ] Can't access other users' data
- [ ] Proper error handling

## 🎉 Summary

All endpoints now use **token-based authentication** with the authenticated user automatically extracted from the token. This provides:

- **Simpler API** - Fewer parameters to manage
- **More Secure** - Can't access other users' data
- **Better UX** - Automatic user association
- **Easier Development** - Less boilerplate code

The `belongs_to` field for workouts is now **read-only** and automatically set from your authentication token. Just include your token in the Authorization header and the backend handles the rest!

# Frontend Developer Guide - Cisco Running API

## 🎯 Quick Reference

### Base URLs
- **Development**: `http://localhost:8000/api/`
- **Production**: `https://ciscorunning.herokuapp.com/api/`

### Authentication
Token-based authentication using Strava OAuth2 flow.

## 🔐 Authentication Flow

### Complete Strava OAuth2 Flow

**Step 1: Frontend redirects user to Strava for authorization**

```javascript
const STRAVA_CLIENT_ID = 'your_strava_client_id';
const REDIRECT_URI = 'https://yourfrontend.com/auth/callback';
const STRAVA_AUTH_URL = `https://www.strava.com/oauth/authorize?client_id=${STRAVA_CLIENT_ID}&response_type=code&redirect_uri=${REDIRECT_URI}&approval_prompt=force&scope=activity:read_all`;

// Redirect user to Strava
window.location.href = STRAVA_AUTH_URL;
```

**Step 2: Strava redirects back with authorization code**

Strava will redirect to: `https://yourfrontend.com/auth/callback?code=AUTHORIZATION_CODE`

**Step 3: Exchange authorization code for access token**

```javascript
// In your callback handler
const exchangeTokens = async (code) => {
  const response = await fetch('https://www.strava.com/oauth/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      client_id: 'your_strava_client_id',
      client_secret: 'your_strava_client_secret',
      code: code,
      grant_type: 'authorization_code'
    })
  });
  
  const data = await response.json();
  // data contains: access_token, refresh_token, athlete info
  return data;
};
```

**Step 4: Authenticate with backend API**

```javascript
const authenticateBackend = async (stravaAccessToken) => {
  const response = await fetch('http://localhost:8000/api/auth/strava/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      strava_access_token: stravaAccessToken
    })
  });
  
  const data = await response.json();
  // data contains: token (Django token), user info (username from Strava)
  localStorage.setItem('authToken', data.token);
  return data;
};
```

**Step 5: Create user profile (if new user)**

```javascript
const createProfile = async (token, profileData) => {
  const response = await fetch('http://localhost:8000/api/profiles/me/', {
    method: 'POST',
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      cec: profileData.cec,
      user_goal_km: profileData.goal,
      category: profileData.category  // 'runner' or 'freestyler'
    })
  });
  
  return response.json();
};
```

### Complete Frontend Example

```javascript
// auth.js - Complete authentication handler

const API_BASE_URL = 'http://localhost:8000';
const STRAVA_CLIENT_ID = 'your_client_id';
const STRAVA_CLIENT_SECRET = 'your_client_secret';
const REDIRECT_URI = 'http://yourfrontend.com/auth/callback';

// 1. Initiate Strava OAuth
export const initiateStravaAuth = () => {
  const authUrl = `https://www.strava.com/oauth/authorize?client_id=${STRAVA_CLIENT_ID}&response_type=code&redirect_uri=${REDIRECT_URI}&approval_prompt=force&scope=activity:read_all`;
  window.location.href = authUrl;
};

// 2. Handle OAuth callback
export const handleAuthCallback = async (code) => {
  try {
    // Exchange code for Strava tokens
    const stravaResponse = await fetch('https://www.strava.com/oauth/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        client_id: STRAVA_CLIENT_ID,
        client_secret: STRAVA_CLIENT_SECRET,
        code: code,
        grant_type: 'authorization_code'
      })
    });
    
    const stravaData = await stravaResponse.json();
    const { access_token, athlete } = stravaData;
    
    // Authenticate with backend
    const backendResponse = await fetch(`${API_BASE_URL}/api/auth/strava/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        strava_access_token: access_token
      })
    });
    
    const backendData = await backendResponse.json();
    
    // Store token
    localStorage.setItem('authToken', backendData.token);
    localStorage.setItem('userId', backendData.user.id);
    localStorage.setItem('stravaId', backendData.user.strava_id);
    
    // Check if user has a profile
    const profileResponse = await fetch(`${API_BASE_URL}/api/profiles/me/`, {
      headers: {
        'Authorization': `Token ${backendData.token}`
      }
    });
    
    if (profileResponse.status === 404) {
      // No profile exists, redirect to profile creation
      return { needsProfile: true, token: backendData.token };
    }
    
    const profile = await profileResponse.json();
    return { needsProfile: false, token: backendData.token, profile };
    
  } catch (error) {
    console.error('Authentication error:', error);
    throw error;
  }
};

// 3. Create profile for new users
export const createUserProfile = async (profileData) => {
  const token = localStorage.getItem('authToken');
  
  const response = await fetch(`${API_BASE_URL}/api/profiles/me/`, {
    method: 'POST',
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      cec: profileData.cec,
      user_goal_km: profileData.goal,
      category: profileData.category  // 'runner' or 'freestyler'
    })
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error);
  }
  
  return response.json();
};

// 4. Logout
export const logout = () => {
  localStorage.removeItem('authToken');
  localStorage.removeItem('userId');
  localStorage.removeItem('stravaId');
  window.location.href = '/';
};
```

### React Component Example

```jsx
// AuthCallback.jsx
import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { handleAuthCallback } from './auth';

function AuthCallback() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const code = searchParams.get('code');
    
    if (code) {
      handleAuthCallback(code)
        .then(result => {
          if (result.needsProfile) {
            navigate('/create-profile');
          } else {
            navigate('/dashboard');
          }
        })
        .catch(err => {
          setError(err.message);
        });
    }
  }, [searchParams, navigate]);
  
  if (error) {
    return <div>Error: {error}</div>;
  }
  
  return <div>Authenticating with Strava...</div>;
}

export default AuthCallback;
```

```jsx
// CreateProfile.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createUserProfile } from './auth';

function CreateProfile() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    cec: '',
    goal: '42.00',
    category: 'runner'
  });
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createUserProfile(formData);
      navigate('/dashboard');
    } catch (error) {
      console.error('Profile creation error:', error);
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={formData.cec}
        onChange={e => setFormData({...formData, cec: e.target.value})}
        placeholder="CEC ID"
        required
      />
      <input
        type="number"
        value={formData.goal}
        onChange={e => setFormData({...formData, goal: e.target.value})}
        placeholder="Goal (km)"
        required
      />
      <select
        value={formData.category}
        onChange={e => setFormData({...formData, category: e.target.value})}
      >
        <option value="runner">Runner</option>
        <option value="freestyler">Freestyler</option>
      </select>
      <button type="submit">Create Profile</button>
    </form>
  );
}

export default CreateProfile;
```

## 📍 API Endpoints Summary

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/auth/strava/` | POST | No | Exchange Strava token for Django token |
| `/api/profiles/me/` | GET | Yes | Get your profile |
| `/api/profiles/me/` | POST | Yes | Create profile |
| `/api/profiles/me/` | PATCH | Yes | Update profile |
| `/api/profiles/me/` | DELETE | Yes | Delete profile |
| `/api/workouts/` | GET | Yes | List your workouts |
| `/api/workouts/` | POST | Yes | Create workout |
| `/api/workouts/{id}/` | GET | Yes | Get specific workout |
| `/api/workouts/{id}/` | PATCH | Yes | Update workout |
| `/api/workouts/{id}/` | DELETE | Yes | Delete workout |
| `/api/docs/` | GET | No | Swagger UI docs |

## � Authentication Endpoint Details

### POST /api/auth/strava/
Exchange a Strava access token for a Django REST Framework authentication token.

**Request:**
```json
{
  "strava_access_token": "abc123def456..."
}
```

**Response (200 OK):**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "strava_id": "12345678"
  },
  "created": false
}
```

**What happens behind the scenes:**
1. Backend validates the Strava token by calling Strava's API
2. Extracts username and user info from Strava athlete data
3. Creates a Django User if it doesn't exist (matched by Strava ID)
4. Creates/links a SocialAccount with Strava data
5. Returns a Django token for subsequent API requests

**Error Responses:**

**400 Bad Request** - Missing token
```json
{
  "error": "strava_access_token is required"
}
```

**401 Unauthorized** - Invalid Strava token
```json
{
  "error": "Invalid Strava access token",
  "detail": "Token validation failed with Strava API"
}
```

**503 Service Unavailable** - Strava API error
```json
{
  "error": "Failed to validate Strava token",
  "detail": "Connection timeout"
}
```

## �🔐 Using Authentication Tokens

All authenticated requests should include the token in the Authorization header:

```http
GET /api/profiles/me/
Authorization: Token YOUR_TOKEN_HERE
```

**JavaScript Example:**
```javascript
const apiRequest = async (endpoint, options = {}) => {
  const token = localStorage.getItem('authToken');
  
  return fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    }
  });
};

// Usage
const profile = await apiRequest('/api/profiles/me/').then(r => r.json());
```

## 👤 Profile Endpoints

### GET /api/profiles/me/
Returns complete profile with all badges and metrics.

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

### POST /api/profiles/me/
Create a new profile. User must not have a profile.

**Request:**
```json
{
  "cec": "johndoe",
  "user_goal_km": "42.00",
  "category": "runner"
}
```

**Notes:**
- `category`: Must be "runner" or "freestyler"
- Backend auto-assigns to "beginnerrunner" or "beginnerfreestyler"
- Auto-promotion happens based on performance

### PATCH /api/profiles/me/
Update profile fields.

**Request:**
```json
{
  "user_goal_km": "84.00"
}
```

**Notes:**
- Can update `user_goal_km` unlimited times
- Can change `category` only once (runner ↔ freestyler)
- Cannot manually change beginner status

## Profiles Endpoints

### Get All Profiles (Leaderboard)
**GET** `/api/profiles/`

Returns all profiles grouped by category and sorted by distance (highest to lowest within each category). This is perfect for displaying leaderboards.

**Authentication:** Required (Bearer token)

**Response:**
```json
{
  "beginnerrunner": [
    {
      "id": 1,
      "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe"
      },
      "cec": "12345",
      "distance": 125.50,
      "category": "beginnerrunner",
      "avatar": "https://example.com/avatar.jpg",
      "user_goal": true,
      "user_goal_km": 42.00,
      "total_workouts": 25,
      "current_streak": 5,
      "longest_streak": 10,
      "first_workout_date": "2025-01-15",
      "last_workout_date": "2025-10-20"
    },
    {
      "id": 2,
      "user": {...},
      "distance": 98.75,
      ...
    }
  ],
  "runner": [
    {
      "id": 3,
      "distance": 250.00,
      ...
    }
  ],
  "freestyler": [...],
  "beginnerfreestyler": [...]
}
```

**Categories:**
- `beginnerrunner` - Beginner Runner
- `runner` - Runner
- `freestyler` - Freestyler
- `beginnerfreestyler` - Beginner Freestyler

**Use Case:**
This endpoint is ideal for creating leaderboards. Each category is sorted by distance in descending order, so the first profile in each array is the leader for that category.

**Example Usage:**
```javascript
const response = await fetch('http://127.0.0.1:8000/api/profiles/', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
const leaderboard = await response.json();

// Display beginner runner leaderboard
leaderboard.beginnerrunner.forEach((profile, index) => {
  console.log(`${index + 1}. ${profile.user.first_name} ${profile.user.last_name} - ${profile.distance} km`);
});
```
## 🏃 Workout Endpoints

### GET /api/workouts/
List all your workouts (newest first).

**Response:**
```json
[
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
    "edition": 2025
  }
]
```

### POST /api/workouts/
Create a new workout. Returns workout + newly awarded badges.

**Authentication Required:** Yes (Token in Authorization header)

**Request (FormData):**
```javascript
const formData = new FormData();
// belongs_to is automatically set from authenticated user - DO NOT include it
formData.append('distance', '5.00');
formData.append('date_time', '2024-12-15T08:30:00Z');
formData.append('time', '00:30:00');
formData.append('sport', 1);
formData.append('intensity', 2);
formData.append('photo_evidence', fileObject);

// Send with authorization header
fetch('/api/workouts/', {
  method: 'POST',
  headers: {
    'Authorization': `Token ${yourToken}`
  },
  body: formData
});
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
  "newly_awarded_badges": [
    {
      "slug": "7day-streak",
      "name": "Week Warrior",
      "description": "Amazing! You completed 7 consecutive days of workouts!",
      "awarded_at": "2024-12-15T08:30:15Z"
    }
  ]
}
```

**Important Notes:**
- The `belongs_to` field is **read-only** and automatically set from your authentication token
- The `uuid` field is the unique identifier for each workout (auto-generated)
- The `uploaded_at` and `edition` fields are automatically set
- You must have a profile before creating workouts
- If you try to create a workout without a profile, you'll get a 400 error

## 🏆 Badge System

### Badge Slugs Reference

**Distance Badges:**
- `10K` - 10km total
- `21K` - 21km total (half marathon)
- `42K` - 42km total (full marathon)
- `84K` - 84km total (2 marathons)
- `126K` - 126km total (3 marathons)
- `168K` - 168km total (4 marathons)
- `ownK` - Personal goal achieved

**Streak Badges:**
- `7day-streak` - 7 consecutive workout days
- `14day-streak` - 14 consecutive workout days
- `21day-streak` - 21 consecutive workout days

### Badge Notification Flow

1. User submits workout via POST /api/workouts/
2. Backend calculates new distance and streaks
3. Backend checks badge criteria
4. Response includes `newly_awarded_badges` array
5. Frontend displays celebration/notification

## 📊 Sport IDs

| ID | Sport Type | Conversion |
|----|------------|------------|
| 1 | Running | 1:1 |
| 2 | Cycling | TBD |
| 3 | Swimming | TBD |
| 4 | Hiking | TBD |
| ... | ... | ... |

*(Check Django admin for complete sport mappings)*

## 🚦 Category System

### User Selection (Wizard)
- `runner` - Traditional running
- `freestyler` - Various sports activities

### Actual Categories (Backend)
- `beginnerrunner` - Auto-assigned to new runners
- `runner` - Auto-promoted experienced runners
- `beginnerfreestyler` - Auto-assigned to new freestylers
- `freestyler` - Auto-promoted experienced freestylers

### Auto-Promotion Triggers
User is promoted when **any** of these conditions are met:

1. **High Distance + Consistency**: 84km + 10 workout days
2. **Performance Detected**: 5 workouts averaging 7km+
3. **Super Consistent**: 42km + 15 workout days

## ⚠️ Important Notes

### Field Constraints
- `distance`: Auto-calculated (read-only)
- `current_streak`: Auto-calculated (read-only)
- `longest_streak`: Auto-calculated (read-only)
- `workout_days_count`: Auto-calculated (read-only)
- `category_changed`: Auto-set (read-only)
- `actual_category`: Computed field (not in database)

### Category Change Restriction
Users can switch between runner ↔ freestyler **only once**.

**Example:**
```javascript
// First change: OK
PATCH /api/profiles/me/ { "category": "freestyler" }

// Second change: ERROR
PATCH /api/profiles/me/ { "category": "runner" }
// Response: 400 Bad Request
// "You have already changed your category once"
```

### Streak Calculation
- **Current Streak**: Only valid if last workout was today or yesterday
- **Longest Streak**: Never decreases, only increases when broken record
- **Unique Days**: Multiple workouts same day = 1 day

## 🔍 Error Handling

### Common Errors

**401 Unauthorized**
```json
{
  "detail": "Authentication credentials were not provided."
}
```
*Solution: Include Authorization header with valid token*

**400 Bad Request - Profile Already Exists**
```json
{
  "non_field_errors": ["You already have a profile. Use PUT/PATCH to update it instead of POST."]
}
```
*Solution: Use PATCH instead of POST*

**400 Bad Request - Category Already Changed**
```json
{
  "category": ["You have already changed your category once. You cannot switch between runner and freestyler again."]
}
```
*Solution: Cannot change category track more than once*

## 💡 Frontend Tips

### Token Management
```javascript
// Store token securely
localStorage.setItem('authToken', token);

// Create axios instance with auth
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://ciscorunning.herokuapp.com/api/',
  headers: {
    'Authorization': `Token ${localStorage.getItem('authToken')}`
  }
});

// Use in components
const profile = await api.get('/profiles/me/');
```

### Real-time Updates
```javascript
// After workout submission, update local state
const submitWorkout = async (data) => {
  const result = await api.post('/workouts/', data);
  
  // Update profile to reflect new distance/streaks
  const updatedProfile = await api.get('/profiles/me/');
  
  // Show badge notifications
  if (result.data.newly_awarded_badges?.length > 0) {
    showBadgeModal(result.data.newly_awarded_badges);
  }
  
  return { workout: result.data, profile: updatedProfile.data };
};
```

### Badge Progress Tracking
```javascript
const calculateBadgeProgress = (profile) => {
  const progress = {
    distance: [],
    streak: []
  };
  
  // Distance progress
  const milestones = [10, 21, 42, 84, 126, 168];
  milestones.forEach(km => {
    const earned = profile.awarded_badges.some(b => b.slug === `${km}K`);
    const percentage = (profile.distance / km) * 100;
    progress.distance.push({
      target: km,
      earned,
      percentage: Math.min(percentage, 100),
      remaining: Math.max(km - profile.distance, 0)
    });
  });
  
  // Streak progress
  const streakMilestones = [7, 14, 21];
  streakMilestones.forEach(days => {
    const earned = profile.awarded_badges.some(b => b.slug === `${days}day-streak`);
    const percentage = (profile.longest_streak / days) * 100;
    progress.streak.push({
      target: days,
      earned,
      percentage: Math.min(percentage, 100),
      remaining: Math.max(days - profile.longest_streak, 0)
    });
  });
  
  return progress;
};
```

## 📚 Additional Resources

- **Swagger UI**: https://ciscorunning.herokuapp.com/api/docs/
- **ReDoc**: https://ciscorunning.herokuapp.com/api/redoc/
- **OpenAPI Schema**: https://ciscorunning.herokuapp.com/api/schema/

## 🐛 Support

For API issues or questions:
- Email: gpe-reyes-marathon@cisco.com
- Admin: Sari Fernandez (sarifern@cisco.com)
- Admin: Alfredo Prado (apradoca@cisco.com)

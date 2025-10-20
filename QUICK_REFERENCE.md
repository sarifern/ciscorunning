# Quick Reference Card - Strava OAuth Integration

## 🎯 For Frontend Developers

### Environment Variables Needed
```env
VITE_STRAVA_CLIENT_ID=your_client_id
VITE_STRAVA_CLIENT_SECRET=your_client_secret  
VITE_REDIRECT_URI=http://localhost:3000/auth/callback
VITE_API_BASE_URL=http://localhost:8000
```

### Step 1: Login Button
```javascript
const loginUrl = `https://www.strava.com/oauth/authorize?client_id=${STRAVA_CLIENT_ID}&response_type=code&redirect_uri=${REDIRECT_URI}&scope=activity:read_all`;
window.location.href = loginUrl;
```

### Step 2: Handle Callback (Get token from Strava)
```javascript
const response = await fetch('https://www.strava.com/oauth/token', {
  method: 'POST',
  body: JSON.stringify({
    client_id: STRAVA_CLIENT_ID,
    client_secret: STRAVA_CLIENT_SECRET,
    code: authorizationCode,
    grant_type: 'authorization_code'
  })
});
const { access_token, athlete } = await response.json();
```

### Step 3: Authenticate with Backend
```javascript
const response = await fetch('http://localhost:8000/api/auth/strava/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    strava_access_token: access_token
  })
});
const { token, user } = await response.json();
// user.username comes from Strava automatically
localStorage.setItem('auth_token', token);
```

### Step 4: Check for Profile
```javascript
const response = await fetch('http://localhost:8000/api/profiles/me/', {
  headers: { 'Authorization': `Token ${token}` }
});

if (response.status === 404) {
  // Redirect to profile creation
} else {
  // Redirect to dashboard
}
```

### Step 5: Create Profile (if needed)
```javascript
const response = await fetch('http://localhost:8000/api/profiles/me/', {
  method: 'POST',
  headers: {
    'Authorization': `Token ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    cec: 'johndoe',
    user_goal_km: '42.00',
    category: 'runner'  // or 'freestyler'
  })
});
```

### All Subsequent Requests
```javascript
// Get workouts
const response = await fetch('http://localhost:8000/api/workouts/', {
  headers: { 'Authorization': `Token ${token}` }
});

// Create workout (FormData for file upload)
const formData = new FormData();
formData.append('distance', '5.00');
formData.append('date_time', '2024-12-15T08:30:00Z');
formData.append('time', '00:30:00');
formData.append('sport', 1);
formData.append('intensity', 2);
formData.append('photo_evidence', fileObject);

const createResponse = await fetch('http://localhost:8000/api/workouts/', {
  method: 'POST',
  headers: { 'Authorization': `Token ${token}` },
  body: formData
});
```

**Note:** `belongs_to` is automatically set from your auth token - don't include it!

## 🔧 For Backend Developers

### Endpoint Available
```
POST /api/auth/strava/
```

### Test with cURL
```bash
curl -X POST http://localhost:8000/api/auth/strava/ \
  -H "Content-Type: application/json" \
  -d '{
    "strava_access_token": "your_strava_token"
  }'
```

### Required Migrations
```bash
python manage.py migrate
```

### Update CORS (if needed)
In `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://yourfrontend.com",
]
```

### View API Docs
```
http://localhost:8000/api/docs/
```

## 📋 API Endpoints Quick Reference

| Endpoint | Method | Auth | Body |
|----------|--------|------|------|
| `/api/auth/strava/` | POST | No | `{strava_access_token}` |
| `/api/profiles/me/` | GET | Yes | - |
| `/api/profiles/me/` | POST | Yes | `{cec, user_goal_km, category}` |
| `/api/profiles/me/` | PATCH | Yes | `{user_goal_km}` |
| `/api/workouts/` | GET | Yes | - |
| `/api/workouts/` | POST | Yes | FormData with workout details |
| `/api/workouts/{id}/` | DELETE | Yes | - |

## 🔑 Authentication Header Format
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```
**Note:** "Token" not "Bearer"

## 🐛 Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| CORS error | Frontend origin not allowed | Add to CORS_ALLOWED_ORIGINS |
| 401 Unauthorized | Missing/invalid token | Check Authorization header |
| 400 Bad Request | Invalid Strava token | Get fresh token from OAuth |
| 404 Not Found | Profile doesn't exist | Create with POST |

## 📚 Documentation Files

- **IMPLEMENTATION_SUMMARY.md** - Complete overview
- **FRONTEND_AUTH_GUIDE.md** - Full frontend code examples
- **AUTHENTICATION_FLOW_DIAGRAM.md** - Visual flow
- **SETUP_GUIDE.md** - Setup instructions
- **API_FRONTEND_GUIDE.md** - API reference

## 🎉 Quick Start

1. Get Strava credentials from https://www.strava.com/settings/api
2. Set environment variables
3. Implement login flow (see FRONTEND_AUTH_GUIDE.md)
4. Test authentication
5. Build your app!

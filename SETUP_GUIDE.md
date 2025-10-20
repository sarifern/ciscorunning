# Quick Setup Guide - Strava OAuth Integration

## ✅ What's Already Done (Backend)

Your backend already has everything configured! Here's what exists:

### 1. Authentication Endpoint
- **URL**: `/api/auth/strava/`
- **File**: `ic_marathon_app/auth_views.py`
- **Status**: ✅ Implemented and registered in URLs

### 2. Django Settings
- **DRF**: ✅ Configured with Token Authentication
- **Allauth**: ✅ Installed with Strava provider
- **CORS**: ✅ Configured (update for your frontend domain)

### 3. Models
- ✅ User model (Django default)
- ✅ SocialAccount model (django-allauth)
- ✅ Token model (DRF authtoken)
- ✅ Profile model (your custom model)

## 🚀 What You Need to Do

### Backend Setup (5 minutes)

1. **Update CORS settings** in `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",      # Your frontend dev server
    "http://127.0.0.1:3000",
    "https://yourfrontend.com",    # Your production frontend
]
```

2. **Run migrations** (if not done):
```bash
python manage.py migrate
```

3. **Test the endpoint** (optional):
```bash
python manage.py runserver
```

### Frontend Setup

1. **Get Strava API Credentials**
   - Go to https://www.strava.com/settings/api
   - Create application or use existing
   - Save Client ID and Client Secret

2. **Set environment variables**
```env
VITE_STRAVA_CLIENT_ID=your_client_id_here
VITE_STRAVA_CLIENT_SECRET=your_client_secret_here
VITE_REDIRECT_URI=http://localhost:3000/auth/callback
VITE_API_BASE_URL=http://localhost:8000
```

3. **Implement the flow** (see FRONTEND_AUTH_GUIDE.md)
   - Login page with "Connect with Strava" button
   - Auth callback handler at `/auth/callback`
   - Profile creation page for new users
   - Protected routes for authenticated pages

## 📋 API Endpoint Reference

### POST /api/auth/strava/
Exchange Strava access token for Django token.

**Request:**
```json
{
  "strava_access_token": "your_strava_access_token"
}
```

**Response:**
```json
{
  "token": "django_rest_framework_token",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "strava_id": "12345678"
  },
  "created": true
}
```

**Note:** Username is automatically extracted from Strava athlete data.

### GET /api/profiles/me/
Get current user's profile (requires token).

**Headers:**
```
Authorization: Token your_django_token
```

### POST /api/profiles/me/
Create profile for new users (requires token).

**Request:**
```json
{
  "cec": "johndoe",
  "user_goal_km": "42.00",
  "category": "runner"
}
```

## 🔄 Complete Authentication Flow

```
1. User clicks "Login with Strava"
   ↓
2. Redirect to: https://www.strava.com/oauth/authorize?client_id=...
   ↓
3. User authorizes, Strava redirects to: yourfrontend.com/auth/callback?code=...
   ↓
4. Frontend exchanges code for Strava token:
   POST https://www.strava.com/oauth/token
   ↓
5. Frontend sends Strava token to backend:
   POST http://localhost:8000/api/auth/strava/
   {
     "strava_access_token": "..."
   }
   ↓
6. Backend:
   - Validates Strava token
   - Extracts username from Strava athlete data
   - Creates/retrieves User (matched by Strava ID)
   - Creates/links SocialAccount
   - Returns Django token
   ↓
7. Frontend stores Django token
   ↓
8. Frontend checks for profile:
   GET http://localhost:8000/api/profiles/me/
   ↓
9. If no profile exists:
   - Show profile creation form
   - POST http://localhost:8000/api/profiles/me/
   ↓
10. Redirect to dashboard
```

## 🧪 Testing Steps

### Test Backend

1. Start server:
```bash
python manage.py runserver
```

2. Visit API docs:
```
http://localhost:8000/api/docs/
```

3. Test auth endpoint (requires real Strava token):
```bash
# First, get a Strava token manually from Strava OAuth playground
# Then test:
curl -X POST http://localhost:8000/api/auth/strava/ \
  -H "Content-Type: application/json" \
  -d '{
    "strava_access_token": "your_real_strava_token"
  }'
```

### Test Frontend Integration

1. Implement login page
2. Click "Connect with Strava"
3. Authorize on Strava
4. Should redirect to `/auth/callback?code=...`
5. Should auto-authenticate with backend
6. Should redirect to profile creation or dashboard

## 📝 Key Files Created/Updated

### Backend
- ✅ `ic_marathon_site/urls.py` - Added auth endpoint route
- ✅ `ic_marathon_site/settings.py` - Added DRF config
- ✅ `ic_marathon_app/auth_views.py` - Already existed

### Documentation
- ✅ `FRONTEND_AUTH_GUIDE.md` - Complete frontend implementation guide
- ✅ `API_FRONTEND_GUIDE.md` - Updated with auth flow

## 🎯 Next Steps

1. **Backend**: Update CORS settings for your frontend domain
2. **Frontend**: Implement the auth flow using the examples in `FRONTEND_AUTH_GUIDE.md`
3. **Test**: Complete end-to-end authentication test
4. **Deploy**: Update production environment variables

## 💡 Tips

- The backend is production-ready for this authentication flow
- Store Strava tokens separately from Django tokens
- Implement Strava token refresh (tokens expire after 6 hours)
- Handle profile creation gracefully for new users
- Use the API docs at `/api/docs/` to explore all endpoints

## 🆘 Troubleshooting

**Issue**: CORS errors
**Fix**: Add your frontend URL to `CORS_ALLOWED_ORIGINS` in settings.py

**Issue**: 401 Unauthorized
**Fix**: Check Authorization header format: `Token your_token` (not `Bearer`)

**Issue**: Profile already exists error
**Fix**: Check if profile exists with GET before creating with POST

**Issue**: Strava token invalid
**Fix**: Ensure you're getting a fresh token from Strava OAuth flow

## 📚 Read More

- Complete frontend implementation: `FRONTEND_AUTH_GUIDE.md`
- API reference: `API_FRONTEND_GUIDE.md`
- Strava docs: https://developers.strava.com/docs/authentication/

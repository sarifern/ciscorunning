# Summary: Strava OAuth2 + Backend API Integration

## 🎉 What I've Done

I've set up your Django backend to work seamlessly with Strava OAuth2 authentication from your frontend. Here's everything that's been configured:

## ✅ Backend Changes

### 1. Updated URLs (`ic_marathon_site/urls.py`)
- Added authentication endpoint route: `/api/auth/strava/`
- Imported the `auth_views` module
- Endpoint is now accessible and documented in Swagger

### 2. Updated Settings (All 3 settings files)
Added to `settings.py`, `local_settings.py`, and `render_settings.py`:
- `rest_framework` - Django REST Framework
- `rest_framework.authtoken` - Token authentication
- `drf_spectacular` - API documentation
- REST_FRAMEWORK configuration for Token-based auth
- Swagger/OpenAPI settings

### 3. Created Documentation Files

**SETUP_GUIDE.md**
- Quick reference for backend setup
- Testing instructions
- Common troubleshooting

**FRONTEND_AUTH_GUIDE.md**
- Complete frontend implementation guide
- React/JavaScript code examples
- Step-by-step OAuth flow
- Error handling examples
- Protected routes setup

**AUTHENTICATION_FLOW_DIAGRAM.md**
- Visual flow diagram
- Step-by-step authentication process
- Database entities created
- Request/response examples

**API_FRONTEND_GUIDE.md** (Updated)
- Added complete Strava OAuth2 flow section
- Authentication endpoint documentation
- JavaScript/React examples
- Error responses documented

## 🔄 How It Works

### The Complete Flow

1. **Frontend**: User clicks "Login with Strava"
2. **Strava**: User authorizes your app
3. **Frontend**: Receives authorization code
4. **Frontend**: Exchanges code for Strava access token
5. **Frontend**: Sends Strava token to your backend (`POST /api/auth/strava/`)
6. **Backend**: Validates token with Strava API
7. **Backend**: Creates Django User + SocialAccount
8. **Backend**: Returns Django token
9. **Frontend**: Stores Django token
10. **Frontend**: Checks if Profile exists (`GET /api/profiles/me/`)
11. **Frontend**: Creates profile if needed (`POST /api/profiles/me/`)
12. **Frontend**: Redirects to dashboard

### What Gets Created

When a user authenticates:
1. **Django User** - Standard Django user model
2. **SocialAccount** - Links user to Strava (via django-allauth)
3. **Token** - Django REST Framework authentication token
4. **Profile** - Your custom profile (created by user after auth)

## 📍 API Endpoints

### Authentication
```
POST /api/auth/strava/
```
Request:
```json
{
  "strava_access_token": "your_strava_token"
}
```

Response:
```json
{
  "token": "django_token_here",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "strava_id": "12345678"
  },
  "created": true
}
```

**Note:** Username is automatically extracted from Strava athlete data.

### Profile Management
```
GET    /api/profiles/me/     - Get profile
POST   /api/profiles/me/     - Create profile (new users)
PATCH  /api/profiles/me/     - Update profile
```

### Workouts
```
GET    /api/workouts/        - List workouts
POST   /api/workouts/        - Create workout
GET    /api/workouts/{id}/   - Get workout
PATCH  /api/workouts/{id}/   - Update workout
DELETE /api/workouts/{id}/   - Delete workout
```

All authenticated endpoints require:
```
Authorization: Token your_django_token
```

## 🚀 Next Steps for You

### 1. Backend Setup (5 minutes)

Run migrations if you haven't:
```bash
python manage.py migrate
```

Update CORS for your frontend domain in `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://yourfrontend.com",
]
```

### 2. Get Strava Credentials

1. Go to https://www.strava.com/settings/api
2. Create/view your application
3. Get Client ID and Client Secret
4. Set Authorization Callback Domain

### 3. Frontend Implementation

Follow the complete guide in `FRONTEND_AUTH_GUIDE.md`:

**Key files to create:**
- `Login.jsx` - Login page with Strava button
- `AuthCallback.jsx` - Handle OAuth callback
- `CreateProfile.jsx` - Profile creation for new users
- `services/api.js` - API service layer
- `ProtectedRoute.jsx` - Route protection

**Environment variables:**
```env
VITE_STRAVA_CLIENT_ID=your_client_id
VITE_STRAVA_CLIENT_SECRET=your_client_secret
VITE_REDIRECT_URI=http://localhost:3000/auth/callback
VITE_API_BASE_URL=http://localhost:8000
```

### 4. Test the Integration

1. Start backend: `python manage.py runserver`
2. Start frontend: `npm run dev`
3. Click "Login with Strava"
4. Authorize on Strava
5. Should redirect back and authenticate
6. Create profile
7. Access dashboard

## 📚 Documentation Files

- **`SETUP_GUIDE.md`** - Quick setup reference
- **`FRONTEND_AUTH_GUIDE.md`** - Complete frontend guide with code
- **`AUTHENTICATION_FLOW_DIAGRAM.md`** - Visual flow diagram
- **`API_FRONTEND_GUIDE.md`** - API reference for frontend devs

## 🔧 Backend Code Structure

```
ic_marathon_app/
  auth_views.py               # ✅ Authentication endpoint
  models.py                   # ✅ Profile model with ViewSet
  
ic_marathon_site/
  urls.py                     # ✅ Routes including /api/auth/strava/
  settings.py                 # ✅ DRF + Token auth configured
  local_settings.py           # ✅ DRF configured for local dev
  render_settings.py          # ✅ DRF configured for production
```

## 🎯 Key Features

✅ **Strava OAuth2** - Complete flow implemented
✅ **Token Authentication** - Secure API access
✅ **User Management** - Automatic user creation
✅ **Social Account Linking** - Strava accounts linked to users
✅ **Profile System** - Custom profiles with goals and badges
✅ **API Documentation** - Swagger UI at `/api/docs/`
✅ **CORS Configured** - Ready for frontend integration

## 💡 Important Notes

### Authentication
- Backend validates Strava tokens by calling Strava API
- Users are created automatically on first login
- SocialAccount links Django user to Strava
- Django tokens don't expire (unlike Strava tokens)

### Profile Creation
- Check if profile exists before creating
- Use GET first, then POST if 404
- Only POST once - use PATCH for updates
- Category can only be changed once

### Token Management
- Store Django token in localStorage
- Include in all API requests: `Authorization: Token xxx`
- Strava tokens expire after 6 hours (implement refresh)
- Django tokens persist until manually deleted

## 🐛 Troubleshooting

**CORS Errors**
→ Add frontend URL to `CORS_ALLOWED_ORIGINS`

**401 Unauthorized**
→ Check Authorization header: `Token xxx` (not `Bearer`)

**Invalid Strava Token**
→ Ensure fresh token from OAuth flow

**Profile Already Exists**
→ Use GET to check before POST

## 🎓 Understanding the Stack

**Django Backend:**
- Django 2.2+
- Django REST Framework (DRF)
- django-allauth (Social auth)
- drf-spectacular (API docs)

**Authentication Flow:**
- Strava OAuth2 → Authorization code
- Exchange for Strava access token
- Validate with backend
- Receive Django token
- Use for all API calls

**Database Models:**
- `User` (Django built-in)
- `SocialAccount` (django-allauth)
- `Token` (DRF authtoken)
- `Profile` (Your custom model)

## ✨ What Makes This Special

1. **Seamless Integration** - Frontend handles Strava OAuth, backend validates
2. **Secure** - Token validation against Strava API
3. **Automatic User Creation** - No manual user management
4. **Social Account Linking** - Full Strava profile data stored
5. **Token-based API** - Stateless authentication
6. **Well Documented** - Swagger UI + markdown guides

## 🎉 You're Ready!

Your backend is fully configured and ready to accept Strava OAuth authentication from your frontend. Follow the `FRONTEND_AUTH_GUIDE.md` for complete frontend implementation with React/JavaScript examples.

**Questions?** Check the documentation files or test the endpoints at `/api/docs/`

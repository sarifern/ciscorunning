# Implementation Checklist

## ✅ Backend Setup Checklist

### Prerequisites
- [ ] Python and Django installed
- [ ] PostgreSQL/SQLite database configured
- [ ] Virtual environment activated

### Configuration
- [x] Django REST Framework installed (`rest_framework`)
- [x] Auth token package installed (`rest_framework.authtoken`)
- [x] Django-allauth installed with Strava provider
- [x] DRF Spectacular installed for API docs
- [x] Authentication endpoint created (`/api/auth/strava/`)
- [x] URLs configured
- [x] REST_FRAMEWORK settings added to settings.py

### Database
- [ ] Run `python manage.py migrate`
- [ ] Verify `authtoken_token` table created
- [ ] Verify `socialaccount_socialaccount` table created

### CORS Configuration
- [ ] Update `CORS_ALLOWED_ORIGINS` in settings.py with frontend URL(s)
  - [ ] Add `http://localhost:3000` for development
  - [ ] Add production frontend URL
- [ ] Verify CORS middleware is in MIDDLEWARE list

### Testing
- [ ] Start server: `python manage.py runserver`
- [ ] Access Swagger docs: `http://localhost:8000/api/docs/`
- [ ] Verify `/api/auth/strava/` endpoint appears in docs
- [ ] Test endpoint with valid Strava token (optional)

## ✅ Strava Application Setup Checklist

### Strava Developer Portal
- [ ] Go to https://www.strava.com/settings/api
- [ ] Create new application or use existing
- [ ] Note down:
  - [ ] Client ID
  - [ ] Client Secret
- [ ] Set Authorization Callback Domain:
  - [ ] `localhost:3000` for development
  - [ ] Your production domain for production

### Strava Settings
- [ ] Application Name set
- [ ] Application Description set
- [ ] Website URL set
- [ ] Application Icon uploaded (optional)

## ✅ Frontend Setup Checklist

### Environment Configuration
- [ ] Create `.env` file
- [ ] Add `VITE_STRAVA_CLIENT_ID=your_client_id`
- [ ] Add `VITE_STRAVA_CLIENT_SECRET=your_client_secret`
- [ ] Add `VITE_REDIRECT_URI=http://localhost:3000/auth/callback`
- [ ] Add `VITE_API_BASE_URL=http://localhost:8000`
- [ ] Add `.env` to `.gitignore`

### Dependencies
- [ ] Install React Router: `npm install react-router-dom`
- [ ] Install any other dependencies (axios, etc.)

### Components to Create
- [ ] **Login.jsx** - Login page with Strava button
  - [ ] Strava login button
  - [ ] Redirect to Strava OAuth URL
  
- [ ] **AuthCallback.jsx** - OAuth callback handler
  - [ ] Get authorization code from URL params
  - [ ] Exchange code for Strava token
  - [ ] Authenticate with backend
  - [ ] Check for profile
  - [ ] Redirect accordingly
  
- [ ] **CreateProfile.jsx** - Profile creation form
  - [ ] CEC input field
  - [ ] Goal input field
  - [ ] Category selector (runner/freestyler)
  - [ ] Submit handler
  - [ ] Error handling
  
- [ ] **ProtectedRoute.jsx** - Route protection component
  - [ ] Check for auth token
  - [ ] Redirect to login if not authenticated

### Services to Create
- [ ] **services/api.js** - API service layer
  - [ ] Base API URL configuration
  - [ ] Token management
  - [ ] Request wrapper with auth headers
  - [ ] Profile endpoints (GET, POST, PATCH)
  - [ ] Workout endpoints (GET, POST, DELETE)
  - [ ] Logout function

### Routing Setup
- [ ] Configure React Router
  - [ ] `/login` → Login component
  - [ ] `/auth/callback` → AuthCallback component
  - [ ] `/create-profile` → CreateProfile component (protected)
  - [ ] `/dashboard` → Dashboard component (protected)
  - [ ] `/` → Redirect to dashboard

### State Management
- [ ] Set up authentication state (Context/Redux/Zustand)
- [ ] User state management
- [ ] Profile state management

## ✅ Integration Testing Checklist

### Authentication Flow
- [ ] Click "Login with Strava" button
- [ ] Redirected to Strava authorization page
- [ ] Strava shows correct app name and permissions
- [ ] After authorization, redirected to `/auth/callback`
- [ ] Loading indicator shows during authentication
- [ ] No console errors during OAuth flow
- [ ] Django token stored in localStorage
- [ ] User data stored in localStorage/state

### New User Flow
- [ ] Profile check returns 404
- [ ] Redirected to `/create-profile`
- [ ] Form displays correctly
- [ ] Form validation works
- [ ] Profile creation succeeds
- [ ] Redirected to dashboard after creation
- [ ] Profile data visible in dashboard

### Returning User Flow
- [ ] Profile check returns 200 with profile data
- [ ] Redirected directly to dashboard
- [ ] User stats display correctly
- [ ] Badges display correctly (if any)

### Protected Routes
- [ ] Accessing protected route without token redirects to login
- [ ] Accessing protected route with token shows content
- [ ] Token persists across page refreshes

### API Integration
- [ ] GET /api/profiles/me/ works with token
- [ ] POST /api/profiles/me/ creates profile
- [ ] PATCH /api/profiles/me/ updates profile
- [ ] GET /api/workouts/ returns workouts
- [ ] POST /api/workouts/ creates workout
- [ ] DELETE /api/workouts/{id}/ deletes workout

### Error Handling
- [ ] Invalid Strava token shows error message
- [ ] Network errors handled gracefully
- [ ] 401 errors trigger logout/redirect
- [ ] Form validation errors display correctly
- [ ] User-friendly error messages shown

## ✅ Production Deployment Checklist

### Backend
- [ ] Update `ALLOWED_HOSTS` in settings.py
- [ ] Update `CORS_ALLOWED_ORIGINS` with production URL
- [ ] Set `DEBUG = False` in production settings
- [ ] Configure production database
- [ ] Set up static files serving
- [ ] Set up media files serving (S3/similar)
- [ ] Configure environment variables
- [ ] Run migrations on production database
- [ ] Collect static files: `python manage.py collectstatic`

### Frontend
- [ ] Update `.env.production` with production URLs
- [ ] Build production bundle: `npm run build`
- [ ] Deploy to hosting (Vercel/Netlify/etc.)
- [ ] Verify environment variables set in hosting platform

### Strava
- [ ] Update Authorization Callback Domain with production domain
- [ ] Update Application Website URL

### Testing in Production
- [ ] Test complete OAuth flow
- [ ] Test user creation
- [ ] Test profile creation
- [ ] Test all API endpoints
- [ ] Check HTTPS working
- [ ] Verify CORS working

## ✅ Security Checklist

### Backend
- [ ] `DEBUG = False` in production
- [ ] Strong `SECRET_KEY` set via environment variable
- [ ] Database credentials in environment variables
- [ ] HTTPS enforced in production
- [ ] CORS properly configured (not ALLOW_ALL)
- [ ] Rate limiting configured (optional)

### Frontend
- [ ] Client secret NOT in frontend code
- [ ] Environment variables properly configured
- [ ] API tokens stored securely (localStorage/httpOnly cookies)
- [ ] No sensitive data in console logs
- [ ] HTTPS used for all API calls

### Strava
- [ ] Client secret kept secure
- [ ] Never commit credentials to git
- [ ] Minimum required scopes requested
- [ ] Webhook signature verification (if using webhooks)

## 📝 Documentation Checklist

- [x] IMPLEMENTATION_SUMMARY.md created
- [x] FRONTEND_AUTH_GUIDE.md created
- [x] AUTHENTICATION_FLOW_DIAGRAM.md created
- [x] SETUP_GUIDE.md created
- [x] QUICK_REFERENCE.md created
- [x] API_FRONTEND_GUIDE.md updated
- [ ] README.md updated with new features
- [ ] Team onboarding docs updated

## 🎉 Launch Checklist

- [ ] All tests passing
- [ ] Documentation complete
- [ ] Team trained on authentication flow
- [ ] Monitoring set up
- [ ] Error tracking configured (Sentry/similar)
- [ ] Backup strategy in place
- [ ] Support contact information updated

---

**Legend:**
- [x] Already completed/configured
- [ ] Needs to be done

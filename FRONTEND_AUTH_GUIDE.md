# Frontend Authentication Guide - Strava OAuth2 Integration

## 🎯 Overview

This guide explains how to authenticate users through Strava OAuth2 and integrate with the Cisco Running backend API.

## 🔄 Authentication Flow Diagram

```
Frontend App → Strava OAuth → Frontend Callback → Backend API → Create User
     ↓              ↓                ↓                  ↓              ↓
  [Login]    [Authorize]      [Get Token]        [Validate]    [Return Token]
```

## 📝 Step-by-Step Implementation

### Step 1: Configure Strava Application

1. Go to [Strava API Settings](https://www.strava.com/settings/api)
2. Create a new application or use existing one
3. Note down:
   - **Client ID**: Your public identifier
   - **Client Secret**: Your secret key (keep secure!)
4. Set **Authorization Callback Domain** to your frontend domain
   - Development: `localhost:3000`
   - Production: `yourfrontend.com`

### Step 2: Frontend - Initiate OAuth Flow

**Environment Variables (.env)**
```env
VITE_STRAVA_CLIENT_ID=your_client_id
VITE_STRAVA_CLIENT_SECRET=your_client_secret
VITE_REDIRECT_URI=http://localhost:3000/auth/callback
VITE_API_BASE_URL=http://localhost:8000
```

**Login Component**
```javascript
// Login.jsx
import { useNavigate } from 'react-router-dom';

function Login() {
  const handleStravaLogin = () => {
    const clientId = import.meta.env.VITE_STRAVA_CLIENT_ID;
    const redirectUri = import.meta.env.VITE_REDIRECT_URI;
    
    const authUrl = new URL('https://www.strava.com/oauth/authorize');
    authUrl.searchParams.append('client_id', clientId);
    authUrl.searchParams.append('response_type', 'code');
    authUrl.searchParams.append('redirect_uri', redirectUri);
    authUrl.searchParams.append('approval_prompt', 'force');
    authUrl.searchParams.append('scope', 'activity:read_all');
    
    window.location.href = authUrl.toString();
  };
  
  return (
    <div className="login-page">
      <h1>Cisco Running Challenge</h1>
      <button onClick={handleStravaLogin} className="strava-login-btn">
        Connect with Strava
      </button>
    </div>
  );
}

export default Login;
```

### Step 3: Frontend - Handle OAuth Callback

**Callback Handler**
```javascript
// AuthCallback.jsx
import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { authenticateWithBackend } from '../services/auth';

function AuthCallback() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState('processing');
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const code = searchParams.get('code');
    const errorParam = searchParams.get('error');
    
    if (errorParam) {
      setError('Authentication was denied');
      setStatus('error');
      return;
    }
    
    if (!code) {
      setError('No authorization code received');
      setStatus('error');
      return;
    }
    
    handleAuthentication(code);
  }, [searchParams]);
  
  const handleAuthentication = async (code) => {
    try {
      setStatus('exchanging');
      
      // Step 1: Exchange code for Strava access token
      const stravaTokenResponse = await fetch('https://www.strava.com/oauth/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          client_id: import.meta.env.VITE_STRAVA_CLIENT_ID,
          client_secret: import.meta.env.VITE_STRAVA_CLIENT_SECRET,
          code: code,
          grant_type: 'authorization_code'
        })
      });
      
      if (!stravaTokenResponse.ok) {
        throw new Error('Failed to get Strava access token');
      }
      
      const stravaData = await stravaTokenResponse.json();
      const { access_token, refresh_token, athlete } = stravaData;
      
      // Store Strava tokens for future use
      localStorage.setItem('strava_access_token', access_token);
      localStorage.setItem('strava_refresh_token', refresh_token);
      
      setStatus('authenticating');
      
      // Step 2: Authenticate with backend
      const username = athlete.username || `strava_${athlete.id}`;
      const backendResponse = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/auth/strava/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          strava_access_token: access_token,
          username: username
        })
      });
      
      if (!backendResponse.ok) {
        const errorData = await backendResponse.json();
        throw new Error(errorData.error || 'Backend authentication failed');
      }
      
      const backendData = await backendResponse.json();
      
      // Store backend token
      localStorage.setItem('auth_token', backendData.token);
      localStorage.setItem('user', JSON.stringify(backendData.user));
      
      setStatus('checking_profile');
      
      // Step 3: Check if user has a profile
      const profileResponse = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/profiles/me/`, {
        headers: {
          'Authorization': `Token ${backendData.token}`
        }
      });
      
      if (profileResponse.status === 404 || profileResponse.status === 400) {
        // No profile exists - redirect to profile creation
        navigate('/create-profile', { 
          state: { 
            isNewUser: true,
            athlete: athlete 
          } 
        });
      } else if (profileResponse.ok) {
        const profile = await profileResponse.json();
        localStorage.setItem('profile', JSON.stringify(profile));
        navigate('/dashboard');
      } else {
        throw new Error('Failed to check profile status');
      }
      
    } catch (err) {
      console.error('Authentication error:', err);
      setError(err.message);
      setStatus('error');
    }
  };
  
  const getStatusMessage = () => {
    switch (status) {
      case 'processing':
        return 'Processing...';
      case 'exchanging':
        return 'Connecting to Strava...';
      case 'authenticating':
        return 'Authenticating with backend...';
      case 'checking_profile':
        return 'Loading your profile...';
      case 'error':
        return `Error: ${error}`;
      default:
        return 'Authenticating...';
    }
  };
  
  return (
    <div className="auth-callback">
      <div className="spinner"></div>
      <p>{getStatusMessage()}</p>
      {status === 'error' && (
        <button onClick={() => navigate('/login')}>
          Back to Login
        </button>
      )}
    </div>
  );
}

export default AuthCallback;
```

### Step 4: Frontend - Create Profile for New Users

**Profile Creation Component**
```javascript
// CreateProfile.jsx
import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

function CreateProfile() {
  const navigate = useNavigate();
  const location = useLocation();
  const athlete = location.state?.athlete;
  
  const [formData, setFormData] = useState({
    cec: '',
    user_goal_km: '42.00',
    category: 'runner'
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      const token = localStorage.getItem('auth_token');
      
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/profiles/me/`, {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          cec: formData.cec,
          user_goal_km: formData.user_goal_km,
          category: formData.category
        })
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.non_field_errors?.[0] || 'Failed to create profile');
      }
      
      const profile = await response.json();
      localStorage.setItem('profile', JSON.stringify(profile));
      
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="create-profile">
      <h1>Welcome to Cisco Running Challenge!</h1>
      {athlete && (
        <div className="athlete-info">
          <p>Hi, {athlete.firstname} {athlete.lastname}!</p>
          <p>Let's set up your profile</p>
        </div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>CEC ID</label>
          <input
            type="text"
            value={formData.cec}
            onChange={e => setFormData({...formData, cec: e.target.value})}
            placeholder="Enter your Cisco CEC ID"
            required
          />
        </div>
        
        <div className="form-group">
          <label>Goal (km)</label>
          <input
            type="number"
            step="0.01"
            value={formData.user_goal_km}
            onChange={e => setFormData({...formData, user_goal_km: e.target.value})}
            placeholder="42.00"
            required
          />
          <small>Set your distance goal for the challenge</small>
        </div>
        
        <div className="form-group">
          <label>Category</label>
          <select
            value={formData.category}
            onChange={e => setFormData({...formData, category: e.target.value})}
          >
            <option value="runner">Runner - Track running activities</option>
            <option value="freestyler">Freestyler - Track various sports</option>
          </select>
          <small>You can change this once later</small>
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        <button type="submit" disabled={loading}>
          {loading ? 'Creating Profile...' : 'Create Profile'}
        </button>
      </form>
    </div>
  );
}

export default CreateProfile;
```

### Step 5: Frontend - API Service Layer

**API Service**
```javascript
// services/api.js
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

class ApiService {
  constructor() {
    this.baseUrl = API_BASE_URL;
  }
  
  getAuthToken() {
    return localStorage.getItem('auth_token');
  }
  
  async request(endpoint, options = {}) {
    const token = this.getAuthToken();
    
    const config = {
      ...options,
      headers: {
        ...options.headers,
        'Authorization': token ? `Token ${token}` : '',
        'Content-Type': 'application/json',
      }
    };
    
    const response = await fetch(`${this.baseUrl}${endpoint}`, config);
    
    if (response.status === 401) {
      // Token expired or invalid - logout
      this.logout();
      window.location.href = '/login';
      throw new Error('Authentication expired');
    }
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || error.error || 'Request failed');
    }
    
    return response.json();
  }
  
  // Profile endpoints
  async getProfile() {
    return this.request('/api/profiles/me/');
  }
  
  async createProfile(data) {
    return this.request('/api/profiles/me/', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }
  
  async updateProfile(data) {
    return this.request('/api/profiles/me/', {
      method: 'PATCH',
      body: JSON.stringify(data)
    });
  }
  
  // Workout endpoints
  async getWorkouts() {
    return this.request('/api/workouts/');
  }
  
  async createWorkout(formData) {
    const token = this.getAuthToken();
    
    // Don't set Content-Type for FormData - browser will set it with boundary
    const response = await fetch(`${this.baseUrl}/api/workouts/`, {
      method: 'POST',
      headers: {
        'Authorization': `Token ${token}`,
      },
      body: formData  // FormData object
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to create workout');
    }
    
    return response.json();
  }
  
  async deleteWorkout(id) {
    return this.request(`/api/workouts/${id}/`, {
      method: 'DELETE'
    });
  }
  
  logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    localStorage.removeItem('profile');
    localStorage.removeItem('strava_access_token');
    localStorage.removeItem('strava_refresh_token');
  }
}

export default new ApiService();
```

### Step 6: Frontend - Protected Routes

**Route Protection**
```javascript
// components/ProtectedRoute.jsx
import { Navigate } from 'react-router-dom';

function ProtectedRoute({ children }) {
  const token = localStorage.getItem('auth_token');
  
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
}

export default ProtectedRoute;
```

**App Router Setup**
```javascript
// App.jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import AuthCallback from './pages/AuthCallback';
import CreateProfile from './pages/CreateProfile';
import Dashboard from './pages/Dashboard';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/auth/callback" element={<AuthCallback />} />
        <Route path="/create-profile" element={
          <ProtectedRoute>
            <CreateProfile />
          </ProtectedRoute>
        } />
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

## 🔧 Backend Configuration Required

### 1. Install Required Packages

Add to `requirements.txt`:
```
djangorestframework
django-allauth
requests
drf-spectacular
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Create Django Tokens Table

```bash
python manage.py migrate authtoken
```

## 🧪 Testing the Flow

### Test Authentication Locally

1. Start Django backend:
```bash
python manage.py runserver
```

2. Test the auth endpoint with curl:
```bash
curl -X POST http://localhost:8000/api/auth/strava/ \
  -H "Content-Type: application/json" \
  -d '{
    "strava_access_token": "your_strava_token",
    "username": "testuser"
  }'
```

Expected response:
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "testuser@example.com",
    "strava_id": "12345678"
  },
  "created": true
}
```

3. Test authenticated endpoint:
```bash
curl http://localhost:8000/api/profiles/me/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

## 🚨 Common Issues & Solutions

### Issue 1: CORS Errors

**Problem:** Browser blocks requests from frontend to backend

**Solution:** Update `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://yourfrontend.com",
]

# Or for development only:
CORS_ALLOW_ALL_ORIGINS = True
```

### Issue 2: 401 Unauthorized

**Problem:** Token not being sent correctly

**Solution:** Verify Authorization header format:
```javascript
headers: {
  'Authorization': `Token ${token}`,  // Note: "Token" not "Bearer"
}
```

### Issue 3: Profile Already Exists

**Problem:** User tries to POST when profile exists

**Solution:** Check for profile first:
```javascript
const profileResponse = await api.getProfile();
if (profileResponse) {
  // Profile exists, use PATCH to update
} else {
  // Create new profile with POST
}
```

### Issue 4: Strava Token Expires

**Problem:** Strava access tokens expire after 6 hours

**Solution:** Implement token refresh:
```javascript
async function refreshStravaToken() {
  const refreshToken = localStorage.getItem('strava_refresh_token');
  
  const response = await fetch('https://www.strava.com/oauth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      client_id: STRAVA_CLIENT_ID,
      client_secret: STRAVA_CLIENT_SECRET,
      grant_type: 'refresh_token',
      refresh_token: refreshToken
    })
  });
  
  const data = await response.json();
  localStorage.setItem('strava_access_token', data.access_token);
  localStorage.setItem('strava_refresh_token', data.refresh_token);
  
  return data.access_token;
}
```

## 📊 What Gets Created

When a user authenticates through Strava:

1. **Django User** - Created in `auth_user` table
   - username: from Strava or custom
   - email: from Strava athlete data
   - first_name, last_name: from Strava

2. **SocialAccount** - Created in `socialaccount_socialaccount` table
   - Links Django user to Strava account
   - Stores Strava user ID (uid)
   - Stores extra athlete data (JSON)

3. **Token** - Created in `authtoken_token` table
   - One-to-one with User
   - Used for all API authentication

4. **Profile** - Created by user in `/create-profile`
   - Links to User via belongs_to field
   - Stores CEC, goals, category, etc.

## 🔐 Security Best Practices

1. **Never expose client secret in frontend code**
   - Use environment variables
   - Store in `.env` file
   - Add `.env` to `.gitignore`

2. **HTTPS in production**
   - All API calls must use HTTPS
   - Strava requires HTTPS for production callbacks

3. **Token storage**
   - Use localStorage for simplicity
   - Consider httpOnly cookies for better security
   - Implement token expiration handling

4. **Validate on backend**
   - Backend always validates Strava tokens
   - Never trust frontend data

## 🎉 Complete Flow Summary

```
User clicks "Login with Strava"
  ↓
Redirected to Strava OAuth
  ↓
User authorizes app
  ↓
Redirected back with code
  ↓
Frontend exchanges code for Strava access_token
  ↓
Frontend sends access_token to /api/auth/strava/
  ↓
Backend validates token with Strava API
  ↓
Backend creates User + SocialAccount
  ↓
Backend returns Django token
  ↓
Frontend stores token
  ↓
Frontend checks if profile exists
  ↓
If no profile → /create-profile
If profile exists → /dashboard
```

## 📚 Additional Resources

- [Strava API Documentation](https://developers.strava.com/docs/authentication/)
- [Django REST Framework Authentication](https://www.django-rest-framework.org/api-guide/authentication/)
- [Django Allauth](https://django-allauth.readthedocs.io/)

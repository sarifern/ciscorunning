# Testing Strava OAuth Authentication

## ✅ Endpoint Status
- **URL**: `POST /api/auth/strava/`
- **Authentication Required**: ❌ **NO** (uses `@permission_classes([AllowAny])`)
- **Content-Type**: `application/json`

## 🧪 Testing Methods

### Method 1: Using cURL (Command Line)

```bash
curl -X POST https://ciscorunning.herokuapp.com/api/auth/strava/ \
  -H "Content-Type: application/json" \
  -d '{
    "strava_access_token": "your_strava_access_token_here",
    "username": "johndoe"
  }'
```

**Local Testing:**
```bash
curl -X POST http://localhost:8000/api/auth/strava/ \
  -H "Content-Type: application/json" \
  -d '{
    "strava_access_token": "your_strava_access_token_here",
    "username": "johndoe"
  }'
```

### Method 2: Using Postman

1. **Method**: POST
2. **URL**: `https://ciscorunning.herokuapp.com/api/auth/strava/`
3. **Headers**:
   - `Content-Type`: `application/json`
4. **Body** (raw JSON):
```json
{
  "strava_access_token": "your_strava_access_token_here",
  "username": "johndoe"
}
```

### Method 3: Using JavaScript (Frontend)

```javascript
const authenticateWithStrava = async (stravaAccessToken, username) => {
  const response = await fetch('https://ciscorunning.herokuapp.com/api/auth/strava/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
      // NO Authorization header needed!
    },
    body: JSON.stringify({
      strava_access_token: stravaAccessToken,
      username: username
    })
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Authentication failed');
  }
  
  const data = await response.json();
  return data; // { token, user, created }
};

// Usage
try {
  const result = await authenticateWithStrava('abc123...', 'johndoe');
  console.log('Django Token:', result.token);
  console.log('User:', result.user);
  console.log('New User?', result.created);
  
  // Store token for future API calls
  localStorage.setItem('authToken', result.token);
} catch (error) {
  console.error('Auth failed:', error.message);
}
```

### Method 4: Using Python `requests`

```python
import requests

url = 'https://ciscorunning.herokuapp.com/api/auth/strava/'
payload = {
    'strava_access_token': 'your_strava_access_token_here',
    'username': 'johndoe'
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    data = response.json()
    print(f"Django Token: {data['token']}")
    print(f"User: {data['user']}")
    print(f"Created: {data['created']}")
else:
    print(f"Error: {response.json()}")
```

## 📝 How to Get a Strava Access Token (For Testing)

### Option 1: Complete OAuth Flow

```javascript
// Step 1: Redirect to Strava
const CLIENT_ID = 'your_strava_client_id';
const REDIRECT_URI = 'http://localhost:3000/auth/callback';

window.location.href = `https://www.strava.com/oauth/authorize?client_id=${CLIENT_ID}&response_type=code&redirect_uri=${REDIRECT_URI}&scope=activity:read_all`;

// Step 2: In your callback, exchange code for token
const code = new URLSearchParams(window.location.search).get('code');

const tokenResponse = await fetch('https://www.strava.com/oauth/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    client_id: 'your_client_id',
    client_secret: 'your_client_secret',
    code: code,
    grant_type: 'authorization_code'
  })
});

const { access_token, athlete } = await tokenResponse.json();

// Step 3: Now authenticate with Django
const djangoAuth = await fetch('https://ciscorunning.herokuapp.com/api/auth/strava/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    strava_access_token: access_token,
    username: athlete.username
  })
});

const { token } = await djangoAuth.json();
// Use this token for all subsequent API calls!
```

### Option 2: Manual Testing with Existing Token

If you already have a Strava account and app:

1. Go to https://www.strava.com/settings/api
2. Create an application (if you haven't)
3. Note your Client ID and Client Secret
4. Get a temporary token for testing:
   - Use Strava's OAuth Playground or Postman
   - Or use this URL (replace CLIENT_ID):
     ```
     https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://localhost&scope=activity:read_all
     ```
5. Exchange the code for an access token
6. Use that token to test the `/api/auth/strava/` endpoint

## ✅ Expected Responses

### Success (200 OK)

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

### Error: Missing Parameters (400 Bad Request)

```json
{
  "error": "Both strava_access_token and username are required"
}
```

### Error: Invalid Token (401 Unauthorized)

```json
{
  "error": "Invalid Strava access token",
  "detail": "Token validation failed with Strava API"
}
```

### Error: Account Mismatch (403 Forbidden)

```json
{
  "error": "Strava account mismatch",
  "detail": "The Strava account does not match this user"
}
```

### Error: Strava API Down (503 Service Unavailable)

```json
{
  "error": "Failed to validate Strava token",
  "detail": "Connection timeout..."
}
```

## 🔐 Using the Django Token

After successful authentication, use the returned token for all API calls:

```javascript
// Store token
const djangoToken = result.token;

// Use in API calls
const profileResponse = await fetch('https://ciscorunning.herokuapp.com/api/profiles/me/', {
  headers: {
    'Authorization': `Token ${djangoToken}`,
    'Content-Type': 'application/json'
  }
});

const profile = await profileResponse.json();
```

## 🧪 Complete Test Flow

```javascript
// Complete authentication and profile creation flow
async function testCompleteFlow() {
  // 1. Authenticate with Strava token
  console.log('Step 1: Authenticating with Strava...');
  const authResponse = await fetch('http://localhost:8000/api/auth/strava/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      strava_access_token: 'YOUR_STRAVA_TOKEN',
      username: 'testuser'
    })
  });
  
  const { token, user, created } = await authResponse.json();
  console.log('✅ Authenticated!', { token, user, created });
  
  // 2. Check if profile exists
  console.log('Step 2: Checking for profile...');
  const profileCheckResponse = await fetch('http://localhost:8000/api/profiles/me/', {
    headers: { 'Authorization': `Token ${token}` }
  });
  
  if (profileCheckResponse.status === 404) {
    console.log('No profile found, creating one...');
    
    // 3. Create profile
    const createProfileResponse = await fetch('http://localhost:8000/api/profiles/me/', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        cec: user.username,
        user_goal_km: 42,
        category: 'runner'
      })
    });
    
    const profile = await createProfileResponse.json();
    console.log('✅ Profile created!', profile);
  } else {
    const profile = await profileCheckResponse.json();
    console.log('✅ Profile exists!', profile);
  }
  
  console.log('🎉 Complete flow successful!');
}

// Run the test
testCompleteFlow().catch(console.error);
```

## 📚 Swagger UI

You can also test the endpoint interactively at:
- **Swagger UI**: http://localhost:8000/api/docs/
- **Production**: https://ciscorunning.herokuapp.com/api/docs/

Look for the **POST /api/auth/strava/** endpoint and click "Try it out".

## 🔍 Debugging Tips

### Check if endpoint is unauthenticated:
```bash
# This should NOT return 401 Unauthorized, but 400 Bad Request (missing params)
curl -X POST http://localhost:8000/api/auth/strava/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

Expected: `{"error": "Both strava_access_token and username are required"}`

If you get `401 Unauthorized`, the endpoint requires authentication (BUG!).

### Verify Strava token is valid:
```bash
# Test your Strava token directly
curl -X GET https://www.strava.com/api/v3/athlete \
  -H "Authorization: Bearer YOUR_STRAVA_TOKEN"
```

Should return your Strava athlete profile.

### Enable Django Debug Mode:
In `local_settings.py`, ensure:
```python
DEBUG = True
```

This will show detailed error messages in the response.

## ⚠️ Important Notes

1. **No Authentication Header**: The `/api/auth/strava/` endpoint does NOT require authentication because you don't have a Django token yet!

2. **Strava Token Validation**: The endpoint validates your Strava token by calling Strava's API, so make sure your token has the `activity:read_all` scope.

3. **User Creation**: If the user doesn't exist, it's automatically created from Strava profile data.

4. **Account Linking**: The SocialAccount is created/updated to link your Strava ID to the Django user.

5. **Token Persistence**: The Django token returned is permanent until explicitly deleted. Store it securely!

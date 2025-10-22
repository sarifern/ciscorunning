# Authentication Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      STRAVA OAUTH2 AUTHENTICATION FLOW                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Frontend   │      │    Strava    │      │   Backend    │      │   Database   │
│              │      │    OAuth     │      │     API      │      │              │
└──────┬───────┘      └──────┬───────┘      └──────┬───────┘      └──────┬───────┘
       │                     │                     │                     │
       │                                                                  │
   [1] User clicks                                                        │
       "Login with Strava"                                                │
       │                                                                  │
       │──────────────────────────────────────────────────────────────────────────┐
       │ Redirect to Strava Authorization                                │        │
   [2] │ https://www.strava.com/oauth/authorize?                         │        │
       │   client_id=xxx&                                                │        │
       │   response_type=code&                                           │        │
       │   redirect_uri=http://yourfrontend.com/auth/callback&           │        │
       │   scope=activity:read_all                                       │        │
       │──────────────────────────────────────────────────────────────────────────┘
       │                     │                                            │
       │                     │                                            │
       │                 [3] User authorizes app                          │
       │                     on Strava                                    │
       │                     │                                            │
       │<────────────────────┘                                            │
   [4] Redirect back with code                                            │
       http://yourfrontend.com/auth/callback?code=AUTHORIZATION_CODE     │
       │                                                                  │
       │                                                                  │
       │─────────────────────>                                            │
   [5] Exchange code for token                                            │
       POST /oauth/token                                                  │
       {                                                                  │
         client_id: xxx,                                                  │
         client_secret: xxx,                                              │
         code: AUTHORIZATION_CODE,                                        │
         grant_type: authorization_code                                   │
       }                                                                  │
       │                     │                                            │
       │<─────────────────────                                            │
   [6] Returns access token                                               │
       {                                                                  │
         access_token: "strava_token_xxx",                                │
         refresh_token: "refresh_xxx",                                    │
         athlete: {                                                       │
           id: 12345678,                                                  │
           username: "johndoe",                                           │
           firstname: "John",                                             │
           lastname: "Doe",                                               │
           email: "john@example.com"                                      │
         }                                                                │
       }                                                                  │
       │                                                                  │
       │                                     │                            │
       │─────────────────────────────────────>                            │
   [7] Authenticate with backend                                          │
       POST /api/auth/strava/                                             │
       {                                                                  │
         strava_access_token: "strava_token_xxx"                                               │
       }                                                                  │
       │                                     │                            │
       │                                     │─────────────────────────────>
   [8]                                       Validate Strava token        │
                                             GET https://www.strava.com/api/v3/athlete
                                             Authorization: Bearer strava_token_xxx
                                             │                            │
                                             │<─────────────────────────────
                                         [9] Returns athlete data         │
                                             {                            │
                                               id: 12345678,              │
                                               username: "johndoe",       │
                                               ...                        │
                                             }                            │
                                             │                            │
                                             │                            │
                                             │──────────────────────────────>
                                        [10] Create/Get User              │
                                             - Check if User exists        │
                                             - If not, create new User     │
                                             │                            │
                                             │<──────────────────────────────
                                        [11] User created/retrieved       │
                                             │                            │
                                             │──────────────────────────────>
                                        [12] Create/Get SocialAccount     │
                                             - Link User to Strava        │
                                             - Store Strava ID            │
                                             │                            │
                                             │<──────────────────────────────
                                        [13] SocialAccount linked         │
                                             │                            │
                                             │──────────────────────────────>
                                        [14] Create/Get Token             │
                                             - Generate Django token      │
                                             │                            │
                                             │<──────────────────────────────
                                        [15] Token created                │
       │                                     │                            │
       │<─────────────────────────────────────                            │
  [16] Returns Django token                                               │
       {                                                                  │
         token: "django_token_9944b09...",                                │
         user: {                                                          │
           id: 1,                                                         │
           username: "johndoe",                                           │
           email: "john@example.com",                                     │
           strava_id: "12345678"                                          │
         },                                                               │
         created: true                                                    │
       }                                                                  │
       │                                                                  │
       │                                                                  │
  [17] Store token in localStorage                                        │
       localStorage.setItem('auth_token', 'django_token_9944b09...')     │
       │                                                                  │
       │                                                                  │
       │─────────────────────────────────────>                            │
  [18] Check if profile exists                                            │
       GET /api/profiles/me/                                              │
       Authorization: Token django_token_9944b09...                       │
       │                                     │                            │
       │                                     │──────────────────────────────>
       │                                [19] Query Profile                │
       │                                     WHERE belongs_to = user_id   │
       │                                     │                            │
       │                                     │<──────────────────────────────
       │                                [20] Profile found/not found      │
       │<─────────────────────────────────────                            │
  [21] Response                                                           │
       │                                                                  │
       │                                                                  │
       ├──── IF PROFILE EXISTS (200 OK) ────────────────────────────────────┐
       │    {                                                             │ │
       │      user: "johndoe",                                            │ │
       │      distance: "25.50",                                          │ │
       │      awarded_badges: [...]                                       │ │
       │    }                                                             │ │
       │                                                                  │ │
  [22] │    Navigate to /myworkouts                                       │ │
       │    Show user workouts                                            │ │
       └────────────────────────────────────────────────────────────────────┘
       │                                                                  │
       │                                                                  │
       ├──── IF PROFILE NOT FOUND (404 NOT FOUND) ──────────────────────────┐
       │    {                                                             │ │
       │      detail: "Not found."                                        │ │
       │    }                                                             │ │
       │                                                                  │ │
  [23] │    Navigate to /create-profile                                   │ │
       │                                                                  │ │
  [24] │    User fills form:                                              │ │
       │    - CEC ID                                                      │ │
       │    - Goal (km)                                                   │ │
       │    - Category (runner/freestyler) 
            - Avatar picture(prefilled by last response)                  │ │
       │                                                                  │ │
  [25] │─────────────────────────────────────>                            │ │
       │    POST /api/profiles/me/                                        │ │
       │    Authorization: Token django_token_9944b09...                  │ │
       │    {                                                             │ │
       │      cec: "johndoe",                                             │ │
       │      user_goal_km: "42.00",                                      │ │
       │      category: "runner"                                          │ │
       │      avatar: "https://lh3.googleusercontent.com/a/               │ | │ACg8ocLddd8wCRRQgLkims3zuim1fc6ifmfLKZ-M2AVXXXXXXXX"              | |
       │    }                                                             │ │
       │                                     │                            │ │
       │                                     │──────────────────────────────>│
       │                                [26] Create Profile               │ │
       │                                     - Set belongs_to = user_id   │ │
       │                                     - Set actual_category =      │ │
       │                                       "beginnerrunner"            │ │
       │                                     │                            │ │
       │                                     │<──────────────────────────────│
       │                                [27] Profile created              │ │
       │<─────────────────────────────────────                            │ │
  [28] │    Response:                                                     │ │
       │    {                                                             │ │
       │      user: "johndoe",                                            │ │
       │      cec: "johndoe",                                             │ │
       │      category: "runner",                                         │ │
       │      actual_category: "Beginner Runner",                         │ │
       │      user_goal_km: "42.00",                                      │ │
       │      distance: "0.00",                                           │ │
       │      awarded_badges: []                                          │ │
       │    }                                                             │ │
       │                                                                  │ │
  [29] │    Navigate to /myworkouts                                       │ │
       └────────────────────────────────────────────────────────────────────┘
       │                                                                  │
       │                                                                  │
  [30] User is now fully authenticated with:                              │
       ✓ Strava account linked                                            │
       ✓ Django user created                                              │
       ✓ SocialAccount created                                            │
       ✓ Django token stored                                              │
       ✓ Profile created                                                  │
       │                                                                  │
       │                                                                  │
  [31] For subsequent requests:                                           │
       │─────────────────────────────────────>                            │
       │    GET /api/workouts/                                            │
       │    Authorization: Token django_token_9944b09...                  │
       │                                     │                            │
       │<─────────────────────────────────────                            │
       │    Returns workout data                                          │
       │                                                                  │

┌─────────────────────────────────────────────────────────────────────────────┐
│                         DATABASE ENTITIES CREATED                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  auth_user                                                                   │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │ id: 1                                                             │       │
│  │ username: "johndoe"                                               │       │
│  │ email: "john@example.com"                                         │       │
│  │ first_name: "John"                                                │       │
│  │ last_name: "Doe"                                                  │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                                                              │
│  socialaccount_socialaccount                                                 │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │ user_id: 1                                                        │       │
│  │ provider: "strava"                                                │       │
│  │ uid: "12345678"                                                   │       │
│  │ extra_data: {"id": 12345678, "username": "johndoe", ...}          │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                                                              │
│  authtoken_token                                                             │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │ key: "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"                   │       │
│  │ user_id: 1                                                        │       │
│  │ created: "2024-12-18T10:30:00Z"                                   │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                                                              │
│  ic_marathon_app_profile                                                     │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │ belongs_to_id: 1                                                  │       │
│  │ cec: "johndoe"                                                    │       │
│  │ category: "runner"                                                │       │
│  │ user_goal_km: 42.00                                               │       │
│  │ distance: 0.00                                                    │       │
│  │ current_streak: 0                                                 │       │
│  │ longest_streak: 0                                                 │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

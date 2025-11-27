# Cisco Running Challenge 2025# Cisco Running



🏃‍♂️ **Marathon-Style Fitness Competition** | December 12, 2024 - January 6, 2025 (26 Days)Repo for Web APP Cisco Running Challenge 2025



[![Python](https://img.shields.io/badge/Python-3.11.6-blue.svg)](https://python.org)## 🏃‍♂️ Overview

[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://djangoproject.com)

[![License](https://img.shields.io/badge/License-Cisco_Internal-red.svg)](LICENSE)The Cisco Running Challenge is a marathon-style fitness competition running from **December 12, 2024 to January 6, 2025** (26 days). Participants can compete in two main tracks:

- **Runner Track**: Traditional running activities

---- **Freestyler Track**: Various sports (cycling, swimming, hiking, etc.) converted to km equivalents



## 📋 Table of Contents### Key Features



- [Overview](#overview)- 🏅 **Smart Category System**: Auto-assigns beginners and promotes based on performance

- [Key Features](#key-features)- 🚫 **Anti-Sandbagging**: Prevents skilled athletes from dominating beginner categories

- [Architecture](#architecture)- 📊 **Separate Leaderboards**: Beginner Runner, Runner, Beginner Freestyler, Freestyler

- [Quick Start](#quick-start)- 🎯 **Goal Tracking**: Personal distance goals with achievement badges

- [Installation](#installation)- 🔐 **REST API**: Full CRUD operations with authentication

  - [Mac Installation](#installation-mac)- 📝 **Swagger Documentation**: Interactive API docs at `/api/docs/`

  - [Windows Installation](#installation-windows)- 🏆 **Badge System**: Distance achievements (10K-168K) + Streak badges (7, 14, 21 days)

- [Running Locally](#running-locally)- 🔥 **Streak Tracking**: Automatic tracking of current and longest workout streaks

- [API Documentation](#api-documentation)

- [Partner Workouts](#partner-workouts)---

- [Badge System](#badge-system)

- [Category System](#category-system)#### 2. Profile Management

- [Deployment](#deployment)

- [Testing](#testing)- [Architecture](#architecture)

- [Troubleshooting](#troubleshooting)- [Installation](#installation)

- [License](#license)  - [Mac Installation](#installation-in-mac)

  - [Windows Installation](#installation-in-windows)

---- [API Documentation](#api-documentation)

- [Modern Frontend Integration](#modern-frontend-integration)

## 🏃‍♂️ Overview- [Streak Tracking System](#streak-tracking-system)

- [Category System](#category-system)

The Cisco Running Challenge is a gamified fitness competition where participants compete in two main tracks:- [Running the Project](#running-the-project)

- [Deployment](#heroku-deployment)

- **Runner Track**: Traditional running activities

- **Freestyler Track**: Various sports (cycling, swimming, hiking, etc.) converted to km equivalents---



### Event Details## Architecture

- **Start Date**: December 12, 2024

- **End Date**: January 6, 2025### 🏗️ Headless Backend + Modern Frontend

- **Duration**: 26 days

- **Target**: 168km (equivalent to 4 marathons)The Cisco Running application follows a modern **headless CMS architecture**:

- **Awards**: Multiple distance and streak achievement badges

```

---┌─────────────────────────────────────────────────────────┐

│                   Modern Frontend                        │

## 🎯 Key Features│          (React/Vue/Svelte/Next.js/etc.)                │

│                                                          │

### 🏅 Smart Category System│  • Strava OAuth Integration                             │

- **Auto-Assignment**: Everyone starts as a beginner│  • Real-time Badge Notifications                        │

- **Auto-Promotion**: System detects and promotes skilled athletes based on performance│  • Progressive Web App (PWA)                            │

- **Anti-Sandbagging**: Prevents gaming the system with multiple detection methods│  • Responsive Design                                     │

- **Four Categories**: Beginner Runner, Runner, Beginner Freestyler, Freestyler└─────────────────────────────────────────────────────────┘

                         ↕ HTTP/REST

### 🤝 Partner Workouts┌─────────────────────────────────────────────────────────┐

- **1.5x Distance Bonus**: Train with a partner and earn 50% bonus distance│              Django REST API (Headless)                  │

- **Same Category Required**: Partners must be in the same track (both runners or both freestylers)│                                                          │

- **Confirmation System**: Partner must confirm before bonus is applied│  • Token Authentication                                  │

- **Dual Tracking**: Both partners get the bonus distance│  • Auto-calculated Metrics                              │

│  • Badge System                                          │

### 🏆 Achievement Badges│  • Anti-Sandbagging Logic                               │

- **Distance Badges**: 10K, 21K, 42K, 84K, 126K, 168K, Personal Goal│  • Swagger Documentation                                 │

- **Streak Badges**: 7-day, 14-day, 21-day consecutive workout achievements└─────────────────────────────────────────────────────────┘

- **Automatic Awards**: Real-time badge checking on every workout submission                         ↕

- **Permanent**: Once earned, badges are never lost┌─────────────────────────────────────────────────────────┐

│          Django Admin (Auditing/Legacy)                  │

### 🔥 Streak Tracking│                                                          │

- **Current Streak**: Tracks consecutive days with workouts│  • Workout Auditing (is_audited flag)                   │

- **Longest Streak**: Records personal best (never decreases)│  • User Management                                       │

- **Smart Detection**: Resets if you skip a day│  • Manual Badge Awards                                   │

- **Gamification**: Encourages daily participation│  • Database Management                                   │

└─────────────────────────────────────────────────────────┘

### 🔐 REST API```

- **Full CRUD Operations**: Complete API for profiles and workouts

- **Token Authentication**: Secure API access with Strava OAuth integration### Key Architectural Decisions

- **Swagger Documentation**: Interactive API docs at `/api/docs/`

- **Modern Frontend Ready**: Headless CMS architecture for React/Vue/Next.js1. **Headless API**: Django serves only JSON via REST API

2. **Token Auth**: Modern frontends use token-based authentication

### 📊 Separate Leaderboards3. **CORS Enabled**: Cross-origin requests allowed for frontend apps

- Four distinct leaderboards for fair competition4. **Admin Preserved**: Django admin remains for auditing and management

- Real-time ranking updates5. **Backward Compatible**: Legacy Django templates still work but deprecated

- Position tracking within your category

---

---

## Modern Frontend Integration

## 🏗️ Architecture

### 🚀 Quick Start for Frontend Developers

### Headless Backend + Modern Frontend

#### 1. Authentication Flow (To Be Implemented)

```

┌─────────────────────────────────────────────────────────┐Authentication will be handled by your modern frontend. The backend provides:

│                   Modern Frontend                        │- Token-based authentication via DRF

│          (React/Vue/Svelte/Next.js/etc.)                │- Profile management endpoints

│                                                          │- Workout tracking endpoints

│  • Strava OAuth Integration                             │

│  • Real-time Badge Notifications                        │**Basic API Usage:**

│  • Progressive Web App (PWA)                            │```javascript

│  • Responsive Design                                     │// Once you have a token (from your auth system)

└─────────────────────────────────────────────────────────┘const apiRequest = (url, options = {}) => {

                         ↕ HTTP/REST  return fetch(url, {

┌─────────────────────────────────────────────────────────┐    ...options,

│              Django REST API (Headless)                  │    headers: {

│                                                          │      ...options.headers,

│  • Token Authentication                                  │      'Authorization': `Token ${your_token_here}`,

│  • Auto-calculated Metrics                              │      'Content-Type': 'application/json'

│  • Badge System                                          │    }

│  • Anti-Sandbagging Logic                               │  });

│  • Swagger Documentation                                 │};

└─────────────────────────────────────────────────────────┘```

                         ↕

┌─────────────────────────────────────────────────────────┐#### 2. Complete User Flow

│          Django Admin (Auditing/Legacy)                  │

│                                                          │```javascript

│  • Workout Auditing (is_audited flag)                   │// A. Check if user has profile

│  • User Management                                       │const checkProfile = async () => {

│  • Manual Badge Awards                                   │  try {

│  • Database Management                                   │    const response = await apiRequest('https://ciscorunning.herokuapp.com/api/profiles/me/');

└─────────────────────────────────────────────────────────┘    if (response.ok) {

```      const profile = await response.json();

      return profile;

### Technical Stack    }

  } catch (error) {

- **Backend**: Django 4.2.7    return null; // No profile exists

- **REST Framework**: Django REST Framework 3.16.1  }

- **API Docs**: drf-spectacular 0.27.0};

- **Database**: PostgreSQL 17

- **Storage**: AWS S3 (ciscorunningaws bucket in us-east-2)// B. Create profile if needed

- **Cache**: Memcached Cloud (Heroku addon)const createProfile = async (profileData) => {

- **Authentication**: Django AllAuth + Token Auth + Strava OAuth  const response = await apiRequest('https://ciscorunning.herokuapp.com/api/profiles/me/', {

- **Badges**: Django Badgify    method: 'POST',

- **Frontend**: Django Templates + CUI CSS Framework (legacy)    body: JSON.stringify({

- **Deployment**: Heroku (ciscorunning app)      cec: profileData.cec,

      user_goal_km: profileData.goalKm,

---      category: profileData.category // 'runner' or 'freestyler'

    })

## 🚀 Quick Start  });

  return response.json();

### For Frontend Developers};



1. **Get API Token via Strava OAuth**// C. Submit workout and get badge notifications

2. **Create Profile**: `POST /api/profiles/me/`const submitWorkout = async (workoutData) => {

3. **Submit Workouts**: `POST /api/workouts/`  const formData = new FormData();

4. **Track Progress**: `GET /api/profiles/me/`  formData.append('belongs_to', profile.id);

5. **Check Badges**: Included in profile response  formData.append('distance', workoutData.distance);

  formData.append('date_time', workoutData.dateTime);

See [API Documentation](#api-documentation) for complete details.  formData.append('time', workoutData.duration);

  formData.append('sport', workoutData.sportId);

### For Backend Developers  formData.append('intensity', workoutData.intensity);

  formData.append('photo_evidence', workoutData.photo);

1. Clone repository  

2. Set up virtual environment  const response = await fetch('https://ciscorunning.herokuapp.com/api/workouts/', {

3. Install dependencies    method: 'POST',

4. Configure `.secrets` and `local_settings.py`    headers: {

5. Run migrations      'Authorization': `Token ${localStorage.getItem('authToken')}`

6. Initialize badges    },

7. Start server    body: formData

  });

See [Installation](#installation) for step-by-step instructions.  

  const result = await response.json();

---  

  // Check for newly awarded badges

## 📦 Installation  if (result.newly_awarded_badges && result.newly_awarded_badges.length > 0) {

    result.newly_awarded_badges.forEach(badge => {

### Prerequisites      showBadgeNotification(badge); // Your UI notification function

    });

- Python 3.11.6  }

- PostgreSQL 17  

- Git  return result;

- Virtual environment tool (venv/virtualenv)};

```

### Installation (Mac)

#### 3. Profile Management

1. **Clone the repository**

```bash```javascript

git clone https://github.com/sarifern/ciscorunning.git// Get profile with all badges

cd ciscorunningconst getProfile = async () => {

```  const response = await apiRequest('https://ciscorunning.herokuapp.com/api/profiles/me/');

  const profile = await response.json();

2. **Set up git config**  

```bash  /*

git config --global user.name "Your Name"  Profile structure:

git config --global user.email "your.email@cisco.com"  {

```    user: "johndoe",

    cec: "johndoe",

3. **Edit hosts file** (requires sudo)    category: "runner",  // Intent (runner or freestyler)

```bash    actual_category: "Beginner Runner",  // Current progression

sudo nano /etc/hosts    distance: "25.50",

# Add:    user_goal_km: "42.00",

127.0.0.1 www.lurifern.com    current_streak: 7,

```    longest_streak: 12,

    workout_days_count: 18,

4. **Install PostgreSQL**    awarded_badges: [

```bash      {

brew reinstall openssl        slug: "10K",

export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/        name: "10K Record Smashed",

brew install postgresql        description: "Congrats! You set a new 10k personal record",

```        awarded_at: "2024-12-18T10:30:00Z"

      },

5. **Add pg_config to PATH** (in ~/.bash_profile or ~/.zshrc)      // ... more badges

```bash    ]

export PATH=$PATH:/usr/local/bin/pg_config  }

```  */

  

6. **Install Xcode tools**  return profile;

```bash};

xcode-select --install

```// Update goal

const updateGoal = async (newGoalKm) => {

7. **Create virtual environment**  const response = await apiRequest('https://ciscorunning.herokuapp.com/api/profiles/me/', {

```bash    method: 'PATCH',

python3.11 -m virtualenv venv    body: JSON.stringify({ user_goal_km: newGoalKm })

source venv/bin/activate  });

```  return response.json();

};

8. **Install dependencies**

```bash// Switch category (one-time only)

env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2==2.9.9const switchCategory = async (newCategory) => {

pip install -r requirements.txt  const response = await apiRequest('https://ciscorunning.herokuapp.com/api/profiles/me/', {

```    method: 'PATCH',

    body: JSON.stringify({ category: newCategory }) // 'runner' or 'freestyler'

9. **Configure environment** (get `.secrets` from admin)  });

```bash  return response.json();

# Place .secrets in project root};

export $(grep -v '^#' .secrets | xargs)```

```

#### 4. Badge Display

10. **Collect static files** (if needed)

```bash```javascript

python manage.py collectstatic --settings=ic_marathon_site.local_settings// Display badge gallery

```const displayBadges = (profile) => {

  const allBadges = [

11. **Setup badge system**    { slug: '10K', locked: true },

```bash    { slug: '21K', locked: true },

python manage.py makemigrations badgify --settings=ic_marathon_site.local_settings    { slug: '42K', locked: true },

python manage.py migrate badgify --settings=ic_marathon_site.local_settings    { slug: '84K', locked: true },

python manage.py badgify_sync badges --settings=ic_marathon_site.local_settings    { slug: '126K', locked: true },

python manage.py badgify_reset --settings=ic_marathon_site.local_settings    { slug: '168K', locked: true },

python manage.py badgify_sync awards --disable-signals --settings=ic_marathon_site.local_settings    { slug: 'ownK', locked: true },

python manage.py badgify_sync counts --settings=ic_marathon_site.local_settings    { slug: '7day-streak', locked: true },

```    { slug: '14day-streak', locked: true },

    { slug: '21day-streak', locked: true },

12. **Run migrations**  ];

```bash  

python manage.py makemigrations --settings=ic_marathon_site.local_settings  // Mark earned badges as unlocked

python manage.py migrate --settings=ic_marathon_site.local_settings  profile.awarded_badges.forEach(earnedBadge => {

```    const badge = allBadges.find(b => b.slug === earnedBadge.slug);

    if (badge) {

13. **Initialize badges**      badge.locked = false;

```bash      badge.name = earnedBadge.name;

python manage.py shell < initialize_badges.py --settings=ic_marathon_site.local_settings      badge.description = earnedBadge.description;

```      badge.awarded_at = earnedBadge.awarded_at;

    }

14. **Create superuser**  });

```bash  

python manage.py createsuperuser --settings=ic_marathon_site.local_settings  return allBadges;

```};



### Installation (Windows)// Calculate progress

const calculateProgress = (profile) => {

1. **Clone the repository**  const totalBadges = 10;

```powershell  const earnedBadges = profile.awarded_badges.length;

git clone https://github.com/sarifern/ciscorunning.git  const percentage = (earnedBadges / totalBadges) * 100;

cd ciscorunning  

```  return {

    earned: earnedBadges,

2. **Set up git config**    total: totalBadges,

```powershell    percentage: Math.round(percentage)

git config user.name "Your Name"  };

git config user.email "your.email@cisco.com"};

``````



3. **Edit hosts file** (Run Notepad as Administrator)### 🔒 CORS Configuration

```

# In C:\Windows\System32\drivers\etc\hostsCORS is pre-configured to allow requests from any origin during development. For production, you should restrict allowed origins in `local_settings.py`:

# Add:

127.0.0.1 www.apradofern.com```python

```CORS_ALLOWED_ORIGINS = [

    "https://your-frontend-app.com",

4. **Install PostgreSQL 17**    "https://your-frontend-app.vercel.app",

- Download from: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads]

- Set superuser password during installation```



5. **Install Microsoft C++ Build Tools**### 📱 Strava OAuth Integration

- Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

- Select "Desktop development with C++"The backend already has Strava OAuth configured via Django Allauth. For your modern frontend:

- Only install the included packages (C++ Build Tools core features, C++ 2022 Redistributable, C++ core desktop features)

1. **Backend Handles OAuth**: Use the existing `/accounts/strava/login/` endpoint

6. **Create virtual environment**2. **Redirect Flow**: Configure Strava to redirect to your frontend

```powershell3. **Token Exchange**: Frontend receives token and uses it for API calls

pip install virtualenv

virtualenv .venv --python=3.11---

.\.venv\Scripts\activate

```## API Documentation



7. **Install dependencies**### 🔗 Base URL

```powershell- **Local**: `https://localhost:8000/api/`

pip install -r requirements.txt- **Production**: `https://ciscorunning.herokuapp.com/api/`

pip install -U setuptools

```### 📚 Interactive Documentation

- **Swagger UI**: `/api/docs/` - Full interactive API documentation

8. **Configure environment** (get `.secrets` from admin)- **ReDoc**: `/api/redoc/` - Alternative documentation view

```powershell- **OpenAPI Schema**: `/api/schema/` - Raw OpenAPI 3.0 schema

# Place .secrets in project root

get-content .secrets | foreach {### 🔐 Authentication

    $name, $value = $_.split('=')

    set-content env:\$name $valueAll API endpoints require authentication. The API uses token-based authentication.

}

$env:ENVIRONMENT='local_settings'**Supported Methods:**

```- **Token Authentication**: Use REST Framework tokens (recommended for API clients)

- **Session Authentication**: Use Django's session system (for browsable API)

9. **Collect static files** (if needed)- **Basic Authentication**: Username/password with each request (for testing only)

```powershell

python manage.py collectstatic --settings=ic_marathon_site.$env:ENVIRONMENT**Note**: Authentication details will be finalized based on your frontend OAuth implementation.

```

#### Using the Token

10. **Setup badge system**

```powershellInclude the token in the `Authorization` header of all API requests:

python manage.py makemigrations badgify --settings=ic_marathon_site.$env:ENVIRONMENT

python manage.py migrate badgify --settings=ic_marathon_site.$env:ENVIRONMENT```http

python manage.py badgify_sync badges --settings=ic_marathon_site.$env:ENVIRONMENTAuthorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

python manage.py badgify_reset --settings=ic_marathon_site.$env:ENVIRONMENT```

python manage.py badgify_sync awards --disable-signals --settings=ic_marathon_site.$env:ENVIRONMENT

python manage.py badgify_sync counts --settings=ic_marathon_site.$env:ENVIRONMENT**Example with fetch:**

``````javascript

const response = await fetch('https://ciscorunning.herokuapp.com/api/profiles/me/', {

11. **Run migrations**  headers: {

```powershell    'Authorization': 'Token your-token-here',

python manage.py makemigrations --settings=ic_marathon_site.$env:ENVIRONMENT    'Content-Type': 'application/json'

python manage.py migrate --settings=ic_marathon_site.$env:ENVIRONMENT  }

```});

```

12. **Initialize badges**

```powershell**Example with axios:**

python manage.py shell --settings=ic_marathon_site.$env:ENVIRONMENT```javascript

>>> exec(open('initialize_badges.py').read())axios.defaults.headers.common['Authorization'] = 'Token your-token-here';

>>> exit()```

```

### 📌 Endpoints

13. **Create superuser**

```powershell#### Profile Management

python manage.py createsuperuser --settings=ic_marathon_site.$env:ENVIRONMENT

```##### `GET /api/profiles/me/`

Get your own profile information.

14. **Create cache table**

```powershell**Response Example:**

python manage.py createcachetable --settings=ic_marathon_site.$env:ENVIRONMENT```json

```{

  "user": "john.doe",

---  "user_goal_km": "42.00",

  "category": "runner",

## 🖥️ Running Locally  "actual_category": "Beginner Runner",

  "cec": "johndoe",

### Using VSCode Debugger  "avatar": "https://ciscorunning2023.s3.us-east-1.amazonaws.com/static/img/user.png",

  "distance": "15.50",

VSCode is preconfigured with `.vscode/launch.json` for debugging.  "category_changed": false,

  "current_streak": 5,

### Manual Start  "longest_streak": 12,

  "workout_days_count": 18,

**Mac/Linux:**  "awarded_badges": [

```bash    {

python manage.py runsslserver --settings=ic_marathon_site.local_settings      "slug": "10K",

```      "name": "10K Record Smashed",

      "description": "Congrats! You set a new 10k personal record",

**Windows:**      "awarded_at": "2024-12-18T10:30:00Z"

```powershell    },

python manage.py runsslserver --settings=ic_marathon_site.$env:ENVIRONMENT    {

```      "slug": "7day-streak",

      "name": "Week Warrior",

### Access Points      "description": "Amazing! You completed 7 consecutive days of workouts!",

      "awarded_at": "2024-12-20T08:15:00Z"

- **Web Interface**: https://www.lurifern.com:8000 (Mac) or https://www.apradofern.com:8000 (Windows)    }

- **Admin Panel**: https://localhost:8000/admin  ]

- **API Root**: https://localhost:8000/api/}

- **API Docs**: https://localhost:8000/api/docs/```



---**Notes:**

- `category`: Shows your selected track (runner or freestyler)

## 📚 API Documentation- `actual_category`: Shows your current progression (Beginner Runner → Runner)

- `distance`: Auto-calculated from workouts (read-only)

### Base URLs- `current_streak`: Consecutive days with workouts (resets if you skip a day)

- `longest_streak`: Your personal best streak record

- **Development**: `http://localhost:8000/api/`- `workout_days_count`: Total unique days you've worked out

- **Production**: `https://ciscorunning-ecfd9da3d311.herokuapp.com/api/`- `awarded_badges`: Array of all badges you've earned (with full details)



### Interactive Documentation##### `POST /api/profiles/me/`

Create your profile.

- **Swagger UI**: `/api/docs/`

- **ReDoc**: `/api/redoc/`**Request Body:**

- **OpenAPI Schema**: `/api/schema/````json

{

### Authentication  "cec": "johndoe",

  "user_goal_km": "42.00",

The API uses Token-based authentication with Strava OAuth integration.  "category": "runner"

}

#### Step 1: Strava OAuth (Frontend)```



```javascript**Notes:**

// Redirect user to Strava for authorization- You can only select `"runner"` or `"freestyler"`

const STRAVA_CLIENT_ID = 'your_strava_client_id';- Backend automatically assigns you to beginner category

const REDIRECT_URI = 'https://yourfrontend.com/auth/callback';- You'll be auto-promoted based on performance

const STRAVA_AUTH_URL = `https://www.strava.com/oauth/authorize?client_id=${STRAVA_CLIENT_ID}&response_type=code&redirect_uri=${REDIRECT_URI}&approval_prompt=force&scope=activity:read_all`;

##### `PUT /api/profiles/me/`

window.location.href = STRAVA_AUTH_URL;Update your entire profile (or create if doesn't exist).

```

**Request Body:**

#### Step 2: Exchange Code for Token```json

{

```javascript  "cec": "johndoe",

// Strava redirects back with authorization code  "user_goal_km": "84.00",

const exchangeTokens = async (code) => {  "category": "runner"

  const response = await fetch('https://www.strava.com/oauth/token', {}

    method: 'POST',```

    headers: { 'Content-Type': 'application/json' },

    body: JSON.stringify({##### `PATCH /api/profiles/me/`

      client_id: 'your_strava_client_id',Partially update your profile.

      client_secret: 'your_strava_client_secret',

      code: code,**Request Body (any fields):**

      grant_type: 'authorization_code'```json

    }){

  });  "user_goal_km": "84.00"

  }

  const data = await response.json();```

  return data.access_token; // Use this with backend

};**Notes:**

```- Can update `user_goal_km` unlimited times

- Can only change `category` (runner ↔ freestyler) **once**

#### Step 3: Authenticate with Backend- Cannot manually change beginner status (auto-managed)



```javascript##### `DELETE /api/profiles/me/`

const authenticateWithBackend = async (stravaAccessToken) => {Delete your profile and all associated workouts.

  const response = await fetch('https://ciscorunning.herokuapp.com/api/auth/strava/', {

    method: 'POST',**Response:** `204 No Content`

    headers: { 'Content-Type': 'application/json' },

    body: JSON.stringify({**Warning:** This action cannot be undone. All workouts will be permanently deleted.

      strava_access_token: stravaAccessToken

    })#### Workout Management

  });

  ##### `GET /api/workouts/`

  const { token, user } = await response.json();List all your workouts.

  localStorage.setItem('authToken', token);

  return { token, user };**Response Example:**

};```json

```[

  {

#### Step 4: Use Token for API Calls    "belongs_to": 1,

    "distance": "5.00",

```javascript    "date_time": "2024-12-15T08:30:00Z",

const apiRequest = (url, options = {}) => {    "time": "00:30:00",

  return fetch(url, {    "sport": 1,

    ...options,    "intensity": 2,

    headers: {    "photo_evidence": "https://..."

      ...options.headers,  }

      'Authorization': `Token ${localStorage.getItem('authToken')}`,]

      'Content-Type': 'application/json'```

    }

  });##### `POST /api/workouts/`

};Create a new workout.

```

**Request Body:**

### Core Endpoints```json

{

#### Profile Management  "belongs_to": 1,

  "distance": "5.00",

##### `GET /api/profiles/me/`  "date_time": "2024-12-15T08:30:00Z",

Get current user's profile with all data.  "time": "00:30:00",

  "sport": 1,

**Response:**  "intensity": 2,

```json  "photo_evidence": "<file>"

{}

  "user": "johndoe",```

  "cec": "johndoe",

  "category": "runner",**Response Example:**

  "actual_category": "Beginner Runner",```json

  "user_goal_km": "42.00",{

  "distance": "25.50",  "belongs_to": 1,

  "current_streak": 7,  "distance": "5.00",

  "longest_streak": 12,  "date_time": "2024-12-15T08:30:00Z",

  "workout_days_count": 18,  "time": "00:30:00",

  "category_changed": false,  "sport": 1,

  "avatar": "https://...",  "intensity": 2,

  "awarded_badges": [  "photo_evidence": "https://...",

    {  "newly_awarded_badges": [

      "slug": "10K",    {

      "name": "10K Record Smashed",      "slug": "7day-streak",

      "description": "Congrats! You set a new 10k personal record",      "name": "Week Warrior",

      "awarded_at": "2024-12-18T10:30:00Z"      "description": "Amazing! You completed 7 consecutive days of workouts!",

    }      "awarded_at": "2024-12-15T08:30:00Z"

  ]    }

}  ]

```}

```

##### `POST /api/profiles/me/`

Create a new profile (first-time registration).**Notes:**

- `newly_awarded_badges`: Array of badges earned with this workout (empty if none)

**Request:**- Badges are checked automatically after workout is saved

```json- Distance and streak metrics are updated via signals

{- Frontend can display badge notifications based on this response

  "cec": "johndoe",

  "user_goal_km": 42.00,---

  "category": "runner"

}## Streak Tracking System

```

### 🔥 How Streaks Work

**Response:** Same as GET, with new profile data.

The system automatically tracks your workout consistency through two key metrics:

**Notes:**

- `category` must be "runner" or "freestyler"#### Current Streak

- Backend auto-assigns to beginner categories- **Definition**: Number of consecutive days with at least one workout

- Can only create one profile per user- **Behavior**: Resets to 0 if you skip a day

- **Validation**: Only counts if your last workout was today or yesterday

##### `PATCH /api/profiles/me/`- **Example**: Work out Mon-Tue-Wed-Thu-Fri = 5-day current streak

Update profile (goal or category).

#### Longest Streak

**Request:**- **Definition**: Your personal best consecutive workout streak

```json- **Behavior**: Never decreases, only updates when you break your record

{- **Used For**: Awarding permanent achievement badges

  "user_goal_km": 84.00- **Example**: If you had a 12-day streak in week 1, that's your longest streak even if current streak is 3

}

```### 🏆 Streak Badges



**Category Change Rules:**Earn progressive achievements based on your **longest streak**:

- Can only change once (`category_changed` flag)

- Must have < 50km to change tracks| Badge | Requirement | Description |

- Workouts and distance carry over|-------|-------------|-------------|

- Reset to beginner in new track| **Week Warrior** 🏆 | 7 consecutive days | Complete 7 days in a row |

| **Fortnight Champion** 🎖️ | 14 consecutive days | Complete 14 days in a row |

#### Workout Management| **Three Week Legend** 🏅 | 21 consecutive days | Complete 21 days in a row (81% of event!) |



##### `GET /api/workouts/`**Why longest streak?** Because we want to reward your achievements permanently. Once earned, streak badges stay in your profile forever!

List all workouts for authenticated user.

### 📊 Streak Examples

**Response:**

```json**Perfect Dedication:**

[```

  {Days 1-7: Workout every day → Week Warrior badge earned ✓

    "uuid": "123e4567-e89b-12d3-a456-426614174000",Days 8-14: Continue → Fortnight Champion badge earned ✓

    "belongs_to": 1,Days 15-21: Continue → Three Week Legend badge earned ✓

    "distance": "5.00",Current: 21-day streak | Longest: 21 days

    "date_time": "2024-12-15T08:30:00Z",```

    "time": "00:30:00",

    "sport": 1,**Comeback Story:**

    "intensity": 2,```

    "photo_evidence": "https://...",Days 1-12: Workout every day → Longest: 12 days

    "uploaded_at": "2024-12-15T08:30:00Z",Day 13: Skip workout → Current streak resets to 0

    "edition": 2025Days 14-20: Workout every day → Current: 7 days | Longest: still 12

  }Continue to Day 27 → Current: 14 days | Longest: 14 days (new record!)

]```

```

**Consistent Participant:**

##### `POST /api/workouts/````

Submit a new workout.Pattern: Workout Mon-Fri, rest weekends

Week 1: 5-day streak → breaks on Saturday

**Request (multipart/form-data):**Week 2: 5-day streak → breaks on Saturday

```javascriptWeek 3: 5-day streak → breaks on Saturday

const formData = new FormData();Result: Longest streak is 5 days (no badges yet)

formData.append('distance', '5.00');```

formData.append('date_time', '2024-12-15T08:30:00Z');

formData.append('time', '00:30:00');### 🎯 Strategy Tips

formData.append('sport', 1); // Running

formData.append('intensity', 2); // Moderate- **Daily commitment wins**: Even a short 2km run counts for your streak

formData.append('photo_evidence', fileBlob);- **Plan ahead**: The event is 26 days, so 21-day badge leaves 5 rest days

- **Mixed activities**: Freestylers can alternate sports to avoid burnout

const response = await fetch('/api/workouts/', {- **Early morning**: Log workouts early to maintain streak pressure-free

  method: 'POST',

  headers: { 'Authorization': `Token ${token}` },---

  body: formData

});## Category System

```

### 🎯 How Categories Work

**Response:**

```json#### User Experience

{When you sign up, you choose:

  "uuid": "123e4567-e89b-12d3-a456-426614174000",- **Runner** - Traditional running

  "belongs_to": 1,- **Freestyler** - Various sports activities

  "distance": "5.00",

  "date_time": "2024-12-15T08:30:00Z",#### Behind the Scenes

  "time": "00:30:00",The system automatically:

  "sport": 1,1. Assigns you to the **beginner version** of your chosen category

  "intensity": 2,2. Tracks your performance across multiple metrics

  "photo_evidence": "https://...",3. Auto-promotes you when you demonstrate skill/consistency

  "uploaded_at": "2024-12-15T08:30:00Z",

  "edition": 2025,### 📊 The Four Categories

  "newly_awarded_badges": [

    {| Category | Badge | Description |

      "slug": "10K",|----------|-------|-------------|

      "name": "10K Record Smashed",| **Beginner Runner** | 🏃 | New to running, < 84km or < 10 days |

      "description": "Congrats! You set a new 10k personal record",| **Runner** | 🏃🏃 | Experienced runners, promoted automatically |

      "awarded_at": "2024-12-15T08:30:15Z"| **Beginner Freestyler** | 🚴 | New to varied sports, < 84km or < 10 days |

    }| **Freestyler** | 🚴🚴 | Experienced athletes, promoted automatically |

  ]

}### 🚀 Auto-Promotion System

```

You are automatically promoted when you meet **ANY** of these criteria:

**Important:**

- `belongs_to` is auto-set from authentication token (read-only)#### Path 1: High Distance + Consistency

- `newly_awarded_badges` array contains any badges just earned- **84km** total distance

- Distance triggers auto-promotion logic- **10+ unique workout days**

- Streak tracking updates automatically- Example: 8.4km/day for 10 days



##### `PATCH /api/workouts/{uuid}/`#### Path 2: Performance Level Detection (Anti-Sandbagging) ⭐

Update an existing workout.- **5+ workouts** averaging **7km+ each**

- Example: 10km, 8km, 9km, 7km, 11km = Promoted after 5th workout

##### `DELETE /api/workouts/{uuid}/`- **Prevents skilled runners from staying in beginner category**

Delete a workout (reverses distance, recalculates streaks).

#### Path 3: Super Consistent Participation

#### Reference Data- **42km** total distance

- **15+ unique workout days**

##### `GET /api/reference-data/`- Example: 2.8km/day for 15 days

Get all sports, intensities, and conversion mappings.

### 🛡️ Anti-Sandbagging Protection

**Response:**

```json**Problem:** In previous editions, skilled runners would sign up as "Beginner Runner" and dominate the leaderboard while staying just under promotion thresholds.

{

  "sports": [**Solution:** The system now detects skilled athletes in multiple ways:

    { "id": 1, "name": "Running" },

    { "id": 2, "name": "Cycling" },| Sandbagging Strategy | Detection Method | Result |

    { "id": 3, "name": "Swimming" }|---------------------|------------------|---------|

  ],| "Run 83km and stop" | Averaging 8km+ per workout → Path 2 | ✅ Promoted |

  "intensity_levels": [| "Run big then stop" | 50km in 5 workouts = 10km avg → Path 2 | ✅ Promoted |

    { "id": 1, "name": "Light" },| "Many small runs" | 45km over 16 days → Path 3 | ✅ Promoted |

    { "id": 2, "name": "Moderate" },| True beginner | 25km over 8 days, 3km avg | ❌ Stays beginner |

    { "id": 3, "name": "High" }

  ],### 📈 Progression Examples

  "mappings": [

    {**Skilled Runner (Auto-Promoted Fast):**

      "sport_id": 1,```

      "sport_name": "Running",Day 1: 10km → Day 2: 9km → Day 3: 11km → Day 4: 8km → Day 5: 12km

      "intensity_id": 2,Total: 50km over 5 days, avg 10km/workout

      "intensity_name": "Moderate",Result: AUTO-PROMOTED to Runner (Path 2 triggered)

      "km_per_hour": 10.0```

    }

  ]**Dedicated Beginner (Eventually Promoted):**

}```

```Week 1: 3km x 7 days = 21km

Week 2: 3km x 7 days = 21km  

**Use Case:** Get this data once on app load to populate dropdowns and calculate distance.Week 3: 3km x 2 days = 6km

Total: 48km over 16 days

---Result: AUTO-PROMOTED to Runner (Path 3 triggered)

```

## 🤝 Partner Workouts

**True Beginner (Stays in Category):**

### Overview```

Sporadic participation: 3km, 4km, 2km, 5km, 3km over 8 days

Partner Workouts allow two users in the same category track to train together and earn a **1.5x distance bonus** (50% extra distance).Total: 17km over 8 days

Result: Stays in Beginner Runner category

### Key Features```



- **1.5x Bonus**: Both partners get 50% extra distance### 🔄 Category Changes

- **Category Matching**: Partners must be in same track (runners or freestylers)

- **Confirmation Required**: Partner must confirm before bonus appliesUsers can switch tracks (Runner ↔ Freestyler) **only once**, with safeguards to prevent gaming:

- **Dual Tracking**: Both workouts created with same `partner_workout_group` UUID

- **Pending System**: View sent and received partner requests#### ✅ Rules for Changing Category



### Business Rules| Rule | Requirement | Reason |

|------|-------------|---------|

1. **Same Category Track**: Can only partner with users in same parent category| **One-Time Only** | Can only change once | Prevents category hopping |

   - Runners (Beginner Runner + Runner) can partner together| **Distance Limit** | Must have < 50km | Prevents switching to dominate leaderboard |

   - Freestylers (Beginner Freestyler + Freestyler) can partner together| **Workouts Preserved** | All workouts carry over | Fair - respects effort invested |

| **Beginner Reset** | Start at beginner level in new track | Ensures fair competition |

2. **1.5x Distance Bonus**: Applied ONLY after confirmation

   - Original distance stored in `base_distance` field#### 📋 Examples

   - Bonus distance: `base_distance × 1.5`

**✅ Allowed Change (Low Distance):**

3. **Dual Workout Creation**:```

   - User A submits → Creates workout with `partner_confirmed=False`User: Beginner Runner, 25km over 10 days

   - User B confirms → User A's workout updated + User B's workout createdAction: Switch to Freestyler

   - Both share same `partner_workout_group` UUIDResult: Becomes Beginner Freestyler with 25km

Reason: Under 50km limit ✓

4. **Decline Handling**:```

   - User B can decline → Original workout deleted

   - No notifications or timeouts**✅ Allowed Change (Early Switch):**

```

5. **Profile Requirements**:User: Beginner Runner, 5km over 2 days

   - Partner must have profile with CECAction: Switch to Freestyler

   - No workout history requiredResult: Becomes Beginner Freestyler with 5km

   - Cannot partner with yourselfReason: Under 50km limit - early exploration encouraged ✓

```

### User Flow

**❌ Blocked Change (Too Much Distance):**

#### Submitting a Partner Workout```

User: Beginner Runner, 75km over 20 days  

1. User A clicks "Add Partner Workout" buttonAction: Try to switch to Freestyler

2. Selects partner from dropdown (filtered by category)Result: BLOCKED - "Cannot change with 75km completed"

3. Enters distance, date, uploads photoReason: 75km > 50km limit (likely trying to game leaderboard) ✗

4. Submits → Workout created with `partner_confirmed=False````

5. No distance added to totals yet

**❌ Blocked Change (Already Changed):**

#### Confirming a Partner Workout```

User: Previously changed Runner → Freestyler

1. User B sees notification of pending requestAction: Try to switch back to Runner

2. Clicks "View Pending Requests"Result: BLOCKED - "Already changed category once"

3. Reviews workout details (distance, date, photo)Reason: Only one change allowed per user ✗

4. Clicks "Accept":```

   - User A's workout: `partner_confirmed=True`, distance updated to `base_distance × 1.5`

   - User B's workout: Created automatically with same details and bonus#### 🎯 Why These Rules?

   - Both workouts linked via `partner_workout_group` UUID

5. OR clicks "Decline":1. **50km Limit**: Prevents skilled athletes with high mileage from switching to beginner category

   - User A's workout deleted2. **One-Time Only**: Encourages commitment to a track

   - No further action needed3. **Workouts Carry Over**: Fair to users who genuinely want to try a different track

4. **Beginner Reset**: Ensures fair competition - no "instant expert" status

### Database Schema5. **Early Switch Allowed**: Users exploring early aren't penalized - encourages finding the right fit



```sql#### 💻 How to Change (Web Interface)

-- Partner Workout Fields

is_partner_workout       BOOLEAN DEFAULT FALSE1. Go to **My Profile** page

partner_profile_id       INTEGER (FK to Profile)2. Click **"Change Category"** button (only visible if eligible)

partner_confirmed        BOOLEAN DEFAULT FALSE3. Review rules and current progress

partner_workout_group    UUID4. Select new category (Runner or Freestyler)

base_distance            DECIMAL(5,2) DEFAULT 0.005. Confirm change (double confirmation required)

```6. You're now in Beginner [New Category] and can progress normally



### Web Interface#### 🔧 How to Change (API)



**Add Partner Workout:**```bash

- `/add_partner_workout/` - For runners# Check if eligible to change

- `/add_partner_workoutfs/` - For freestylerscurl -X GET https://ciscorunning.herokuapp.com/api/profiles/me/ \

  -H "Authorization: Token YOUR_TOKEN"

**Manage Requests:**

- `/pending_partner_requests/` - View sent/received requests# Response includes:

- `/confirm_partner_workout/<uuid>/` - Confirm/decline specific request# "category_changed": false  # Can change

# "distance": 35.5           # Under 50km ✓

**API Endpoint:**

- `GET /get_category_members/` - Get eligible partners (JSON)# Make the change

curl -X PATCH https://ciscorunning.herokuapp.com/api/profiles/me/ \

### Example Scenarios  -H "Authorization: Token YOUR_TOKEN" \

  -H "Content-Type: application/json" \

**Scenario 1: Successful Partner Workout**  -d '{"category": "freestyler"}'

```

Day 1:# System will:

- Alice (Beginner Runner, 15km total) submits 10km partner workout with Bob# 1. Validate: distance < 50km? ✓

- Bob (Runner, 50km total) receives pending request# 2. Set category_changed = true

- Alice's workout: 10km (unconfirmed), not added to her 15km total yet# 3. Set category = "beginnerfreestyler"

# 4. Keep all workouts and distance

Day 2:```

- Bob accepts the request

- Alice's workout: Updated to 15km (10 × 1.5), added to her total → 30km---

- Bob's workout: Created with 15km, added to his total → 65km

- Both workouts share same partner_workout_group UUID## Installation in MAC

```

0. Install VSCode and VSCode python plugin.

**Scenario 2: Declined Partner Workout**

```1. Clone the project.

Day 1:

- Alice (Beginner Runner, 15km) submits 8km partner workout with Bob2. Set up your git global config

- Bob receives pending request

- Alice's workout: 8km (unconfirmed), not counted``` 

git config --global user.name "<Your name>"     

Day 2:git config --global user.email "<Your email>"

- Bob declines the request``` 

- Alice's workout: Deleted

- Alice's total: Still 15km (unchanged)3. Edit your hostnames file and add the following

```

``` 

**Scenario 3: Category Mismatch Prevention**#in /etc/hosts

```#add

- Alice (Runner) tries to select Charlie (Freestyler) as partner

- System: Dropdown only shows runners (Bob, David, Emma)127.0.0.1         www.lurifern.com

- Prevention: Can't even submit cross-category partner request``` 

```

4. Install PostgreSQL 

### Admin Interface

``` 

Partner workouts show special indicators in admin:brew reinstall openssl

export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/

- **Partner Status Column**: Color-coded (green=confirmed, orange=pending)brew install postgresql

- **Filters**: Filter by `is_partner_workout` and `partner_confirmed```` 

- **Search**: Search by partner CEC

- **Workout Display**: Shows "🤝 Partner with [name]" and bonus calculation4.1 Add the path out of 



---``` 

which pg_config

## 🏆 Badge System``` 

to your PATH declaration in your shell profile (for example ~/.bash_profile)

### Overview

``` 

The badge system automatically awards achievements based on distance milestones and workout streaks.export PATH=$PATH:/usr/local/bin/pg_config

``` 

### Distance Badges5. Install Xcode tools



| Badge | Requirement | Equivalent |``` 

|-------|-------------|------------|xcode-select --install

| 10K Record Smashed | 10km total | Entry level |``` 

| 21K Award Unlocked | 21km total | Half marathon |

| 42K Milestone | 42km total | Full marathon |6. Create a virtual environment for Python 3.11.

| 84K Milestone | 84km total | 2 marathons |

| 126K Milestone | 126km total | 3 marathons |``` 

| 168K Milestone | 168km total | 4 marathons (event target) |python3.11 -m virtualenv env

| My Milestone | Personal goal | Custom achievement |``` 



### Streak Badges6. a. Activate your environment



| Badge | Requirement | % of Event |``` 

|-------|-------------|------------|source env/bin/activate

| Week Warrior | 7 consecutive days | 27% of event |```

| Fortnight Champion | 14 consecutive days | 54% of event |

| Three Week Legend | 21 consecutive days | 81% of event |7. install the packages



### Badge Mechanics``` 

env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2==2.8.3

- **Automatic Checking**: Every workout save triggers badge evaluationpip install -r requirements.txt 

- **Real-Time Awards**: Newly earned badges returned in API response``` 

- **Permanent**: Once earned, badges never expire or get removed

- **Streak Based**: Streak badges use `longest_streak` (not current_streak)8. Please add the .secrets and local-settings.py files. Ask for them to the admins lurifern@cisco.com

- **API Integration**: `newly_awarded_badges` array in POST responseSet .secrets at the parent folder, and local-settings.py under the ic_marathon_site folder



### Badge Display8.1 Execute



**Profile Response:**``` 

```jsonexport $(grep -v '^#' .secrets | xargs)

{``` 

  "awarded_badges": [

    {9. Collect static files

      "slug": "10K",

      "name": "10K Record Smashed",``` 

      "description": "Congrats! You set a new 10k personal record",python manage.py collectstatic --settings=ic_marathon_site.local_settings

      "awarded_at": "2024-12-18T10:30:00Z"``` 

    },

    {10. Setup the badging system

      "slug": "7day-streak",

      "name": "Week Warrior",``` 

      "description": "Amazing! You completed 7 consecutive days of workouts!",python manage.py makemigrations badgify --settings=ic_marathon_site.local_settings

      "awarded_at": "2024-12-20T08:15:00Z"python manage.py migrate badgify --settings=ic_marathon_site.local_settings

    }python manage.py badgify_sync badges --settings=ic_marathon_site.local_settings

  ]python manage.py badgify_reset --settings=ic_marathon_site.local_settings

}python manage.py badgify_sync awards --disable-signals --settings=ic_marathon_site.local_settings

```python manage.py badgify_sync counts --settings=ic_marathon_site.local_settings

``` 

### Frontend Badge Notifications

11. Make the DB migrations

```javascript

// After submitting workout``` 

const submitWorkout = async (workoutData) => {python manage.py makemigrations --settings=ic_marathon_site.local_settings

  const response = await apiRequest('/api/workouts/', {python manage.py migrate --settings=ic_marathon_site.local_settings

    method: 'POST',```

    body: formData

  });12. Run the initialize_badges.py script

  

  const result = await response.json();``` 

  python manage.py shell < initialize_badges.py  --settings=ic_marathon_site.local_settings

  // Show badge notifications``` 

  if (result.newly_awarded_badges && result.newly_awarded_badges.length > 0) {

    result.newly_awarded_badges.forEach(badge => {13. Create a superuser

      showNotification({

        title: `🏆 ${badge.name}`,``` 

        message: badge.description,python manage.py createsuperuser --settings=ic_marathon_site.local_settings

        type: 'success'```  

      });# Installation in Windows

    });

  }0. Install VSCode and VSCode python plugin. Install Python 3.11.6

  

  return result;1. Clone the project.

};

```2. Set up your git global config



---``` 

git config user.name "<Your name>"     

## 📊 Category Systemgit config user.email "<Your email>"

``` 

### Four Categories

3. Edit your hostnames file in Notepad(run as administrator) and add the following

1. **Beginner Runner**: Entry level for running track

2. **Runner**: Advanced level for running track``` 

3. **Beginner Freestyler**: Entry level for freestyle track#in C:\Windows\System32\drivers\etc\hosts

4. **Freestyler**: Advanced level for freestyle track#add



### Auto-Promotion System127.0.0.1 www.apradofern.com

``` 

Everyone starts as a beginner and gets automatically promoted based on performance. The system has three detection paths:

4. Install PostgreSQL 17.X https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

#### Path 1: High Distance + Consistency

- **84km** total distanceSet the password for the superuser (postgres).

- **10+ unique workout days**

- Example: 8.4km/day for 10 days5. Install Microsoft C++ Build Tools https://visualstudio.microsoft.com/visual-cpp-build-tools/

- **Prevents**: "Run to 83km and stop" sandbaggingPick Desktop development with C++, and deselect the optional packages. Only install the included packages:

C++ Build Tools core features

#### Path 2: Performance Level Detection (Anti-Sandbagging) ⭐C++ 2022 Redistributable Update

- **5+ workouts** averaging **7km+ each**C++ core desktop features

- Example: 10km, 8km, 9km, 7km, 11km = Promoted after 5th workout

- **Prevents**: Skilled runners staying in beginner category6. Create a virtual environment for Python 3.11.6 using VSCode (venv)



#### Path 3: Super Consistent Participation``` 

- **42km** total distancepip install virtualenv

- **15+ unique workout days**virtualenv .venv --python=3.11

- Example: 2.8km/day for 15 days``` 

- **Rewards**: Dedicated daily participationTo activate the environment, use the following command:

``` 

### Anti-Sandbagging ProtectionPS C:\Users\sarifern\CX\ciscorunning> .\venv\Scripts\activate

(venv) PS C:\Users\sarifern\CX\ciscorunning> 

| Sandbagging Strategy | Detection Method | Result |``` 

|---------------------|------------------|---------|Install requirements

| "Run 83km and stop" | Averaging 8km+ per workout → Path 2 | ✅ Promoted |``` 

| "Run big then stop" | 50km in 5 workouts = 10km avg → Path 2 | ✅ Promoted |(venv) PS C:\Users\sarifern\CX\ciscorunning> pip install -r requirements.txt

| "Many small runs" | 45km over 16 days → Path 3 | ✅ Promoted |```

| True beginner | 25km over 8 days, 3km avg | ❌ Stays beginner |

Upgrade setup tools

### Category Change Rules``` 

(venv) PS C:\Users\sarifern\CX\ciscorunning> pip install -U setuptools

Users can switch tracks (Runner ↔ Freestyler) **once**, with safeguards:```



| Rule | Requirement | Reason |7. Please add the .secrets and local-settings.py files. Ask for them to the admins Sari Fernandez (sarifern@cisco.com) and Alfredo Prado (apradoca@cisco.com)

|------|-------------|---------|Set .secrets at the parent folder, and local-settings.py under the ic_marathon_site folder

| **One-Time Only** | Can only change once | Prevents category hopping |

| **Distance Limit** | Must have < 50km | Prevents leaderboard gaming |8.1 Execute the following lines

| **Workouts Preserved** | All workouts carry over | Fair - respects effort |

| **Beginner Reset** | Start at beginner in new track | Ensures fair competition |``` 

get-content .secrets | foreach {

**Examples:**     $name, $value = $_.split('=')

     set-content env:\$name $value

✅ **Allowed:** Beginner Runner with 25km → Switch to Freestyler → Becomes Beginner Freestyler with 25km }

$env:ENVIRONMENT='local_settings'

❌ **Blocked:** Runner with 75km → Try to switch → BLOCKED (over 50km limit)``` 



❌ **Blocked:** Already changed once → Try to change again → BLOCKED (one-time limit)9. Collect static files (only if the bucket was recently created)



---``` 

python manage.py collectstatic --settings=ic_marathon_site.$env:ENVIRONMENT

## 🚀 Deployment``` 



### Heroku Deployment10. Setup the badging system



The application is deployed on Heroku: `ciscorunning` app.``` 

python manage.py makemigrations badgify --settings=ic_marathon_site.$env:ENVIRONMENT

**Production URL:** https://ciscorunning-ecfd9da3d311.herokuapp.com/python manage.py migrate badgify --settings=ic_marathon_site.$env:ENVIRONMENT

python manage.py badgify_sync badges --settings=ic_marathon_site.$env:ENVIRONMENT

#### Prerequisitespython manage.py badgify_reset --settings=ic_marathon_site.$env:ENVIRONMENT

python manage.py badgify_sync awards --disable-signals --settings=ic_marathon_site.$env:ENVIRONMENT

1. **Heroku CLI**: Install from https://devcenter.heroku.com/articles/heroku-clipython manage.py badgify_sync counts --settings=ic_marathon_site.$env:ENVIRONMENT

2. **Git**: Committed changes ready to deploy``` 

3. **Heroku Access**: Permission to deploy to `ciscorunning` app

11. Make the DB migrations

#### Deployment Steps

``` 

1. **Login to Heroku**python manage.py makemigrations --settings=ic_marathon_site.$env:ENVIRONMENT

```bashpython manage.py migrate --settings=ic_marathon_site.$env:ENVIRONMENT

heroku login```

```

12. Run the initialize_badges.py script

2. **Add Git Remote** (if not already added)

```bashThis creates all achievement badges in the database:

heroku git:remote -a ciscorunning- **Distance Badges**: 10K, 21K, 42K, 84K, 126K, 168K, ownK (personal goal)

```- **Streak Badges**: 7-day (Week Warrior), 14-day (Fortnight Champion), 21-day (Three Week Legend)



3. **Push to Heroku**``` 

```bashpython manage.py shell  --settings=ic_marathon_site.$env:ENVIRONMENT

git push heroku legacy_app_2025:main>>> exec(open('initialize_badges.py').read())

```>>> exit()

``` 

4. **Run Migrations**

```bash13. Create a superuser

heroku run python manage.py migrate -a ciscorunning

`````` 

python manage.py createsuperuser --settings=ic_marathon_site.$env:ENVIRONMENT

5. **Monitor Logs**```  

```bash

heroku logs --tail -a ciscorunning14. Create a cache table

`````` 

python manage.py createcachetable --settings=ic_marathon_site.$env:ENVIRONMENT

#### Environment Variables``` 

# Running the project locally

Set via Heroku CLI:

```bashIn VSCode, you can use the debugging option, as the .vscode/launch.json has the right runserver arguments.

heroku config:set VARIABLE_NAME=value -a ciscorunningManually, the command would be

```

``` 

**Critical Environment Variables:**python manage.py runsslserver --settings=ic_marathon_site.$env:ENVIRONMENT

- `DATABASE_URL` - PostgreSQL connection (Heroku Postgres addon)``` 

- `AWS_ACCESS_KEY_ID` - S3 access key

- `AWS_SECRET_ACCESS_KEY` - S3 secret key# Heroku deployment

- `AWS_BUCKET_NAME` - S3 bucket name (ciscorunningaws)

- `AWS_S3_REGION_NAME` - S3 region (us-east-2)Make sure you have the Heroku CLI tool.

- `MEMCACHEDCLOUD_SERVERS` - Memcached servers

- `MEMCACHEDCLOUD_USERNAME` - Memcached usernamehttps://devcenter.heroku.com/articles/heroku-cli

- `MEMCACHEDCLOUD_PASSWORD` - Memcached password

- `DJANGO_SECRET_KEY` - Django secret keyLogin to heroku with the HEROKU_ADMIN and HEROKU_PASSWORD variables

- `STRAVA_CLIENT_ID` - Strava OAuth client ID

- `STRAVA_CLIENT_SECRET` - Strava OAuth secret``` 

- `WT_ROOMID` - WebEx Teams room IDheroku login

``` 

**View Current Config:**

```bashTo set environment variables, use the heroku config command

heroku config -a ciscorunning

`````` 

heroku config:set <variable name>=############ -a ciscorunning

#### Database Management``` 



**Run Commands:**To run bash in the app, use the command

```bash

heroku run bash -a ciscorunning``` 

heroku run python manage.py shell -a ciscorunningheroku run bash -a <name of the app>

heroku run python manage.py createsuperuser -a ciscorunning``` 

```

Since the app is already configured in Heroku (ciscorunning), there is no further configuration.

**Backup Database:**

```bashOnce the changes are committed and push to the repo, Heroku will automatically build the new app and deploy it.

heroku pg:backups:capture -a ciscorunning

heroku pg:backups:download -a ciscorunning---

```

## 🆕 New Features in 2025 Edition

#### AWS S3 Configuration

### 1. REST API with Swagger Documentation

**Bucket:** ciscorunningaws (us-east-2 region)- Full CRUD operations for profiles and workouts

- Interactive API documentation at `/api/docs/`

**Required IAM Policy:**- Integrated drf-spectacular for OpenAPI 3.0 compliance

```json- Session and Basic authentication support

{

    "Version": "2012-10-17",### 2. Beginner Freestyler Category

    "Statement": [- New category for users new to freestyle activities

        {- Mirrors the Beginner Runner → Runner progression

            "Effect": "Allow",- Separate leaderboard for fair competition

            "Action": [

                "s3:PutObject",### 3. Smart Auto-Promotion System

                "s3:GetObject",- Three detection paths prevent sandbagging

                "s3:DeleteObject",- Performance-based promotion (7km+ average)

                "s3:ListBucket",- Consistency-based promotion (15+ active days)

                "s3:GetObjectAcl",- Distance-based promotion (84km + 10 days)

                "s3:PutObjectAcl"

            ],### 4. Enhanced Profile Management

            "Resource": [- `/api/profiles/me/` endpoint for easy self-management

                "arn:aws:s3:::ciscorunningaws",- Tracks first workout date and unique workout days

                "arn:aws:s3:::ciscorunningaws/*"- One-time category change allowance

            ]- Read-only fields prevent data manipulation

        }

    ]### 5. Anti-Gaming Measures

}- Users must select "Runner" or "Freestyler" in wizard

```- Backend auto-assigns to beginner categories

- Multiple promotion triggers catch skilled athletes

**Apply Policy:**- Cannot manually set or maintain beginner status

1. Go to IAM → Users → ciscorunning

2. Add permissions → Attach policies directly### 6. Improved Leaderboards

3. Create policy with JSON above- Four separate leaderboards by category

4. Attach to user- User's category leaderboard shown first

- Beginner categories only show true beginners

#### Heroku Addons- Advanced categories show all promoted users



- **Heroku Postgres**: Essential-0 plan### 7. Database Tracking

- **Memcached Cloud**: 30MB plan- `first_workout_date`: Tracks when user started

- `workout_days_count`: Counts unique active days

#### Monitoring- `category_changed`: Tracks if user switched tracks

- `current_streak`: Consecutive workout days (resets if you skip)

**Check App Status:**- `longest_streak`: Personal best streak record

```bash- Auto-calculated metrics for promotion logic

heroku ps -a ciscorunning

```### 8. Streak Tracking & Gamification 🔥

- **Current Streak**: Tracks consecutive days with workouts

**View Recent Releases:**- **Longest Streak**: Records your personal best (never decreases)

```bash- **Automatic Calculation**: Updates on every workout save/delete

heroku releases -a ciscorunning- **Streak Badges**: Earn achievements at 7, 14, and 21-day milestones

```- **Smart Detection**: Only counts as current streak if last workout was today/yesterday



**Restart App:**### 9. Progressive Achievement Badges

```bash- **Week Warrior** (7-day streak): Complete 7 consecutive workout days

heroku restart -a ciscorunning- **Fortnight Champion** (14-day streak): Complete 14 consecutive workout days

```- **Three Week Legend** (21-day streak): Complete 21 consecutive workout days

- Badges based on longest_streak, so they're permanent achievements

---- Encourages daily participation throughout the 26-day event



## 🧪 Testing### 10. Real-Time Badge Notifications via API 🎉

- **Automatic Badge Checking**: Every workout POST checks for newly earned badges

For comprehensive testing procedures, see [TESTING.md](TESTING.md).- **Response Integration**: Newly awarded badges returned in `newly_awarded_badges` array

- **Profile Badge Display**: GET /api/profiles/me/ returns all awarded badges in `awarded_badges` array

### Quick Test Checklist- **Complete Badge Info**: Each badge includes slug, name, description, and award timestamp

- **Frontend Ready**: JSON response includes all data needed for badge displays and notifications

**User Flow:**- **Seamless UX**: Frontend can display celebratory notifications immediately after workout

- ✅ Register with Strava OAuth- **Works for All Badges**: Distance milestones (10K-168K) and streak achievements (7-21 days)

- ✅ Create profile (CEC, goal, category)

- ✅ Submit workout (distance calculated correctly)---

- ✅ View badge notifications

- ✅ Check leaderboard position## 🔧 Technical Stack

- ✅ Submit partner workout

- ✅ Confirm partner workout- **Backend**: Django 4.2.7

- ✅ Track streak progress- **REST Framework**: Django REST Framework 3.16.1

- **API Docs**: drf-spectacular 0.27.0

**Admin Flow:**- **Database**: PostgreSQL 17

- ✅ Audit workout photos- **Storage**: AWS S3 (static files, workout photos)

- ✅ View partner workout status- **Authentication**: Django AllAuth + Session/Basic Auth

- ✅ Manage user profiles- **Badges**: Django Badgify

- ✅ Check promotion logic- **Frontend**: Django Templates + CUI CSS Framework

- ✅ Monitor badge awards

---

---

## 📝 Development Notes

## 🐛 Troubleshooting

### Profile Tracking Fields

### Common IssuesThe system automatically manages these fields:

- `distance`: Sum of all workout distances (read-only)

**Issue:** Can't promote manually to advanced category- `workout_days_count`: Unique days with workouts (auto-calculated)

- **Expected**: Promotion is automatic based on performance- `first_workout_date`: Date of first workout (auto-set)

- **Solution**: Meet any of the three promotion criteria paths- `current_streak`: Consecutive days with workouts (auto-calculated)

- `longest_streak`: Personal best streak record (auto-calculated)

**Issue:** API returns "runner" but UI shows "Beginner Runner"- `category`: Current category including beginner status (auto-managed)

- **Expected**: API shows track intent, UI shows actual progression- `category_changed`: Boolean flag for track switches (auto-set)

- **Solution**: Check `actual_category` field for true status

### Workout Signals

**Issue:** Category change rejectedEvery time a workout is saved or deleted:

- **Error**: "You have already changed your category once"1. Profile distance is updated

- **Solution**: Category track can only be switched once per user2. Workout days count is recalculated

3. **Streaks are calculated** (current and longest)

**Issue:** Profile creation fails with UNIQUE constraint error4. Auto-promotion logic is evaluated

- **Cause**: User already has a profile5. **Streak badges are checked and awarded** (7, 14, 21 days)

- **Solution**: Use PATCH `/api/profiles/me/` to update instead6. Goal achievement badges are checked

7. S3 cleanup happens on deletion

**Issue:** Current streak shows 0 even though I worked out yesterday

- **Cause**: System checks if last workout was today or yesterday### Streak Calculation Logic

- **Solution**: If workout was 2+ days ago, streak has brokenThe `Profile.calculate_streaks()` method:

1. Gets all unique workout dates (ignoring time)

**Issue:** Worked out twice today but streak is still 12. Sorts dates chronologically

- **Expected**: Streak counts unique workout days, not number of workouts3. Counts consecutive days (dates that are 1 day apart)

- **Solution**: This is correct - multiple workouts same day = 1 streak day4. Tracks the longest consecutive sequence found

5. Validates current streak only if last workout was today or yesterday

**Issue:** Partner workout not giving 1.5x bonus6. Returns tuple: `(current_streak, longest_streak)`

- **Cause**: Partner hasn't confirmed yet

- **Solution**: Partner must accept request before bonus applies### API Serializer Logic

The `ProfileSerializer` handles:

**Issue:** Can't select someone as partner- Mapping user selections (runner/freestyler) to beginner categories

- **Cause**: You're in different category tracks (runner vs freestyler)- Preventing multiple category track changes

- **Solution**: Only users in same track can partner together- Returning "intent" category while tracking actual progression

- Adding `actual_category` field to show real status

**Issue:** S3 images not loading

- **Cause**: AWS credentials or IAM permissions issue---

- **Solution**: Check AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and IAM policy

## 🐛 Troubleshooting

### Getting Help

### Common Issues

For technical issues or questions:

- **Email**: gpe-reyes-marathon@cisco.com**Issue**: Can't promote manually to advanced category

- **Admin**: Sari Fernandez (sarifern@cisco.com)- **Expected**: Promotion is automatic based on performance

- **Admin**: Alfredo Prado (apradoca@cisco.com)- **Solution**: Meet any of the three promotion criteria



---**Issue**: API returns "Runner" but UI shows "Beginner Runner"

- **Expected**: API shows your track, UI shows your progression

## 📜 License- **Solution**: This is intentional - check `actual_category` field



Internal Cisco project - All rights reserved.**Issue**: Category change rejected

- **Error**: "You have already changed your category once"

---- **Solution**: Category track can only be switched once per user



## 🎯 Event Timeline**Issue**: Profile creation fails with UNIQUE constraint error

- **Cause**: User already has a profile

- **Registration Opens**: Early December 2024- **Solution**: Use PUT/PATCH `/api/profiles/me/` to update instead

- **Event Start**: December 12, 2024

- **Event End**: January 6, 2025**Issue**: My current streak shows 0 even though I worked out yesterday

- **Duration**: 26 days- **Cause**: System checks if last workout was today or yesterday

- **Target**: 168km (4 marathons)- **Solution**: If you worked out 2+ days ago, the streak has broken and resets to 0

- **Awards Ceremony**: TBD

**Issue**: My streak badge disappeared

---- **Expected**: Streak badges are based on longest_streak and never disappear

- **Solution**: Check your profile - badges are permanent once earned

## 🙏 Acknowledgments

**Issue**: I worked out twice today but streak is still 1

- **Development Team**: GPE Reyes Marathon Team- **Expected**: Streak counts unique workout days, not number of workouts

- **Framework**: Django and Django REST Framework- **Solution**: This is correct - multiple workouts on same day = 1 day for streak

- **Infrastructure**: Heroku, AWS S3

- **Authentication**: Strava API### Getting Help

- **UI Framework**: Cisco UI Kit

For technical issues or questions:

---- Email: gpe-reyes-marathon@cisco.com

- Admin: Sari Fernandez (sarifern@cisco.com)

Good luck and happy running! 🏃‍♂️💨- Admin: Alfredo Prado (apradoca@cisco.com)


---

## 📜 License

Internal Cisco project - All rights reserved.

---

## 🎯 Event Timeline

- **Registration Opens**: Early December 2024
- **Event Start**: December 12, 2024
- **Event End**: January 6, 2025
- **Duration**: 26 days
- **Awards Ceremony**: TBD

---

## 🏆 Complete Badge Guide

### Distance Badges
| Badge | Requirement | Equivalent |
|-------|-------------|------------|
| 10K Record Smashed | 10km total | Entry level |
| 21K Award Unlocked | 21km total | Half marathon |
| 42K Milestone | 42km total | Full marathon |
| 84K Milestone | 84km total | 2 marathons |
| 126K Milestone | 126km total | 3 marathons |
| 168K Milestone | 168km total | 4 marathons |
| My Milestone | Your personal goal | Custom achievement |

### Streak Badges (NEW! 🔥)
| Badge | Requirement | % of Event |
|-------|-------------|------------|
| Week Warrior | 7 consecutive days | 27% |
| Fortnight Champion | 14 consecutive days | 54% |
| Three Week Legend | 21 consecutive days | 81% |

**Pro Tip**: Combine distance and streak badges for maximum achievement! You can earn all 10 badges in one event.

---

Good luck and happy running! 🏃‍♂️💨
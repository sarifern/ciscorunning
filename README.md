# Cisco Running

Repo for Web APP Cisco Running Challenge 2025

## 🏃‍♂️ Overview

The Cisco Running Challenge is a marathon-style fitness competition running from **December 12, 2024 to January 6, 2025** (26 days). Participants can compete in two main tracks:
- **Runner Track**: Traditional running activities
- **Freestyler Track**: Various sports (cycling, swimming, hiking, etc.) converted to km equivalents

### Key Features

- 🏅 **Smart Category System**: Auto-assigns beginners and promotes based on performance
- 🚫 **Anti-Sandbagging**: Prevents skilled athletes from dominating beginner categories
- 📊 **Separate Leaderboards**: Beginner Runner, Runner, Beginner Freestyler, Freestyler
- 🎯 **Goal Tracking**: Personal distance goals with achievement badges
- 🔐 **REST API**: Full CRUD operations with authentication
- 📝 **Swagger Documentation**: Interactive API docs at `/api/docs/`
- 🏆 **Badge System**: Distance achievements (10K-168K) + Streak badges (7, 14, 21 days)
- 🔥 **Streak Tracking**: Automatic tracking of current and longest workout streaks

---

#### 2. Profile Management

- [Architecture](#architecture)
- [Installation](#installation)
  - [Mac Installation](#installation-in-mac)
  - [Windows Installation](#installation-in-windows)
- [API Documentation](#api-documentation)
- [Modern Frontend Integration](#modern-frontend-integration)
- [Streak Tracking System](#streak-tracking-system)
- [Category System](#category-system)
- [Running the Project](#running-the-project)
- [Deployment](#heroku-deployment)

---

## Architecture

### 🏗️ Headless Backend + Modern Frontend

The Cisco Running application follows a modern **headless CMS architecture**:

```
┌─────────────────────────────────────────────────────────┐
│                   Modern Frontend                        │
│          (React/Vue/Svelte/Next.js/etc.)                │
│                                                          │
│  • Strava OAuth Integration                             │
│  • Real-time Badge Notifications                        │
│  • Progressive Web App (PWA)                            │
│  • Responsive Design                                     │
└─────────────────────────────────────────────────────────┘
                         ↕ HTTP/REST
┌─────────────────────────────────────────────────────────┐
│              Django REST API (Headless)                  │
│                                                          │
│  • Token Authentication                                  │
│  • Auto-calculated Metrics                              │
│  • Badge System                                          │
│  • Anti-Sandbagging Logic                               │
│  • Swagger Documentation                                 │
└─────────────────────────────────────────────────────────┘
                         ↕
┌─────────────────────────────────────────────────────────┐
│          Django Admin (Auditing/Legacy)                  │
│                                                          │
│  • Workout Auditing (is_audited flag)                   │
│  • User Management                                       │
│  • Manual Badge Awards                                   │
│  • Database Management                                   │
└─────────────────────────────────────────────────────────┘
```

### Key Architectural Decisions

1. **Headless API**: Django serves only JSON via REST API
2. **Token Auth**: Modern frontends use token-based authentication
3. **CORS Enabled**: Cross-origin requests allowed for frontend apps
4. **Admin Preserved**: Django admin remains for auditing and management
5. **Backward Compatible**: Legacy Django templates still work but deprecated

---

## Modern Frontend Integration

### 🚀 Quick Start for Frontend Developers

#### 1. Authentication Flow (To Be Implemented)

Authentication will be handled by your modern frontend. The backend provides:
- Token-based authentication via DRF
- Profile management endpoints
- Workout tracking endpoints

**Basic API Usage:**
```javascript
// Once you have a token (from your auth system)
const apiRequest = (url, options = {}) => {
  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Token ${your_token_here}`,
      'Content-Type': 'application/json'
    }
  });
};
```

#### 2. Complete User Flow

```javascript
// A. Check if user has profile
const checkProfile = async () => {
  try {
    const response = await apiRequest('https://ciscorunning.herokuapp.com/api/profiles/me/');
    if (response.ok) {
      const profile = await response.json();
      return profile;
    }
  } catch (error) {
    return null; // No profile exists
  }
};

// B. Create profile if needed
const createProfile = async (profileData) => {
  const response = await apiRequest('https://ciscorunning.herokuapp.com/api/profiles/me/', {
    method: 'POST',
    body: JSON.stringify({
      cec: profileData.cec,
      user_goal_km: profileData.goalKm,
      category: profileData.category // 'runner' or 'freestyler'
    })
  });
  return response.json();
};

// C. Submit workout and get badge notifications
const submitWorkout = async (workoutData) => {
  const formData = new FormData();
  formData.append('belongs_to', profile.id);
  formData.append('distance', workoutData.distance);
  formData.append('date_time', workoutData.dateTime);
  formData.append('time', workoutData.duration);
  formData.append('sport', workoutData.sportId);
  formData.append('intensity', workoutData.intensity);
  formData.append('photo_evidence', workoutData.photo);
  
  const response = await fetch('https://ciscorunning.herokuapp.com/api/workouts/', {
    method: 'POST',
    headers: {
      'Authorization': `Token ${localStorage.getItem('authToken')}`
    },
    body: formData
  });
  
  const result = await response.json();
  
  // Check for newly awarded badges
  if (result.newly_awarded_badges && result.newly_awarded_badges.length > 0) {
    result.newly_awarded_badges.forEach(badge => {
      showBadgeNotification(badge); // Your UI notification function
    });
  }
  
  return result;
};
```

#### 3. Profile Management

```javascript
// Get profile with all badges
const getProfile = async () => {
  const response = await apiRequest('https://ciscorunning.herokuapp.com/api/profiles/me/');
  const profile = await response.json();
  
  /*
  Profile structure:
  {
    user: "johndoe",
    cec: "johndoe",
    category: "runner",  // Intent (runner or freestyler)
    actual_category: "Beginner Runner",  // Current progression
    distance: "25.50",
    user_goal_km: "42.00",
    current_streak: 7,
    longest_streak: 12,
    workout_days_count: 18,
    awarded_badges: [
      {
        slug: "10K",
        name: "10K Record Smashed",
        description: "Congrats! You set a new 10k personal record",
        awarded_at: "2024-12-18T10:30:00Z"
      },
      // ... more badges
    ]
  }
  */
  
  return profile;
};

// Update goal
const updateGoal = async (newGoalKm) => {
  const response = await apiRequest('https://ciscorunning.herokuapp.com/api/profiles/me/', {
    method: 'PATCH',
    body: JSON.stringify({ user_goal_km: newGoalKm })
  });
  return response.json();
};

// Switch category (one-time only)
const switchCategory = async (newCategory) => {
  const response = await apiRequest('https://ciscorunning.herokuapp.com/api/profiles/me/', {
    method: 'PATCH',
    body: JSON.stringify({ category: newCategory }) // 'runner' or 'freestyler'
  });
  return response.json();
};
```

#### 4. Badge Display

```javascript
// Display badge gallery
const displayBadges = (profile) => {
  const allBadges = [
    { slug: '10K', locked: true },
    { slug: '21K', locked: true },
    { slug: '42K', locked: true },
    { slug: '84K', locked: true },
    { slug: '126K', locked: true },
    { slug: '168K', locked: true },
    { slug: 'ownK', locked: true },
    { slug: '7day-streak', locked: true },
    { slug: '14day-streak', locked: true },
    { slug: '21day-streak', locked: true },
  ];
  
  // Mark earned badges as unlocked
  profile.awarded_badges.forEach(earnedBadge => {
    const badge = allBadges.find(b => b.slug === earnedBadge.slug);
    if (badge) {
      badge.locked = false;
      badge.name = earnedBadge.name;
      badge.description = earnedBadge.description;
      badge.awarded_at = earnedBadge.awarded_at;
    }
  });
  
  return allBadges;
};

// Calculate progress
const calculateProgress = (profile) => {
  const totalBadges = 10;
  const earnedBadges = profile.awarded_badges.length;
  const percentage = (earnedBadges / totalBadges) * 100;
  
  return {
    earned: earnedBadges,
    total: totalBadges,
    percentage: Math.round(percentage)
  };
};
```

### 🔒 CORS Configuration

CORS is pre-configured to allow requests from any origin during development. For production, you should restrict allowed origins in `local_settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-app.com",
    "https://your-frontend-app.vercel.app",
]
```

### 📱 Strava OAuth Integration

The backend already has Strava OAuth configured via Django Allauth. For your modern frontend:

1. **Backend Handles OAuth**: Use the existing `/accounts/strava/login/` endpoint
2. **Redirect Flow**: Configure Strava to redirect to your frontend
3. **Token Exchange**: Frontend receives token and uses it for API calls

---

## API Documentation

### 🔗 Base URL
- **Local**: `https://localhost:8000/api/`
- **Production**: `https://ciscorunning.herokuapp.com/api/`

### 📚 Interactive Documentation
- **Swagger UI**: `/api/docs/` - Full interactive API documentation
- **ReDoc**: `/api/redoc/` - Alternative documentation view
- **OpenAPI Schema**: `/api/schema/` - Raw OpenAPI 3.0 schema

### 🔐 Authentication

All API endpoints require authentication. The API uses token-based authentication.

**Supported Methods:**
- **Token Authentication**: Use REST Framework tokens (recommended for API clients)
- **Session Authentication**: Use Django's session system (for browsable API)
- **Basic Authentication**: Username/password with each request (for testing only)

**Note**: Authentication details will be finalized based on your frontend OAuth implementation.

#### Using the Token

Include the token in the `Authorization` header of all API requests:

```http
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Example with fetch:**
```javascript
const response = await fetch('https://ciscorunning.herokuapp.com/api/profiles/me/', {
  headers: {
    'Authorization': 'Token your-token-here',
    'Content-Type': 'application/json'
  }
});
```

**Example with axios:**
```javascript
axios.defaults.headers.common['Authorization'] = 'Token your-token-here';
```

### 📌 Endpoints

#### Profile Management

##### `GET /api/profiles/me/`
Get your own profile information.

**Response Example:**
```json
{
  "user": "john.doe",
  "user_goal_km": "42.00",
  "category": "runner",
  "actual_category": "Beginner Runner",
  "cec": "johndoe",
  "avatar": "https://ciscorunning2023.s3.us-east-1.amazonaws.com/static/img/user.png",
  "distance": "15.50",
  "category_changed": false,
  "current_streak": 5,
  "longest_streak": 12,
  "workout_days_count": 18,
  "awarded_badges": [
    {
      "slug": "10K",
      "name": "10K Record Smashed",
      "description": "Congrats! You set a new 10k personal record",
      "awarded_at": "2024-12-18T10:30:00Z"
    },
    {
      "slug": "7day-streak",
      "name": "Week Warrior",
      "description": "Amazing! You completed 7 consecutive days of workouts!",
      "awarded_at": "2024-12-20T08:15:00Z"
    }
  ]
}
```

**Notes:**
- `category`: Shows your selected track (runner or freestyler)
- `actual_category`: Shows your current progression (Beginner Runner → Runner)
- `distance`: Auto-calculated from workouts (read-only)
- `current_streak`: Consecutive days with workouts (resets if you skip a day)
- `longest_streak`: Your personal best streak record
- `workout_days_count`: Total unique days you've worked out
- `awarded_badges`: Array of all badges you've earned (with full details)

##### `POST /api/profiles/me/`
Create your profile.

**Request Body:**
```json
{
  "cec": "johndoe",
  "user_goal_km": "42.00",
  "category": "runner"
}
```

**Notes:**
- You can only select `"runner"` or `"freestyler"`
- Backend automatically assigns you to beginner category
- You'll be auto-promoted based on performance

##### `PUT /api/profiles/me/`
Update your entire profile (or create if doesn't exist).

**Request Body:**
```json
{
  "cec": "johndoe",
  "user_goal_km": "84.00",
  "category": "runner"
}
```

##### `PATCH /api/profiles/me/`
Partially update your profile.

**Request Body (any fields):**
```json
{
  "user_goal_km": "84.00"
}
```

**Notes:**
- Can update `user_goal_km` unlimited times
- Can only change `category` (runner ↔ freestyler) **once**
- Cannot manually change beginner status (auto-managed)

##### `DELETE /api/profiles/me/`
Delete your profile and all associated workouts.

**Response:** `204 No Content`

**Warning:** This action cannot be undone. All workouts will be permanently deleted.

#### Workout Management

##### `GET /api/workouts/`
List all your workouts.

**Response Example:**
```json
[
  {
    "belongs_to": 1,
    "distance": "5.00",
    "date_time": "2024-12-15T08:30:00Z",
    "time": "00:30:00",
    "sport": 1,
    "intensity": 2,
    "photo_evidence": "https://..."
  }
]
```

##### `POST /api/workouts/`
Create a new workout.

**Request Body:**
```json
{
  "belongs_to": 1,
  "distance": "5.00",
  "date_time": "2024-12-15T08:30:00Z",
  "time": "00:30:00",
  "sport": 1,
  "intensity": 2,
  "photo_evidence": "<file>"
}
```

**Response Example:**
```json
{
  "belongs_to": 1,
  "distance": "5.00",
  "date_time": "2024-12-15T08:30:00Z",
  "time": "00:30:00",
  "sport": 1,
  "intensity": 2,
  "photo_evidence": "https://...",
  "newly_awarded_badges": [
    {
      "slug": "7day-streak",
      "name": "Week Warrior",
      "description": "Amazing! You completed 7 consecutive days of workouts!",
      "awarded_at": "2024-12-15T08:30:00Z"
    }
  ]
}
```

**Notes:**
- `newly_awarded_badges`: Array of badges earned with this workout (empty if none)
- Badges are checked automatically after workout is saved
- Distance and streak metrics are updated via signals
- Frontend can display badge notifications based on this response

---

## Streak Tracking System

### 🔥 How Streaks Work

The system automatically tracks your workout consistency through two key metrics:

#### Current Streak
- **Definition**: Number of consecutive days with at least one workout
- **Behavior**: Resets to 0 if you skip a day
- **Validation**: Only counts if your last workout was today or yesterday
- **Example**: Work out Mon-Tue-Wed-Thu-Fri = 5-day current streak

#### Longest Streak
- **Definition**: Your personal best consecutive workout streak
- **Behavior**: Never decreases, only updates when you break your record
- **Used For**: Awarding permanent achievement badges
- **Example**: If you had a 12-day streak in week 1, that's your longest streak even if current streak is 3

### 🏆 Streak Badges

Earn progressive achievements based on your **longest streak**:

| Badge | Requirement | Description |
|-------|-------------|-------------|
| **Week Warrior** 🏆 | 7 consecutive days | Complete 7 days in a row |
| **Fortnight Champion** 🎖️ | 14 consecutive days | Complete 14 days in a row |
| **Three Week Legend** 🏅 | 21 consecutive days | Complete 21 days in a row (81% of event!) |

**Why longest streak?** Because we want to reward your achievements permanently. Once earned, streak badges stay in your profile forever!

### 📊 Streak Examples

**Perfect Dedication:**
```
Days 1-7: Workout every day → Week Warrior badge earned ✓
Days 8-14: Continue → Fortnight Champion badge earned ✓
Days 15-21: Continue → Three Week Legend badge earned ✓
Current: 21-day streak | Longest: 21 days
```

**Comeback Story:**
```
Days 1-12: Workout every day → Longest: 12 days
Day 13: Skip workout → Current streak resets to 0
Days 14-20: Workout every day → Current: 7 days | Longest: still 12
Continue to Day 27 → Current: 14 days | Longest: 14 days (new record!)
```

**Consistent Participant:**
```
Pattern: Workout Mon-Fri, rest weekends
Week 1: 5-day streak → breaks on Saturday
Week 2: 5-day streak → breaks on Saturday
Week 3: 5-day streak → breaks on Saturday
Result: Longest streak is 5 days (no badges yet)
```

### 🎯 Strategy Tips

- **Daily commitment wins**: Even a short 2km run counts for your streak
- **Plan ahead**: The event is 26 days, so 21-day badge leaves 5 rest days
- **Mixed activities**: Freestylers can alternate sports to avoid burnout
- **Early morning**: Log workouts early to maintain streak pressure-free

---

## Category System

### 🎯 How Categories Work

#### User Experience
When you sign up, you choose:
- **Runner** - Traditional running
- **Freestyler** - Various sports activities

#### Behind the Scenes
The system automatically:
1. Assigns you to the **beginner version** of your chosen category
2. Tracks your performance across multiple metrics
3. Auto-promotes you when you demonstrate skill/consistency

### 📊 The Four Categories

| Category | Badge | Description |
|----------|-------|-------------|
| **Beginner Runner** | 🏃 | New to running, < 84km or < 10 days |
| **Runner** | 🏃🏃 | Experienced runners, promoted automatically |
| **Beginner Freestyler** | 🚴 | New to varied sports, < 84km or < 10 days |
| **Freestyler** | 🚴🚴 | Experienced athletes, promoted automatically |

### 🚀 Auto-Promotion System

You are automatically promoted when you meet **ANY** of these criteria:

#### Path 1: High Distance + Consistency
- **84km** total distance
- **10+ unique workout days**
- Example: 8.4km/day for 10 days

#### Path 2: Performance Level Detection (Anti-Sandbagging) ⭐
- **5+ workouts** averaging **7km+ each**
- Example: 10km, 8km, 9km, 7km, 11km = Promoted after 5th workout
- **Prevents skilled runners from staying in beginner category**

#### Path 3: Super Consistent Participation
- **42km** total distance
- **15+ unique workout days**
- Example: 2.8km/day for 15 days

### 🛡️ Anti-Sandbagging Protection

**Problem:** In previous editions, skilled runners would sign up as "Beginner Runner" and dominate the leaderboard while staying just under promotion thresholds.

**Solution:** The system now detects skilled athletes in multiple ways:

| Sandbagging Strategy | Detection Method | Result |
|---------------------|------------------|---------|
| "Run 83km and stop" | Averaging 8km+ per workout → Path 2 | ✅ Promoted |
| "Run big then stop" | 50km in 5 workouts = 10km avg → Path 2 | ✅ Promoted |
| "Many small runs" | 45km over 16 days → Path 3 | ✅ Promoted |
| True beginner | 25km over 8 days, 3km avg | ❌ Stays beginner |

### 📈 Progression Examples

**Skilled Runner (Auto-Promoted Fast):**
```
Day 1: 10km → Day 2: 9km → Day 3: 11km → Day 4: 8km → Day 5: 12km
Total: 50km over 5 days, avg 10km/workout
Result: AUTO-PROMOTED to Runner (Path 2 triggered)
```

**Dedicated Beginner (Eventually Promoted):**
```
Week 1: 3km x 7 days = 21km
Week 2: 3km x 7 days = 21km  
Week 3: 3km x 2 days = 6km
Total: 48km over 16 days
Result: AUTO-PROMOTED to Runner (Path 3 triggered)
```

**True Beginner (Stays in Category):**
```
Sporadic participation: 3km, 4km, 2km, 5km, 3km over 8 days
Total: 17km over 8 days
Result: Stays in Beginner Runner category
```

### 🔄 Category Changes

- You can switch tracks (Runner ↔ Freestyler) **only once**
- If you switch, you start at the beginner level of the new track
- Auto-promotion rules apply to your new category
- Example: "Beginner Runner" → switch to Freestyler → becomes "Beginner Freestyler"

---

## Installation in MAC

0. Install VSCode and VSCode python plugin.

1. Clone the project.

2. Set up your git global config

``` 
git config --global user.name "<Your name>"     
git config --global user.email "<Your email>"
``` 

3. Edit your hostnames file and add the following

``` 
#in /etc/hosts
#add

127.0.0.1         www.lurifern.com
``` 

4. Install PostgreSQL 

``` 
brew reinstall openssl
export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/
brew install postgresql
``` 

4.1 Add the path out of 

``` 
which pg_config
``` 
to your PATH declaration in your shell profile (for example ~/.bash_profile)

``` 
export PATH=$PATH:/usr/local/bin/pg_config
``` 
5. Install Xcode tools

``` 
xcode-select --install
``` 

6. Create a virtual environment for Python 3.11.

``` 
python3.11 -m virtualenv env
``` 

6. a. Activate your environment

``` 
source env/bin/activate
```

7. install the packages

``` 
env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2==2.8.3
pip install -r requirements.txt 
``` 

8. Please add the .secrets and local-settings.py files. Ask for them to the admins lurifern@cisco.com
Set .secrets at the parent folder, and local-settings.py under the ic_marathon_site folder

8.1 Execute

``` 
export $(grep -v '^#' .secrets | xargs)
``` 

9. Collect static files

``` 
python manage.py collectstatic --settings=ic_marathon_site.local_settings
``` 

10. Setup the badging system

``` 
python manage.py makemigrations badgify --settings=ic_marathon_site.local_settings
python manage.py migrate badgify --settings=ic_marathon_site.local_settings
python manage.py badgify_sync badges --settings=ic_marathon_site.local_settings
python manage.py badgify_reset --settings=ic_marathon_site.local_settings
python manage.py badgify_sync awards --disable-signals --settings=ic_marathon_site.local_settings
python manage.py badgify_sync counts --settings=ic_marathon_site.local_settings
``` 

11. Make the DB migrations

``` 
python manage.py makemigrations --settings=ic_marathon_site.local_settings
python manage.py migrate --settings=ic_marathon_site.local_settings
```

12. Run the initialize_badges.py script

``` 
python manage.py shell < initialize_badges.py  --settings=ic_marathon_site.local_settings
``` 

13. Create a superuser

``` 
python manage.py createsuperuser --settings=ic_marathon_site.local_settings
```  
# Installation in Windows

0. Install VSCode and VSCode python plugin. Install Python 3.11.6

1. Clone the project.

2. Set up your git global config

``` 
git config user.name "<Your name>"     
git config user.email "<Your email>"
``` 

3. Edit your hostnames file in Notepad(run as administrator) and add the following

``` 
#in C:\Windows\System32\drivers\etc\hosts
#add

127.0.0.1 www.apradofern.com
``` 

4. Install PostgreSQL 17.X https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

Set the password for the superuser (postgres).

5. Install Microsoft C++ Build Tools https://visualstudio.microsoft.com/visual-cpp-build-tools/
Pick Desktop development with C++, and deselect the optional packages. Only install the included packages:
C++ Build Tools core features
C++ 2022 Redistributable Update
C++ core desktop features

6. Create a virtual environment for Python 3.11.6 using VSCode (venv)

``` 
pip install virtualenv
virtualenv .venv --python=3.11
``` 
To activate the environment, use the following command:
``` 
PS C:\Users\sarifern\CX\ciscorunning> .\venv\Scripts\activate
(venv) PS C:\Users\sarifern\CX\ciscorunning> 
``` 
Install requirements
``` 
(venv) PS C:\Users\sarifern\CX\ciscorunning> pip install -r requirements.txt
```

Upgrade setup tools
``` 
(venv) PS C:\Users\sarifern\CX\ciscorunning> pip install -U setuptools
```

7. Please add the .secrets and local-settings.py files. Ask for them to the admins Sari Fernandez (sarifern@cisco.com) and Alfredo Prado (apradoca@cisco.com)
Set .secrets at the parent folder, and local-settings.py under the ic_marathon_site folder

8.1 Execute the following lines

``` 
get-content .secrets | foreach {
     $name, $value = $_.split('=')
     set-content env:\$name $value
 }
$env:ENVIRONMENT='local_settings'
``` 

9. Collect static files (only if the bucket was recently created)

``` 
python manage.py collectstatic --settings=ic_marathon_site.$env:ENVIRONMENT
``` 

10. Setup the badging system

``` 
python manage.py makemigrations badgify --settings=ic_marathon_site.$env:ENVIRONMENT
python manage.py migrate badgify --settings=ic_marathon_site.$env:ENVIRONMENT
python manage.py badgify_sync badges --settings=ic_marathon_site.$env:ENVIRONMENT
python manage.py badgify_reset --settings=ic_marathon_site.$env:ENVIRONMENT
python manage.py badgify_sync awards --disable-signals --settings=ic_marathon_site.$env:ENVIRONMENT
python manage.py badgify_sync counts --settings=ic_marathon_site.$env:ENVIRONMENT
``` 

11. Make the DB migrations

``` 
python manage.py makemigrations --settings=ic_marathon_site.$env:ENVIRONMENT
python manage.py migrate --settings=ic_marathon_site.$env:ENVIRONMENT
```

12. Run the initialize_badges.py script

This creates all achievement badges in the database:
- **Distance Badges**: 10K, 21K, 42K, 84K, 126K, 168K, ownK (personal goal)
- **Streak Badges**: 7-day (Week Warrior), 14-day (Fortnight Champion), 21-day (Three Week Legend)

``` 
python manage.py shell  --settings=ic_marathon_site.$env:ENVIRONMENT
>>> exec(open('initialize_badges.py').read())
>>> exit()
``` 

13. Create a superuser

``` 
python manage.py createsuperuser --settings=ic_marathon_site.$env:ENVIRONMENT
```  

14. Create a cache table
``` 
python manage.py createcachetable --settings=ic_marathon_site.$env:ENVIRONMENT
``` 
# Running the project locally

In VSCode, you can use the debugging option, as the .vscode/launch.json has the right runserver arguments.
Manually, the command would be

``` 
python manage.py runsslserver --settings=ic_marathon_site.$env:ENVIRONMENT
``` 

# Heroku deployment

Make sure you have the Heroku CLI tool.

https://devcenter.heroku.com/articles/heroku-cli

Login to heroku with the HEROKU_ADMIN and HEROKU_PASSWORD variables

``` 
heroku login
``` 

To set environment variables, use the heroku config command

``` 
heroku config:set <variable name>=############ -a ciscorunning
``` 

To run bash in the app, use the command

``` 
heroku run bash -a <name of the app>
``` 

Since the app is already configured in Heroku (ciscorunning), there is no further configuration.

Once the changes are committed and push to the repo, Heroku will automatically build the new app and deploy it.

---

## 🆕 New Features in 2025 Edition

### 1. REST API with Swagger Documentation
- Full CRUD operations for profiles and workouts
- Interactive API documentation at `/api/docs/`
- Integrated drf-spectacular for OpenAPI 3.0 compliance
- Session and Basic authentication support

### 2. Beginner Freestyler Category
- New category for users new to freestyle activities
- Mirrors the Beginner Runner → Runner progression
- Separate leaderboard for fair competition

### 3. Smart Auto-Promotion System
- Three detection paths prevent sandbagging
- Performance-based promotion (7km+ average)
- Consistency-based promotion (15+ active days)
- Distance-based promotion (84km + 10 days)

### 4. Enhanced Profile Management
- `/api/profiles/me/` endpoint for easy self-management
- Tracks first workout date and unique workout days
- One-time category change allowance
- Read-only fields prevent data manipulation

### 5. Anti-Gaming Measures
- Users must select "Runner" or "Freestyler" in wizard
- Backend auto-assigns to beginner categories
- Multiple promotion triggers catch skilled athletes
- Cannot manually set or maintain beginner status

### 6. Improved Leaderboards
- Four separate leaderboards by category
- User's category leaderboard shown first
- Beginner categories only show true beginners
- Advanced categories show all promoted users

### 7. Database Tracking
- `first_workout_date`: Tracks when user started
- `workout_days_count`: Counts unique active days
- `category_changed`: Tracks if user switched tracks
- `current_streak`: Consecutive workout days (resets if you skip)
- `longest_streak`: Personal best streak record
- Auto-calculated metrics for promotion logic

### 8. Streak Tracking & Gamification 🔥
- **Current Streak**: Tracks consecutive days with workouts
- **Longest Streak**: Records your personal best (never decreases)
- **Automatic Calculation**: Updates on every workout save/delete
- **Streak Badges**: Earn achievements at 7, 14, and 21-day milestones
- **Smart Detection**: Only counts as current streak if last workout was today/yesterday

### 9. Progressive Achievement Badges
- **Week Warrior** (7-day streak): Complete 7 consecutive workout days
- **Fortnight Champion** (14-day streak): Complete 14 consecutive workout days
- **Three Week Legend** (21-day streak): Complete 21 consecutive workout days
- Badges based on longest_streak, so they're permanent achievements
- Encourages daily participation throughout the 26-day event

### 10. Real-Time Badge Notifications via API 🎉
- **Automatic Badge Checking**: Every workout POST checks for newly earned badges
- **Response Integration**: Newly awarded badges returned in `newly_awarded_badges` array
- **Profile Badge Display**: GET /api/profiles/me/ returns all awarded badges in `awarded_badges` array
- **Complete Badge Info**: Each badge includes slug, name, description, and award timestamp
- **Frontend Ready**: JSON response includes all data needed for badge displays and notifications
- **Seamless UX**: Frontend can display celebratory notifications immediately after workout
- **Works for All Badges**: Distance milestones (10K-168K) and streak achievements (7-21 days)

---

## 🔧 Technical Stack

- **Backend**: Django 4.2.7
- **REST Framework**: Django REST Framework 3.16.1
- **API Docs**: drf-spectacular 0.27.0
- **Database**: PostgreSQL 17
- **Storage**: AWS S3 (static files, workout photos)
- **Authentication**: Django AllAuth + Session/Basic Auth
- **Badges**: Django Badgify
- **Frontend**: Django Templates + CUI CSS Framework

---

## 📝 Development Notes

### Profile Tracking Fields
The system automatically manages these fields:
- `distance`: Sum of all workout distances (read-only)
- `workout_days_count`: Unique days with workouts (auto-calculated)
- `first_workout_date`: Date of first workout (auto-set)
- `current_streak`: Consecutive days with workouts (auto-calculated)
- `longest_streak`: Personal best streak record (auto-calculated)
- `category`: Current category including beginner status (auto-managed)
- `category_changed`: Boolean flag for track switches (auto-set)

### Workout Signals
Every time a workout is saved or deleted:
1. Profile distance is updated
2. Workout days count is recalculated
3. **Streaks are calculated** (current and longest)
4. Auto-promotion logic is evaluated
5. **Streak badges are checked and awarded** (7, 14, 21 days)
6. Goal achievement badges are checked
7. S3 cleanup happens on deletion

### Streak Calculation Logic
The `Profile.calculate_streaks()` method:
1. Gets all unique workout dates (ignoring time)
2. Sorts dates chronologically
3. Counts consecutive days (dates that are 1 day apart)
4. Tracks the longest consecutive sequence found
5. Validates current streak only if last workout was today or yesterday
6. Returns tuple: `(current_streak, longest_streak)`

### API Serializer Logic
The `ProfileSerializer` handles:
- Mapping user selections (runner/freestyler) to beginner categories
- Preventing multiple category track changes
- Returning "intent" category while tracking actual progression
- Adding `actual_category` field to show real status

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: Can't promote manually to advanced category
- **Expected**: Promotion is automatic based on performance
- **Solution**: Meet any of the three promotion criteria

**Issue**: API returns "Runner" but UI shows "Beginner Runner"
- **Expected**: API shows your track, UI shows your progression
- **Solution**: This is intentional - check `actual_category` field

**Issue**: Category change rejected
- **Error**: "You have already changed your category once"
- **Solution**: Category track can only be switched once per user

**Issue**: Profile creation fails with UNIQUE constraint error
- **Cause**: User already has a profile
- **Solution**: Use PUT/PATCH `/api/profiles/me/` to update instead

**Issue**: My current streak shows 0 even though I worked out yesterday
- **Cause**: System checks if last workout was today or yesterday
- **Solution**: If you worked out 2+ days ago, the streak has broken and resets to 0

**Issue**: My streak badge disappeared
- **Expected**: Streak badges are based on longest_streak and never disappear
- **Solution**: Check your profile - badges are permanent once earned

**Issue**: I worked out twice today but streak is still 1
- **Expected**: Streak counts unique workout days, not number of workouts
- **Solution**: This is correct - multiple workouts on same day = 1 day for streak

### Getting Help

For technical issues or questions:
- Email: gpe-reyes-marathon@cisco.com
- Admin: Sari Fernandez (sarifern@cisco.com)
- Admin: Alfredo Prado (apradoca@cisco.com)

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
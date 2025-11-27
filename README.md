# Cisco Running Challenge 2025# Cisco Running Challenge 2025



🏃‍♂️ **Marathon-Style Fitness Competition** | December 12, 2024 - January 6, 2025 (26 Days)🏃‍♂️ **Marathon-Style Fitness Competition** | December 12, 2024 - January 6, 2025 (26 Days)



[![Python](https://img.shields.io/badge/Python-3.11.6-blue.svg)](https://python.org)[![Python](https://img.shields.io/badge/Python-3.11.6-blue.svg)](https://python.org)

[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://djangoproject.com)[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://djangoproject.com)

[![License](https://img.shields.io/badge/License-Cisco_Internal-red.svg)](LICENSE)[![License](https://img.shields.io/badge/License-Cisco_Internal-red.svg)](LICENSE)



A Django-based web application for tracking and gamifying fitness activities during Cisco's annual running challenge. Participants compete in two tracks (Runner and Freestyler) with automatic category assignment, badge achievements, and streak tracking.---



---## 📋 Table of Contents



## 📋 Table of Contents- [Overview](#overview)

- [Key Features](#key-features)

- [Overview](#overview)- [Architecture](#architecture)

- [Key Features](#key-features)- [Quick Start](#quick-start)

- [Architecture](#architecture)- [Installation](#installation)

- [Installation](#installation)  - [Mac Installation](#installation-mac)

  - [Prerequisites](#prerequisites)  - [Windows Installation](#installation-windows)

  - [Mac Installation](#mac-installation)- [Running Locally](#running-locally)

  - [Windows Installation](#windows-installation)- [API Documentation](#api-documentation)

- [Running Locally](#running-locally)- [Partner Workouts](#partner-workouts)

- [Badge System](#badge-system)- [Badge System](#badge-system)

- [Category System](#category-system)- [Category System](#category-system)

- [Partner Workouts](#partner-workouts)- [Deployment](#deployment)

- [Deployment](#deployment)- [Testing](#testing)

- [Environment Variables](#environment-variables)- [Troubleshooting](#troubleshooting)

- [Testing](#testing)- [License](#license)

- [Troubleshooting](#troubleshooting)

- [License](#license)---



---## 🏃‍♂️ Overview



## 🏃‍♂️ OverviewThe Cisco Running Challenge is a gamified fitness competition where participants compete in two main tracks:



The Cisco Running Challenge is a gamified fitness competition where participants compete in two main tracks:- **Runner Track**: Traditional running activities

- **Freestyler Track**: Various sports (cycling, swimming, hiking, etc.) converted to km equivalents

- **Runner Track**: Traditional running activities

- **Freestyler Track**: Various sports (cycling, swimming, hiking, etc.) converted to km equivalents### Event Details



### Event Details- **Start Date**: December 12, 2024



- **Duration**: December 12, 2024 - January 6, 2025 (26 days)- **End Date**: January 6, 2025### 🏗️ Headless Backend + Modern Frontend

- **Goal**: Complete a marathon-equivalent distance (42.195 km) or personal goal

- **Competition**: Four separate leaderboards for fair competition- **Duration**: 26 days

- **Rewards**: Achievement badges for distance milestones and consecutive workout streaks

- **Target**: 168km (equivalent to 4 marathons)The Cisco Running application follows a modern **headless CMS architecture**:

---

- **Awards**: Multiple distance and streak achievement badges

## ✨ Key Features

```

### 🏅 Smart Category System

---┌─────────────────────────────────────────────────────────┐

- **Auto-Assignment**: New users automatically assigned to "Beginner" categories

- **Anti-Sandbagging**: System detects skilled athletes and promotes them automatically│                   Modern Frontend                        │

- **Four Categories**: Beginner Runner, Runner, Beginner Freestyler, Freestyler

- **Fair Competition**: Separate leaderboards prevent experienced athletes from dominating beginner categories## 🎯 Key Features│          (React/Vue/Svelte/Next.js/etc.)                │



### 🏆 Achievement Badges│                                                          │



- **Distance Badges**: 10K, 21K, 42K, 84K, 126K, 168K, Personal Goal### 🏅 Smart Category System│  • Strava OAuth Integration                             │

- **Streak Badges**: 7-day, 14-day, 21-day consecutive workout achievements

- **Automatic Awards**: Real-time badge checking on every workout submission- **Auto-Assignment**: Everyone starts as a beginner│  • Real-time Badge Notifications                        │

- **Permanent**: Once earned, badges are never lost

- **Auto-Promotion**: System detects and promotes skilled athletes based on performance│  • Progressive Web App (PWA)                            │

### 🔥 Streak Tracking

- **Anti-Sandbagging**: Prevents gaming the system with multiple detection methods│  • Responsive Design                                     │

- **Current Streak**: Tracks consecutive days with workouts

- **Longest Streak**: Records personal best (never decreases)- **Four Categories**: Beginner Runner, Runner, Beginner Freestyler, Freestyler└─────────────────────────────────────────────────────────┘

- **Smart Detection**: Resets if you skip a day

- **Gamification**: Encourages daily participation                         ↕ HTTP/REST



### 🤝 Partner Workouts### 🤝 Partner Workouts┌─────────────────────────────────────────────────────────┐



- **Bonus Distance**: Work out with registered partner for 10% bonus- **1.5x Distance Bonus**: Train with a partner and earn 50% bonus distance│              Django REST API (Headless)                  │

- **Expiration**: 72-hour window to claim bonus

- **Dual Tracking**: Both partners receive bonus distance- **Same Category Required**: Partners must be in the same track (both runners or both freestylers)│                                                          │

- **Verification**: Photo evidence required

- **Confirmation System**: Partner must confirm before bonus is applied│  • Token Authentication                                  │

### 📊 Separate Leaderboards- **Dual Tracking**: Both partners get the bonus distance



- Four distinct leaderboards for fair competition### 🏆 Achievement Badges

- Real-time ranking updates

- Position tracking within your category- **Distance Badges**: 10K, 21K, 42K, 84K, 126K, 168K, Personal Goal

- Distance progress visualization- **Streak Badges**: 7-day, 14-day, 21-day consecutive workout achievements

- **Automatic Awards**: Real-time badge checking on every workout submission

### 🔐 Authentication- **Permanent**: Once earned, badges are never lost



- **Strava OAuth**: Login with your Strava account### 🔥 Streak Tracking

- **Profile Sync**: Automatic profile data from Strava

- **Secure**: Token-based authentication- **Current Streak**: Tracks consecutive days with workouts

- **Avatar Support**: AWS S3 storage for profile pictures- **Longest Streak**: Records personal best (never decreases)

- **Smart Detection**: Resets if you skip a day

---- **Gamification**: Encourages daily participation



## 🏗️ Architecture### 🔐 REST API



### Django Monolith Application- **Full CRUD Operations**: Complete API for profiles and workouts

- **Token Authentication**: Secure API access with Strava OAuth integration

```- **Swagger Documentation**: Interactive API docs at `/api/docs/`

┌─────────────────────────────────────────────────────────┐- **Modern Frontend Ready**: Headless CMS architecture for React/Vue/Next.js

│                    Web Browser                           │

│            (Django Templates + Forms)                    │### 📊 Separate Leaderboards

└─────────────────────────────────────────────────────────┘

                         ↕ HTTP- Four distinct leaderboards for fair competition

┌─────────────────────────────────────────────────────────┐- Real-time ranking updates

│                Django Application                        │- Position tracking within your category

│                                                          │

│  • Views & Templates (ic_marathon_app/views.py)         │---

│  • Forms & Validation                                    │

│  • Django Admin Interface                                │## 🏗️ Architecture

│  • Strava OAuth Integration                              │

│  • Badge System (django-badgify)                         │### Headless Backend + Modern Frontend

│  • Automatic Category Management                         │

└─────────────────────────────────────────────────────────┘```

                         ↕┌─────────────────────────────────────────────────────────┐

┌─────────────────────────────────────────────────────────┐│                   Modern Frontend                        │

│                PostgreSQL Database                       ││          (React/Vue/Svelte/Next.js/etc.)                │

│                  (Heroku Postgres)                       ││                                                          │

│                                                          ││  • Strava OAuth Integration                             │

│  • User Profiles                                         ││  • Real-time Badge Notifications                        │

│  • Workouts                                              ││  • Progressive Web App (PWA)                            │

│  • Sports & Intensity Levels                             ││  • Responsive Design                                     │

│  • Badges & Awards                                       │└─────────────────────────────────────────────────────────┘

│  • Partner Workout Records                               │                         ↕ HTTP/REST

└─────────────────────────────────────────────────────────┘┌─────────────────────────────────────────────────────────┐

                         ↕│              Django REST API (Headless)                  │

┌─────────────────────────────────────────────────────────┐│                                                          │

│                AWS S3 Storage                            ││  • Token Authentication                                  │

│              (ciscorunningaws bucket)                    ││  • Auto-calculated Metrics                              │

│                                                          ││  • Badge System                                          │

│  • Profile Avatars                                       ││  • Anti-Sandbagging Logic                               │

│  • Workout Photo Evidence                                ││  • Swagger Documentation                                 │

└─────────────────────────────────────────────────────────┘└─────────────────────────────────────────────────────────┘

```                         ↕

┌─────────────────────────────────────────────────────────┐

### Technology Stack│          Django Admin (Auditing/Legacy)                  │

│                                                          │

- **Backend**: Django 4.2.7│  • Workout Auditing (is_audited flag)                   │

- **Database**: PostgreSQL (Heroku Postgres)│  • User Management                                       │

- **Storage**: AWS S3 (us-east-2 region)│  • Manual Badge Awards                                   │

- **Authentication**: Django-allauth with Strava OAuth│  • Database Management                                   │

- **Badge System**: django-badgify└─────────────────────────────────────────────────────────┘

- **Tables**: django-tables2```

- **Forms**: django-crispy-forms, django-bootstrap4

- **Deployment**: Heroku### Key Architectural Decisions

- **WSGI**: Gunicorn

1. **Headless API**: Django serves only JSON via REST API

---2. **Token Auth**: Modern frontends use token-based authentication

3. **CORS Enabled**: Cross-origin requests allowed for frontend apps

## 🚀 Installation4. **Admin Preserved**: Django admin remains for auditing and management

5. **Backward Compatible**: Legacy Django templates still work but deprecated

### Prerequisites

---

- Python 3.11.6 or higher

- PostgreSQL (for production) or SQLite (for development)## Modern Frontend Integration

- Git

- Virtual environment tool (venv or virtualenv)### 🚀 Quick Start for Frontend Developers

- Strava API credentials (Client ID and Secret)

- AWS S3 bucket (for production)#### 1. Authentication Flow (To Be Implemented)



### Mac InstallationAuthentication will be handled by your modern frontend. The backend provides:

- Token-based authentication via DRF

1. **Clone the repository**- Profile management endpoints

- Workout tracking endpoints

```bash

git clone https://github.com/sarifern/ciscorunning.git**Basic API Usage:**

cd ciscorunning

``````javascript

// Once you have a token (from your auth system)

2. **Create and activate virtual environment**const apiRequest = (url, options = {}) => {

  return fetch(url, {

```bash    ...options,

python3 -m venv venv    headers: {

source venv/bin/activate      ...options.headers,

```      'Authorization': `Token ${your_token_here}`,

      'Content-Type': 'application/json'

3. **Install dependencies**    }

  });

```bash};

pip install -r requirements.txt```

```

#### 2. Complete User Flow

4. **Set up environment variables**

```javascript

Create a `.env` file in the project root:// A. Check if user has profile

const checkProfile = async () => {

```bash  try {

# Django Settings    const response = await apiRequest('https://ciscorunning.herokuapp.com/api/profiles/me/');

DJANGO_SECRET_KEY=your-secret-key-here    if (response.ok) {

DEBUG_PREF=True

HOSTING_DOMAIN=127.0.0.1```      const profile = await response.json();



# Database (leave empty for SQLite in development)      return profile;

DATABASE_URL=

### Technical Stack    }

# Strava OAuth

STRAVA_CLIENT_ID=your-strava-client-id  } catch (error) {

STRAVA_CLIENT_SECRET=your-strava-client-secret

- **Backend**: Django 4.2.7    return null; // No profile exists

# AWS S3 (optional for local development)

AWS_ACCESS_KEY_ID=your-aws-access-key- **REST Framework**: Django REST Framework 3.16.1  }

AWS_SECRET_ACCESS_KEY=your-aws-secret-key

AWS_STORAGE_BUCKET_NAME=your-bucket-name- **API Docs**: drf-spectacular 0.27.0};

AWS_S3_REGION_NAME=us-east-2

```- **Database**: PostgreSQL 17



5. **Run migrations**- **Storage**: AWS S3 (ciscorunningaws bucket in us-east-2)// B. Create profile if needed



```bash- **Cache**: Memcached Cloud (Heroku addon)const createProfile = async (profileData) => {

python manage.py migrate

```- **Authentication**: Django AllAuth + Token Auth + Strava OAuth  const response = await apiRequest('https://ciscorunning.herokuapp.com/api/profiles/me/', {



6. **Initialize badge system**- **Badges**: Django Badgify    method: 'POST',



```bash- **Frontend**: Django Templates + CUI CSS Framework (legacy)    body: JSON.stringify({

python manage.py makemigrations badgify

python manage.py migrate badgify- **Deployment**: Heroku (ciscorunning app)      cec: profileData.cec,

python manage.py badgify_sync badges

python manage.py badgify_reset      user_goal_km: profileData.goalKm,

python manage.py badgify_sync awards --disable-signals

python manage.py badgify_sync counts---      category: profileData.category // 'runner' or 'freestyler'

```

    })

7. **Load initial data (sports and intensities)**

## 🚀 Quick Start  });

```bash

python manage.py migrate ic_marathon_app  return response.json();

```

### For Frontend Developers};

8. **Create superuser**



```bash

python manage.py createsuperuser1. **Get API Token via Strava OAuth**// C. Submit workout and get badge notifications

```

2. **Create Profile**: `POST /api/profiles/me/`const submitWorkout = async (workoutData) => {

9. **Run development server**

3. **Submit Workouts**: `POST /api/workouts/`  const formData = new FormData();

```bash

python manage.py runserver4. **Track Progress**: `GET /api/profiles/me/`  formData.append('belongs_to', profile.id);

```

5. **Check Badges**: Included in profile response  formData.append('distance', workoutData.distance);

Visit `http://127.0.0.1:8000/` to see the application.

  formData.append('date_time', workoutData.dateTime);

### Windows Installation

See [API Documentation](#api-documentation) for complete details.  formData.append('time', workoutData.duration);

1. **Clone the repository**

  formData.append('sport', workoutData.sportId);

```powershell

git clone https://github.com/sarifern/ciscorunning.git### For Backend Developers  formData.append('intensity', workoutData.intensity);

cd ciscorunning

```  formData.append('photo_evidence', workoutData.photo);



2. **Create and activate virtual environment**1. Clone repository  



```powershell2. Set up virtual environment  const response = await fetch('https://ciscorunning.herokuapp.com/api/workouts/', {

python -m venv venv

.\venv\Scripts\Activate.ps13. Install dependencies    method: 'POST',

```

4. Configure `.secrets` and `local_settings.py`    headers: {

3. **Install dependencies**

5. Run migrations      'Authorization': `Token ${localStorage.getItem('authToken')}`

```powershell

pip install -r requirements.txt6. Initialize badges    },

```

7. Start server    body: formData

4. **Set up environment variables**

  });

Create a `.env` file in the project root with the same variables as Mac installation.

See [Installation](#installation) for step-by-step instructions.  

5. **Run migrations**

  const result = await response.json();

```powershell

python manage.py migrate---  

```

  // Check for newly awarded badges

6. **Initialize badge system**

## 📦 Installation  if (result.newly_awarded_badges && result.newly_awarded_badges.length > 0) {

```powershell

python manage.py makemigrations badgify    result.newly_awarded_badges.forEach(badge => {

python manage.py migrate badgify

python manage.py badgify_sync badges### Prerequisites      showBadgeNotification(badge); // Your UI notification function

python manage.py badgify_reset

python manage.py badgify_sync awards --disable-signals    });

python manage.py badgify_sync counts

```- Python 3.11.6  }



7. **Load initial data**- PostgreSQL 17  



```powershell- Git  return result;

python manage.py migrate ic_marathon_app

```- Virtual environment tool (venv/virtualenv)};



8. **Create superuser**```



```powershell### Installation (Mac)

python manage.py createsuperuser

```#### 3. Profile Management



9. **Run development server**```javascript

// Get profile with all badges

```powershellconst getProfile = async () => {

python manage.py runserver  const response = await apiRequest('https://ciscorunning.herokuapp.com/api/profiles/me/');

```  const profile = await response.json();

  

Visit `http://127.0.0.1:8000/` to see the application.  /*

  Profile structure:

---  {

    user: "johndoe",

## 🏃 Running Locally

    cec: "johndoe",

### Development Server

3. **Edit hosts file** (requires sudo)    category: "runner",  // Intent (runner or freestyler)

```bash

python manage.py runserver```bash    actual_category: "Beginner Runner",  // Current progression

```

sudo nano /etc/hosts    distance: "25.50",

Access the application at `http://127.0.0.1:8000/`

# Add:    user_goal_km: "42.00",

### Admin Interface

127.0.0.1 www.lurifern.com    current_streak: 7,

Access the Django admin at `http://127.0.0.1:8000/admin/`

```    longest_streak: 12,

Use the superuser credentials you created during installation.

    workout_days_count: 18,

### Using Local Settings

4. **Install PostgreSQL**    awarded_badges: [

For development, you can use local settings:

```bash      {

```bash

python manage.py runserver --settings=ic_marathon_site.local_settingsbrew reinstall openssl        slug: "10K",

```

export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/        name: "10K Record Smashed",

---

brew install postgresql        description: "Congrats! You set a new 10k personal record",

## 🏆 Badge System

```        awarded_at: "2024-12-18T10:30:00Z"

The application uses django-badgify to award badges automatically based on achievements.

      },

### Distance Badges

5. **Add pg_config to PATH** (in ~/.bash_profile or ~/.zshrc)      // ... more badges

| Badge | Requirement | Description |

|-------|-------------|-------------|```bash    ]

| **10K Record Smashed** 🏅 | 10km total | Complete your first 10 kilometers |

| **Half Marathon Hero** 🏅 | 21km total | Reach the half marathon distance |export PATH=$PATH:/usr/local/bin/pg_config  }

| **Full Marathon Master** 🏅 | 42km total | Complete a full marathon equivalent! |

| **Double Marathon Legend** 🏅 | 84km total | Two marathons worth of effort |```  */

| **Triple Threat Champion** 🏅 | 126km total | Three marathon distances! |

| **Mega Marathon Titan** 🏅 | 168km total | Four marathons - incredible! |  

| **Personal Goal Achieved** 🎯 | User goal | Reach your personal goal |

6. **Install Xcode tools**  return profile;

### Streak Badges

```bash};

| Badge | Requirement | Description |

|-------|-------------|-------------|xcode-select --install

| **Week Warrior** 🔥 | 7 consecutive days | Complete 7 days in a row (27% of event) |

| **Fortnight Champion** 🔥 | 14 consecutive days | Complete 14 days in a row (54% of event) |```// Update goal

| **Three Week Legend** 🔥 | 21 consecutive days | Complete 21 days in a row (81% of event!) |

const updateGoal = async (newGoalKm) => {

### How Badges Work

7. **Create virtual environment**  const response = await apiRequest('https://ciscorunning.herokuapp.com/api/profiles/me/', {

1. **Automatic Detection**: Badges are checked after every workout submission

2. **Immediate Award**: Badges appear in your profile instantly when earned```bash    method: 'PATCH',

3. **Permanent**: Once earned, badges are never removed

4. **Notification**: Newly awarded badges are highlighted in the responsepython3.11 -m virtualenv venv    body: JSON.stringify({ user_goal_km: newGoalKm })

5. **Profile Display**: All earned badges shown on your profile page

source venv/bin/activate  });

---

```  return response.json();

## 📊 Category System

};

The application automatically manages user categories to ensure fair competition.

8. **Install dependencies**

### Categories

```bash// Switch category (one-time only)

1. **Beginner Runner**: New runners, auto-assigned on signup

2. **Runner**: Experienced runners who demonstrate performanceenv LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2==2.9.9const switchCategory = async (newCategory) => {

3. **Beginner Freestyler**: New freestylers, auto-assigned on signup

4. **Freestyler**: Experienced multi-sport athletespip install -r requirements.txt  const response = await apiRequest('https://ciscorunning.herokuapp.com/api/profiles/me/', {



### Auto-Promotion Rules```    method: 'PATCH',



Users are **automatically promoted** from Beginner to regular category when they meet **any** of these criteria:    body: JSON.stringify({ category: newCategory }) // 'runner' or 'freestyler'



#### Path 1: High Single Workout Performance9. **Configure environment** (get `.secrets` from admin)  });



- **Runner**: Single workout ≥ 10km at any intensity```bash  return response.json();

- **Freestyler**: Single workout ≥ 50km equivalent at any intensity

# Place .secrets in project root};

#### Path 2: Sustained Performance Level ⭐

export $(grep -v '^#' .secrets | xargs)```

- **5 or more workouts** averaging:

  - **Runner**: ≥ 8km per workout (regardless of intensity)```

  - **Freestyler**: ≥ 40km per workout (regardless of intensity)

#### 4. Badge Display

#### Path 3: Volume Threshold

10. **Collect static files** (if needed)

- **Runner**: Total distance ≥ 50km across any number of workouts

- **Freestyler**: Total distance ≥ 250km across any number of workouts```bash```javascript



### Category Examplespython manage.py collectstatic --settings=ic_marathon_site.local_settings// Display badge gallery



**Quick Promotion (Path 1):**```const displayBadges = (profile) => {

```

Day 1: 12km run → AUTO-PROMOTED to Runner immediately  const allBadges = [

```

11. **Setup badge system**    { slug: '10K', locked: true },

**Consistent Performance (Path 2):**

``````bash    { slug: '21K', locked: true },

Day 1: 10km → Day 2: 9km → Day 3: 11km → Day 4: 8km → Day 5: 12km

Total: 50km over 5 days, avg 10km/workoutpython manage.py makemigrations badgify --settings=ic_marathon_site.local_settings    { slug: '42K', locked: true },

Result: AUTO-PROMOTED to Runner (Path 2 triggered)

```python manage.py migrate badgify --settings=ic_marathon_site.local_settings    { slug: '84K', locked: true },



**Volume Builder (Path 3):**python manage.py badgify_sync badges --settings=ic_marathon_site.local_settings    { slug: '126K', locked: true },

```

Week 1: 3km x 7 days = 21kmpython manage.py badgify_reset --settings=ic_marathon_site.local_settings    { slug: '168K', locked: true },

Week 2: 3km x 7 days = 21km  

Week 3: 3km x 2 days = 6kmpython manage.py badgify_sync awards --disable-signals --settings=ic_marathon_site.local_settings    { slug: 'ownK', locked: true },

Total: 48km over 16 days

Result: Stays in Beginner (just below 50km threshold)python manage.py badgify_sync counts --settings=ic_marathon_site.local_settings    { slug: '7day-streak', locked: true },

```

```    { slug: '14day-streak', locked: true },

### One-Time Category Switch

    { slug: '21day-streak', locked: true },

Users can **manually switch** between Runner and Freestyler categories **once only**:

12. **Run migrations**  ];

- Switch from Runner to Freestyler (or vice versa)

- Available in profile settings```bash  

- Cannot switch back after changing

- Useful if you initially chose the wrong categorypython manage.py makemigrations --settings=ic_marathon_site.local_settings  // Mark earned badges as unlocked



### Important Notespython manage.py migrate --settings=ic_marathon_site.local_settings  profile.awarded_badges.forEach(earnedBadge => {



- Promotion is **automatic and immediate** - no admin action needed```    const badge = allBadges.find(b => b.slug === earnedBadge.slug);

- Once promoted, you **cannot** go back to Beginner

- The `category_changed` flag prevents manual changes once set    if (badge) {

- Admins can manually adjust categories if needed

13. **Initialize badges**      badge.locked = false;

---

```bash      badge.name = earnedBadge.name;

## 🤝 Partner Workouts

python manage.py shell < initialize_badges.py --settings=ic_marathon_site.local_settings      badge.description = earnedBadge.description;

Work out with a registered partner to earn bonus distance!

```      badge.awarded_at = earnedBadge.awarded_at;

### How It Works

    }

1. **Complete Workout**: Submit your workout as normal

2. **Add Partner**: Enter your partner's CEC (Cisco Employee ID)14. **Create superuser**  });

3. **Bonus Applied**: Both you and partner get 10% bonus distance

4. **Time Window**: Partner has 72 hours to claim the bonus```bash  

5. **Photo Required**: Upload photo evidence of working out together

python manage.py createsuperuser --settings=ic_marathon_site.local_settings  return allBadges;

### Rules

```};

- Partner must be a registered user in the system

- Both users must be in the same edition (2025)

- 72-hour expiration window for claiming bonus

- Photo evidence required for verification### Installation (Windows)// Calculate progress

- Bonus calculated: `original_distance * 0.10`

- Both partners receive the same bonus amountconst calculateProgress = (profile) => {



### Expiration1. **Clone the repository**  const totalBadges = 10;



Partner workout bonuses expire after 72 hours:```powershell  const earnedBadges = profile.awarded_badges.length;



- **Automatic Cleanup**: System removes expired partner workout recordsgit clone https://github.com/sarifern/ciscorunning.git  const percentage = (earnedBadges / totalBadges) * 100;

- **Original Distance Preserved**: Only bonus is removed, not your workout

- **Grace Period**: 72 hours gives partner time to claimcd ciscorunning  

- **Manual Check**: Admins can run `python manage.py expire_partner_bonuses` to clean up

```  return {

### Example

    earned: earnedBadges,

```

User A completes 10km run with User B as partner2. **Set up git config**    total: totalBadges,

↓

Both users get: 10km + 1km bonus = 11km total```powershell    percentage: Math.round(percentage)

↓

User B has 72 hours to accept/verifygit config user.name "Your Name"  };

↓

After 72 hours: Bonus expires if not verifiedgit config user.email "your.email@cisco.com"};

```

``````

---



## 🚀 Deployment

3. **Edit hosts file** (Run Notepad as Administrator)### 🔒 CORS Configuration

### Heroku Deployment

```

The application is configured for Heroku deployment.

# In C:\Windows\System32\drivers\etc\hostsCORS is pre-configured to allow requests from any origin during development. For production, you should restrict allowed origins in `local_settings.py`:

1. **Create Heroku app**

# Add:

```bash

heroku create your-app-name127.0.0.1 www.apradofern.com```python

```

```CORS_ALLOWED_ORIGINS = [

2. **Add PostgreSQL addon**

    "https://your-frontend-app.com",

```bash

heroku addons:create heroku-postgresql:mini4. **Install PostgreSQL 17**    "https://your-frontend-app.vercel.app",

```

- Download from: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads]

3. **Set environment variables**

- Set superuser password during installation```

```bash

heroku config:set DJANGO_SECRET_KEY=your-secret-key

heroku config:set DEBUG_PREF=False

heroku config:set STRAVA_CLIENT_ID=your-strava-client-id5. **Install Microsoft C++ Build Tools**### 📱 Strava OAuth Integration

heroku config:set STRAVA_CLIENT_SECRET=your-strava-client-secret

heroku config:set AWS_ACCESS_KEY_ID=your-aws-key- Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

heroku config:set AWS_SECRET_ACCESS_KEY=your-aws-secret

heroku config:set AWS_STORAGE_BUCKET_NAME=your-bucket-name- Select "Desktop development with C++"The backend already has Strava OAuth configured via Django Allauth. For your modern frontend:

heroku config:set AWS_S3_REGION_NAME=us-east-2

```- Only install the included packages (C++ Build Tools core features, C++ 2022 Redistributable, C++ core desktop features)



4. **Deploy**1. **Backend Handles OAuth**: Use the existing `/accounts/strava/login/` endpoint



```bash6. **Create virtual environment**2. **Redirect Flow**: Configure Strava to redirect to your frontend

git push heroku main

``````powershell3. **Token Exchange**: Frontend receives token and uses it for API calls



5. **Run migrations**pip install virtualenv



```bashvirtualenv .venv --python=3.11---

heroku run python manage.py migrate

heroku run python manage.py migrate badgify.\.venv\Scripts\activate

heroku run python manage.py badgify_sync badges

heroku run python manage.py badgify_reset```## API Documentation

heroku run python manage.py badgify_sync awards --disable-signals

heroku run python manage.py badgify_sync counts

```

7. **Install dependencies**### 🔗 Base URL

6. **Create superuser**

```powershell- **Local**: `https://localhost:8000/api/`

```bash

heroku run python manage.py createsuperuserpip install -r requirements.txt- **Production**: `https://ciscorunning.herokuapp.com/api/`

```

pip install -U setuptools

### Production Configuration

```### 📚 Interactive Documentation

The application automatically uses `render_settings.py` on Heroku, which:

- **Swagger UI**: `/api/docs/` - Full interactive API documentation

- Disables DEBUG mode

- Uses WhiteNoise for static files8. **Configure environment** (get `.secrets` from admin)- **ReDoc**: `/api/redoc/` - Alternative documentation view

- Configures AWS S3 for media storage

- Sets secure cookie settings```powershell- **OpenAPI Schema**: `/api/schema/` - Raw OpenAPI 3.0 schema

- Enables HTTPS redirects

# Place .secrets in project root

---

get-content .secrets | foreach {### 🔐 Authentication

## 🔧 Environment Variables

    $name, $value = $_.split('=')

### Required Variables

    set-content env:\$name $valueAll API endpoints require authentication. The API uses token-based authentication.

| Variable | Description | Example |

|----------|-------------|---------|}

| `DJANGO_SECRET_KEY` | Django secret key | Random 50-char string |

| `DATABASE_URL` | PostgreSQL connection | Auto-set by Heroku |$env:ENVIRONMENT='local_settings'**Supported Methods:**

| `STRAVA_CLIENT_ID` | Strava OAuth client ID | From Strava API settings |

| `STRAVA_CLIENT_SECRET` | Strava OAuth secret | From Strava API settings |```- **Token Authentication**: Use REST Framework tokens (recommended for API clients)



### AWS S3 Variables (Production)- **Session Authentication**: Use Django's session system (for browsable API)



| Variable | Description | Example |9. **Collect static files** (if needed)- **Basic Authentication**: Username/password with each request (for testing only)

|----------|-------------|---------|

| `AWS_ACCESS_KEY_ID` | AWS access key | `AKIAXXXXXXXXXXXXXXXX` |```powershell

| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Your secret key |

| `AWS_STORAGE_BUCKET_NAME` | S3 bucket name | `ciscorunningaws` |python manage.py collectstatic --settings=ic_marathon_site.$env:ENVIRONMENT**Note**: Authentication details will be finalized based on your frontend OAuth implementation.

| `AWS_S3_REGION_NAME` | AWS region | `us-east-2` |

```

### Optional Variables

#### Using the Token

| Variable | Description | Default |

|----------|-------------|---------|10. **Setup badge system**

| `DEBUG_PREF` | Enable debug mode | `False` |

| `HOSTING_DOMAIN` | Additional allowed host | None |```powershellInclude the token in the `Authorization` header of all API requests:



---python manage.py makemigrations badgify --settings=ic_marathon_site.$env:ENVIRONMENT



## 🧪 Testingpython manage.py migrate badgify --settings=ic_marathon_site.$env:ENVIRONMENT```http



A comprehensive testing guide is available in `TESTING.md` with over 40 test cases covering:python manage.py badgify_sync badges --settings=ic_marathon_site.$env:ENVIRONMENTAuthorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b



### User Testingpython manage.py badgify_reset --settings=ic_marathon_site.$env:ENVIRONMENT```

- Registration and authentication

- Profile managementpython manage.py badgify_sync awards --disable-signals --settings=ic_marathon_site.$env:ENVIRONMENT

- Workout submission

- Badge achievementspython manage.py badgify_sync counts --settings=ic_marathon_site.$env:ENVIRONMENT**Example with fetch:**

- Partner workouts

- Category progression``````javascript



### Admin Testingconst response = await fetch('https://ciscorunning.herokuapp.com/api/profiles/me/', {

- Workout auditing

- User management11. **Run migrations**  headers: {

- Badge management

- Data integrity```powershell    'Authorization': 'Token your-token-here',



### System Testingpython manage.py makemigrations --settings=ic_marathon_site.$env:ENVIRONMENT    'Content-Type': 'application/json'

- Performance testing

- Security testingpython manage.py migrate --settings=ic_marathon_site.$env:ENVIRONMENT  }

- Edge cases

```});

Run the test file:

```

```bash

# See TESTING.md for detailed test cases and expected outcomes12. **Initialize badges**

```

```powershell**Example with axios:**

---

python manage.py shell --settings=ic_marathon_site.$env:ENVIRONMENT```javascript

## 🐛 Troubleshooting

>>> exec(open('initialize_badges.py').read())axios.defaults.headers.common['Authorization'] = 'Token your-token-here';

### Common Issues

>>> exit()```

#### 1. Static Files Not Loading

```

**Solution**: Collect static files

### 📌 Endpoints

```bash

python manage.py collectstatic --noinput13. **Create superuser**

```

```powershell#### Profile Management

#### 2. Badge System Not Working

python manage.py createsuperuser --settings=ic_marathon_site.$env:ENVIRONMENT

**Solution**: Re-sync badge system

```##### `GET /api/profiles/me/`

```bash

python manage.py badgify_sync badgesGet your own profile information.

python manage.py badgify_reset

python manage.py badgify_sync awards --disable-signals14. **Create cache table**

python manage.py badgify_sync counts

``````powershell**Response Example:**



#### 3. S3 Images Not Loading (SignatureDoesNotMatch)python manage.py createcachetable --settings=ic_marathon_site.$env:ENVIRONMENT```json



**Solution**: Check IAM policy has correct permissions```{



```json  "user": "john.doe",

{

  "Version": "2012-10-17",---  "user_goal_km": "42.00",

  "Statement": [

    {  "category": "runner",

      "Sid": "VisualEditor0",

      "Effect": "Allow",## 🖥️ Running Locally  "actual_category": "Beginner Runner",

      "Action": [

        "s3:PutObject",  "cec": "johndoe",

        "s3:GetObject",

        "s3:DeleteObject",### Using VSCode Debugger  "avatar": "https://ciscorunning2023.s3.us-east-1.amazonaws.com/static/img/user.png",

        "s3:ListBucket",

        "s3:GetObjectAcl",  "distance": "15.50",

        "s3:PutObjectAcl"

      ],VSCode is preconfigured with `.vscode/launch.json` for debugging.  "category_changed": false,

      "Resource": [

        "arn:aws:s3:::ciscorunningaws/*",  "current_streak": 5,

        "arn:aws:s3:::ciscorunningaws"

      ]### Manual Start  "longest_streak": 12,

    }

  ]  "workout_days_count": 18,

}

```**Mac/Linux:**  "awarded_badges": [



#### 4. Database Migration Errors```bash    {



**Solution**: Reset migrations (development only)python manage.py runsslserver --settings=ic_marathon_site.local_settings      "slug": "10K",



```bash```      "name": "10K Record Smashed",

# WARNING: This deletes all data

python manage.py migrate ic_marathon_app zero      "description": "Congrats! You set a new 10k personal record",

python manage.py migrate

```**Windows:**      "awarded_at": "2024-12-18T10:30:00Z"



#### 5. Strava OAuth Not Working```powershell    },



**Solution**: Check callback URL in Strava settingspython manage.py runsslserver --settings=ic_marathon_site.$env:ENVIRONMENT    {



- Authorization Callback Domain: `your-domain.herokuapp.com````      "slug": "7day-streak",

- Redirect URI: `https://your-domain.herokuapp.com/accounts/strava/login/callback/`

      "name": "Week Warrior",

### Debug Mode

### Access Points      "description": "Amazing! You completed 7 consecutive days of workouts!",

To enable debug mode locally:

      "awarded_at": "2024-12-20T08:15:00Z"

```bash

export DEBUG_PREF=True  # Mac/Linux- **Web Interface**: https://www.lurifern.com:8000 (Mac) or https://www.apradofern.com:8000 (Windows)    }

$env:DEBUG_PREF="True"  # Windows PowerShell

```- **Admin Panel**: https://localhost:8000/admin  ]



### Logs- **API Root**: https://localhost:8000/api/}



View Heroku logs:- **API Docs**: https://localhost:8000/api/docs/```



```bash

heroku logs --tail --app your-app-name

```---**Notes:**



---- `category`: Shows your selected track (runner or freestyler)



## 📝 Admin Interface## 📚 API Documentation- `actual_category`: Shows your current progression (Beginner Runner → Runner)



### Accessing Admin- `distance`: Auto-calculated from workouts (read-only)



Navigate to `/admin/` and login with superuser credentials.### Base URLs- `current_streak`: Consecutive days with workouts (resets if you skip a day)



### Key Admin Functions- `longest_streak`: Your personal best streak record



#### Workout Auditing- **Development**: `http://localhost:8000/api/`- `workout_days_count`: Total unique days you've worked out



- View all submitted workouts- **Production**: `https://ciscorunning-ecfd9da3d311.herokuapp.com/api/`

- Check `is_audited` flag for verified workouts- `awarded_badges`: Array of all badges you've earned (with full details)

- Filter by user, date, sport, category

- Review photo evidence### Interactive Documentation



#### User Management- **Swagger UI**: `/api/docs/`

- **ReDoc**: `/api/redoc/`

- View all registered users- **OpenAPI Schema**: `/api/schema/`

- Check category assignments

- View total distances### Authentication

- Monitor streak progress

- Award manual badges if neededThe API uses Token-based authentication with Strava OAuth integration.



#### Badge Management#### Step 1: Strava OAuth (Frontend)



- View all available badges```javascript

- Check badge awards// Redirect user to Strava for authorization

- See badge statistics

- Manual badge awards (if needed)const STRAVA_CLIENT_ID = 'your_strava_client_id';- Backend automatically assigns you to beginner category



#### Partner Workoutsconst REDIRECT_URI = 'https://yourfrontend.com/auth/callback';- You'll be auto-promoted based on performance



- Review partner workout claimsconst STRAVA_AUTH_URL = `https://www.strava.com/oauth/authorize?client_id=${STRAVA_CLIENT_ID}&response_type=code&redirect_uri=${REDIRECT_URI}&approval_prompt=force&scope=activity:read_all`;

- Check expiration status

- Verify photo evidence##### `PUT /api/profiles/me/`

- Manual bonus adjustments

window.location.href = STRAVA_AUTH_URL;

---```



## 📄 License#### Step 2: Exchange Code for Token



This project is proprietary software for internal Cisco use only. See the [LICENSE](LICENSE) file for details.```javascript

// Strava redirects back with authorization code

---const exchangeTokens = async (code) => {

  const response = await fetch('https://www.strava.com/oauth/token', {

## 🤝 Contributing    method: 'POST',

    headers: { 'Content-Type': 'application/json' },

This is an internal Cisco project. For questions or contributions, contact the development team.    body: JSON.stringify({

      client_id: 'your_strava_client_id',

---      client_secret: 'your_strava_client_secret',

      code: code,

## 📞 Support

      grant_type: 'authorization_code'```json

For technical issues or questions:

    }){

1. Check [TESTING.md](TESTING.md) for comprehensive test scenarios

2. Review [Troubleshooting](#troubleshooting) section above  });  "user_goal_km": "84.00"

3. Contact the development team

4. Check Heroku logs for production issues  }



---  const data = await response.json();```



## 🎯 Project Structure  return data.access_token; // Use this with backend



```};**Notes:**

ciscorunning/

├── ic_marathon_app/          # Main Django application```- Can update `user_goal_km` unlimited times

│   ├── models.py             # Data models (Profile, Workout, Sport, etc.)

│   ├── views.py              # View logic- Can only change `category` (runner ↔ freestyler) **once**

│   ├── auth_views.py         # Strava OAuth views

│   ├── forms.py              # Form definitions#### Step 3: Authenticate with Backend- Cannot manually change beginner status (auto-managed)

│   ├── tables.py             # Django-tables2 definitions

│   ├── signals.py            # Post-save signals for badges

│   ├── validators.py         # Custom validators

│   ├── templates/            # HTML templates```javascript##### `DELETE /api/profiles/me/`

│   ├── static/               # CSS, JS, images

│   └── management/           # Custom management commandsconst authenticateWithBackend = async (stravaAccessToken) => {Delete your profile and all associated workouts.

│       └── commands/

│           └── expire_partner_bonuses.py  const response = await fetch('https://ciscorunning.herokuapp.com/api/auth/strava/', {

├── ic_marathon_site/         # Django project settings

│   ├── settings.py           # Base settings      grant_type: 'authorization_code'

│   ├── local_settings.py     # Local development settings    })

│   ├── render_settings.py    # Production settings (Heroku)  });

│   ├── urls.py               # URL routing  

│   └── storage_backends.py   # AWS S3 configuration  const { access_token, refresh_token } = await response.json();

├── manage.py                 # Django management script  return { access_token, refresh_token };

├── requirements.txt          # Python dependencies};

├── Procfile                  # Heroku process file```

├── runtime.txt               # Python version for Heroku

├── README.md                 # This file#### Step 3: Authenticate with Backend

├── TESTING.md                # Comprehensive testing guide

└── db.sqlite3                # SQLite database (development)```javascript

```// Send Strava token to your backend to create/authenticate user

const authenticateUser = async (stravaAccessToken) => {

---  const response = await fetch('https://ciscorunning.herokuapp.com/api/auth/strava/', {

    method: 'POST',

## 🔄 Key Workflows    headers: { 'Content-Type': 'application/json' },

    body: JSON.stringify({

### User Registration Flow      strava_access_token: stravaAccessToken

    })

1. User clicks "Login with Strava"  });

2. Redirected to Strava for authorization  

3. Strava redirects back with auth code  const { token, user } = await response.json();

4. System creates/updates user profile  localStorage.setItem('authToken', token);

5. User automatically assigned to Beginner category  return { token, user };

6. User can set personal goal and category preference};

```

### Workout Submission Flow

#### Step 4: Use Token for API Calls

1. User fills workout form (distance, time, sport, intensity)

2. Optional: Add photo evidence```javascript

3. Optional: Add partner CEC

4. System validates dataconst apiRequest = (url, options = {}) => {    "time": "00:30:00",

5. System saves workout

6. System checks for badge awards  return fetch(url, {    "sport": 1,

7. System updates streaks

8. System checks for category promotion    ...options,    "intensity": 2,

9. User sees confirmation with any new badges

    headers: {    "photo_evidence": "https://..."

### Badge Award Flow

      ...options.headers,  }

1. Workout saved to database

2. Post-save signal triggers badge check      'Authorization': `Token ${localStorage.getItem('authToken')}`,]

3. System calculates total distance

4. System checks current/longest streaks      'Content-Type': 'application/json'```

5. System compares against badge thresholds

6. Awards any newly-earned badges    }

7. Returns list of newly awarded badges

  });##### `POST /api/workouts/`

---

};Create a new workout.

**Built with ❤️ for Cisco's Fitness Community**

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



##### `GET /api/workouts/`

List all workouts for authenticated user.

**Response:**

```json
[
  {
    "uuid": "123e4567-e89b-12d3-a456-426614174000",
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

##### `POST /api/workouts/`

Submit a new workout.

**Request (multipart/form-data):**

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

      "sport_id": 1,
      "sport_name": "Running",
      "intensity_id": 2,
      "intensity_name": "Moderate",
      "km_per_hour": 10.0
    }
  ]
}
```

**Use Case:** Get this data once on app load to populate dropdowns and calculate distance.

---

## 🤝 Partner Workouts

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
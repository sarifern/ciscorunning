# Cisco Running Challenge 2025

 **Marathon-Style Fitness Competition** | December 12, 2024 - January 6, 2025 (26 Days)

[![Python](https://img.shields.io/badge/Python-3.11.6-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-Cisco_Internal-red.svg)](LICENSE)

A Django-based web application for tracking and gamifying fitness activities during Cisco''s annual running challenge. Participants compete in two tracks (Runner and Freestyler) with automatic category assignment, badge achievements, and streak tracking.

---

##  Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Mac Installation](#mac-installation)
  - [Windows Installation](#windows-installation)
- [Running Locally](#running-locally)
- [Badge System](#badge-system)
- [Category System](#category-system)
- [Partner Workouts](#partner-workouts)
- [Deployment](#deployment)
- [Environment Variables](#environment-variables)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

##  Overview

The Cisco Running Challenge is a gamified fitness competition where participants compete in two main tracks:

- **Advanced Runner Track**: Traditional running activities
- **Advanced Freestyler Track**: Various sports (cycling, swimming, hiking, etc.) converted to km equivalents

### Event Details

- **Duration**: December 12, 2024 - January 7, 2025 (27 days)
- **Goal**: Complete a marathon-equivalent distance (42.195 km) or personal goal
- **Competition**: Four separate leaderboards for fair competition
- **Rewards**: Achievement badges for distance milestones and consecutive workout streaks

---

##  Key Features

###  Smart Category System

- **Auto-Assignment**: New users automatically assigned to "Beginner" categories
- **Anti-Sandbagging**: System detects skilled athletes and promotes them automatically
- **Four Categories**: Beginner Runner, Advanced Runner, Beginner Freestyler, Advanced Freestyler
- **Fair Competition**: Separate leaderboards prevent experienced athletes from dominating beginner categories

###  Achievement Badges

- **Distance Badges**: 10K, 21K, 42K, 84K, 126K, 168K, Personal Goal
- **Streak Badges**: 7-day, 14-day, 21-day consecutive workout achievements
- **Automatic Awards**: Real-time badge checking on every workout submission
- **Permanent**: Once earned, badges are never lost

###  Streak Tracking

- **Current Streak**: Tracks consecutive days with workouts
- **Longest Streak**: Records personal best (never decreases)
- **Smart Detection**: Resets if you skip a day
- **Gamification**: Encourages daily participation

###  Partner Workouts

- **Bonus Distance**: Work out with registered partner for 1.5x distance bonus
- **Expiration**: 2-day window to confirm partner workout
- **Dual Tracking**: Both partners receive bonus distance after confirmation
- **Verification**: Photo evidence required
- **Preserved Workouts**: Declined/expired workouts convert to solo workouts (no bonus)

###  Separate Leaderboards

- Four distinct leaderboards for fair competition
- Real-time ranking updates
- Position tracking within your category
- Distance progress visualization

###  Authentication

- **Strava OAuth**: Login with your Strava account
- **Profile Sync**: Automatic profile data from Strava
- **Secure**: Token-based authentication
- **Avatar Support**: AWS S3 storage for profile pictures

---

##  Architecture

### Django Monolith Application

```

                    Web Browser                           
            (Django Templates + Forms)                    

                          HTTP

                Django Application                        
                                                          
   Views & Templates (ic_marathon_app/views.py)         
   Forms & Validation                                    
   Django Admin Interface                                
   Strava OAuth Integration                              
   Badge System (django-badgify)                         
   Automatic Category Management                         

                         

                PostgreSQL Database                       
                  (Heroku Postgres)                       
                                                          
   User Profiles                                         
   Workouts                                              
   Sports & Intensity Levels                             
   Badges & Awards                                       
   Partner Workout Records                               

                         

                AWS S3 Storage                            
              (ciscorunningaws bucket)                    
                                                          
   Profile Avatars                                       
   Workout Photo Evidence                                

```

### Technology Stack

- **Backend**: Django 4.2.7
- **Database**: PostgreSQL (Heroku Postgres)
- **Storage**: AWS S3 (us-east-2 region)
- **Authentication**: Django-allauth with Strava OAuth
- **Badge System**: django-badgify
- **Tables**: django-tables2
- **Forms**: django-crispy-forms, django-bootstrap4
- **Deployment**: Heroku
- **WSGI**: Gunicorn

---

##  Badge System

The application uses django-badgify to award badges automatically based on achievements.

### Distance Badges

| Badge | Requirement | Description |
|-------|-------------|-------------|
| **10K Record Smashed**  | 10km total | Complete your first 10 kilometers |
| **Half Marathon Hero**  | 21km total | Reach the half marathon distance |
| **Full Marathon Master**  | 42km total | Complete a full marathon equivalent! |
| **Double Marathon Legend**  | 84km total | Two marathons worth of effort |
| **Triple Threat Champion**  | 126km total | Three marathon distances! |
| **Mega Marathon Titan**  | 168km total | Four marathons - incredible! |
| **Personal Goal Achieved**  | User goal | Reach your personal goal |

### Streak Badges

| Badge | Requirement | Description |
|-------|-------------|-------------|
| **Week Warrior**  | 7 consecutive days | Complete 7 days in a row (27% of event) |
| **Fortnight Champion**  | 14 consecutive days | Complete 14 days in a row (54% of event) |
| **Three Week Legend**  | 21 consecutive days | Complete 21 days in a row (81% of event!) |

### How Badges Work

1. **Automatic Detection**: Badges are checked after every workout submission
2. **Immediate Award**: Badges appear in your profile instantly when earned
3. **Permanent**: Once earned, badges are never removed
4. **Notification**: Newly awarded badges are highlighted
5. **Profile Display**: All earned badges shown on your profile page

---

##  Category System

The application automatically manages user categories to ensure fair competition.

### Categories

1. **Beginner Runner**: New runners, auto-assigned on signup
2. **Advanced Runner**: Experienced runners who demonstrate performance
3. **Beginner Freestyler**: New freestylers, auto-assigned on signup
4. **Advanced Freestyler**: Experienced multi-sport athletes

### Auto-Promotion Rules

Users are **automatically promoted** from Beginner to regular category when they meet **any** of these criteria:

#### Path 1: High Single Workout Performance

- **Advanced Runner**: Single workout  10km at any intensity
- **Advanced Freestyler**: Single workout  50km equivalent at any intensity

#### Path 2: Sustained Performance Level 

- **5 or more workouts** averaging:
  - **Advanced Runner**:  8km per workout (regardless of intensity)
  - **Advanced Freestyler**:  40km per workout (regardless of intensity)

#### Path 3: Volume Threshold

- **Advanced Runner**: Total distance  84km across any number of workouts
- **Advanced Freestyler**: Total distance  135km across any number of workouts

### Category Examples

**Quick Promotion (Path 1):**
```
Day 1: 12km run  AUTO-PROMOTED to Advanced Runner immediately
```

**Consistent Performance (Path 2):**
```
Day 1: 10km  Day 2: 9km  Day 3: 11km  Day 4: 8km  Day 5: 12km
Total: 50km over 5 days, avg 10km/workout
Result: AUTO-PROMOTED to Advanced Runner (Path 2 triggered)
```

**Volume Builder (Path 3):**
```
Week 1: 5km x 7 days = 35km
Week 2: 5km x 7 days = 35km  
Week 3: 5km x 3 days = 15km
Total: 85km over 17 days
Result: AUTO-PROMOTED to Advanced Runner (Path 3 triggered - exceeded 84km threshold)
```

### One-Time Category Switch

Users can **manually switch** between Advanced Runner and Advanced Freestyler categories **once only**:

- Switch from Advanced Runner to Advanced Freestyler (or vice versa)
- Available in profile settings
- **Must be done before reaching 40km** total distance
- Cannot switch back after changing
- Useful if you initially chose the wrong category

**Anti-Gaming Measure**: Category switches are only allowed before accumulating 40km to prevent users from gaming the system by switching categories mid-challenge.

### Important Notes

- Promotion is **automatic and immediate** - no admin action needed
- Once promoted, you **cannot** go back to Beginner
- Category switch blocked after 40km total distance
- The `category_changed` flag prevents multiple switches
- Admins can manually adjust categories if needed

---

##  Partner Workouts

Work out with a registered partner to earn bonus distance!

### How It Works

1. **Complete Workout Together**: Do your workout activity with your partner
2. **Take Photo Evidence**: Capture photo showing **both Cisconians** together during or after the workout
3. **Submit Workout**: Enter workout details and select your partner from the dropdown
4. **Upload Photo**: Attach the photo showing both participants
5. **Partner Confirms**: Partner has 2 days to confirm the workout
6. **Bonus Applied**: After confirmation, both receive 1.5x distance!

### Rules

- **Partner must be registered** in the system (same edition)
- **Photo must show both participants** - this is required for verification
- **Same category track** - both must be Advanced Runners or both Advanced Freestylers
- **2-day confirmation window** - partner must confirm within 48 hours
- **1.5x distance bonus** - both users receive: `base_distance × 1.5`
- **Photo sharing** - the same photo is used for both workout records

### Important: Photo Evidence Requirements

⚠️ **The photo must clearly show BOTH Cisconians together**

Valid examples:
- ✅ Selfie with both participants after the run
- ✅ Photo of both during the activity (cycling, hiking, etc.)
- ✅ Group shot at the workout location

Invalid examples:
- ❌ Solo photo of just one person
- ❌ Separate photos of each person
- ❌ Screenshot of workout data only

### Workflow

**When you submit a partner workout:**
1. Workout is created with `partner_confirmed = False`
2. Partner receives notification with bell icon indicator
3. Partner reviews workout and photo evidence
4. Partner can **Confirm** or **Decline**

**If Confirmed:**
- Original workout gets 1.5x bonus distance
- Matching workout created for partner with same bonus
- Both users earn badges if distance thresholds are met

**If Declined or Expired (>2 days):**
- Workout is automatically converted to solo workout
- Only base distance is counted (no bonus)
- Original workout is preserved, not deleted

### Example

```
User A completes 10km run with User B as partner
User A submits workout with photo showing both users
Photo is uploaded with workout details

User B receives notification to confirm
User B has 48 hours to confirm

If confirmed:
  User A gets: 10km × 1.5 = 15km
  User B gets: 10km × 1.5 = 15km
  Both workouts linked with same photo

If declined/expired:
  User A gets: 10km (base distance only, no bonus)
  User B gets: nothing (no workout created)
```

### Management Command

Admins can manually clean up expired partner workouts:

```bash
python manage.py cleanup_expired_partner_workouts
```

This command:
- Finds all unconfirmed partner workouts older than 2 days
- Converts them to regular solo workouts (base distance only)
- Removes partner links and bonus distance
- Preserves the original workout data

---

**Built with  for Cisco''s Fitness Community**

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

- **Runner Track**: Traditional running activities
- **Freestyler Track**: Various sports (cycling, swimming, hiking, etc.) converted to km equivalents

### Event Details

- **Duration**: December 12, 2024 - January 6, 2025 (26 days)
- **Goal**: Complete a marathon-equivalent distance (42.195 km) or personal goal
- **Competition**: Four separate leaderboards for fair competition
- **Rewards**: Achievement badges for distance milestones and consecutive workout streaks

---

##  Key Features

###  Smart Category System

- **Auto-Assignment**: New users automatically assigned to "Beginner" categories
- **Anti-Sandbagging**: System detects skilled athletes and promotes them automatically
- **Four Categories**: Beginner Runner, Runner, Beginner Freestyler, Freestyler
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

- **Bonus Distance**: Work out with registered partner for 10% bonus
- **Expiration**: 72-hour window to claim bonus
- **Dual Tracking**: Both partners receive bonus distance
- **Verification**: Photo evidence required

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
2. **Runner**: Experienced runners who demonstrate performance
3. **Beginner Freestyler**: New freestylers, auto-assigned on signup
4. **Freestyler**: Experienced multi-sport athletes

### Auto-Promotion Rules

Users are **automatically promoted** from Beginner to regular category when they meet **any** of these criteria:

#### Path 1: High Single Workout Performance

- **Runner**: Single workout  10km at any intensity
- **Freestyler**: Single workout  50km equivalent at any intensity

#### Path 2: Sustained Performance Level 

- **5 or more workouts** averaging:
  - **Runner**:  8km per workout (regardless of intensity)
  - **Freestyler**:  40km per workout (regardless of intensity)

#### Path 3: Volume Threshold

- **Runner**: Total distance  84km across any number of workouts
- **Freestyler**: Total distance  135km across any number of workouts

### Category Examples

**Quick Promotion (Path 1):**
```
Day 1: 12km run  AUTO-PROMOTED to Runner immediately
```

**Consistent Performance (Path 2):**
```
Day 1: 10km  Day 2: 9km  Day 3: 11km  Day 4: 8km  Day 5: 12km
Total: 50km over 5 days, avg 10km/workout
Result: AUTO-PROMOTED to Runner (Path 2 triggered)
```

**Volume Builder (Path 3):**
```
Week 1: 5km x 7 days = 35km
Week 2: 5km x 7 days = 35km  
Week 3: 5km x 3 days = 15km
Total: 85km over 17 days
Result: AUTO-PROMOTED to Runner (Path 3 triggered - exceeded 84km threshold)
```

### One-Time Category Switch

Users can **manually switch** between Runner and Freestyler categories **once only**:

- Switch from Runner to Freestyler (or vice versa)
- Available in profile settings
- Cannot switch back after changing
- Useful if you initially chose the wrong category

### Important Notes

- Promotion is **automatic and immediate** - no admin action needed
- Once promoted, you **cannot** go back to Beginner
- The `category_changed` flag prevents manual changes once set
- Admins can manually adjust categories if needed

---

##  Partner Workouts

Work out with a registered partner to earn bonus distance!

### How It Works

1. **Complete Workout**: Submit your workout as normal
2. **Add Partner**: Enter your partner''s CEC (Cisco Employee ID)
3. **Bonus Applied**: Both you and partner get 10% bonus distance
4. **Time Window**: Partner has 72 hours to claim the bonus
5. **Photo Required**: Upload photo evidence of working out together

### Rules

- Partner must be a registered user in the system
- Both users must be in the same edition (2025)
- 72-hour expiration window for claiming bonus
- Photo evidence required for verification
- Bonus calculated: `original_distance * 0.10`
- Both partners receive the same bonus amount

### Expiration

Partner workout bonuses expire after 72 hours:

- **Automatic Cleanup**: System removes expired partner workout records
- **Original Distance Preserved**: Only bonus is removed, not your workout
- **Grace Period**: 72 hours gives partner time to claim
- **Manual Check**: Admins can run `python manage.py expire_partner_bonuses` to clean up

### Example

```
User A completes 10km run with User B as partner

Both users get: 10km + 1km bonus = 11km total

User B has 72 hours to accept/verify

After 72 hours: Bonus expires if not verified
```

---

**Built with  for Cisco''s Fitness Community**

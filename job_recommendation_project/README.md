# ⬡ NexaJobs — AI Job Recommendation System

A fully responsive Django web application with 3D animated UI, ML-powered job recommendations.

---

## 🚀 Quick Setup (VS Code)

### Step 1 — Open in VS Code
Open the `job_recommendation_project` folder in VS Code.

### Step 2 — Create Virtual Environment
Open the **Terminal** in VS Code (`Ctrl+`` ` `` `):
```bash
python -m venv venv
```

### Step 3 — Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```
**Mac/Linux:**
```bash
source venv/bin/activate
```

### Step 4 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5 — Run Migrations
```bash
python manage.py migrate
```

### Step 6 — Seed Sample Jobs
```bash
python manage.py seed_jobs
```
This adds 12 sample job listings to the database.

### Step 7 — Create Admin Account
```bash
python manage.py createsuperuser
```
Follow the prompts to create username/password.

### Step 8 — Run the Server
```bash
python manage.py runserver
```

### Step 9 — Open in Browser
Go to: **http://127.0.0.1:8000**

---

## 📁 Project Structure

```
job_recommendation_project/
│
├── job_recommendation/       # Main Django config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/                 # User auth & profiles
│   ├── models.py             # UserProfile model
│   ├── views.py              # Register, login, profile
│   ├── forms.py              # Auth & profile forms
│   └── urls.py
│
├── jobs/                     # Job listings
│   ├── models.py             # JobListing model
│   ├── views.py              # Home, list, detail, dashboard
│   ├── urls.py
│   └── management/commands/seed_jobs.py
│
├── recommendations/          # ML engine
│   ├── engine.py             # TF-IDF + Cosine Similarity
│   ├── models.py             # Recommendation model
│   └── views.py
│
├── feedback/                 # User feedback loop
│   ├── models.py             # UserFeedback model
│   └── views.py
│
├── templates/                # All HTML templates
│   ├── base.html             # 3D Three.js particle background
│   ├── jobs/
│   │   ├── home.html         # Landing page
│   │   ├── job_list.html     # Browse with filters
│   │   ├── job_detail.html   # Job detail
│   │   └── dashboard.html    # User dashboard
│   ├── accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   └── profile_edit.html
│   ├── recommendations/
│   │   └── recommendations.html
│   └── feedback/
│       └── saved_jobs.html
│
├── requirements.txt
└── manage.py
```

---

## 🌐 Pages & URLs

| URL | Page |
|-----|------|
| `/` | Home / Landing |
| `/jobs/` | Browse all jobs with filters |
| `/jobs/<id>/` | Job detail |
| `/dashboard/` | User dashboard |
| `/recommendations/` | AI recommendations |
| `/feedback/saved/` | Saved/Applied/Liked jobs |
| `/accounts/register/` | Register |
| `/accounts/login/` | Login |
| `/accounts/profile/` | Profile view |
| `/accounts/profile/edit/` | Edit profile |
| `/admin/` | Django admin panel |

---

## 🤖 How the ML Works

1. **TF-IDF Vectorization** — Converts job descriptions + user profile into numerical vectors
2. **Cosine Similarity** — Measures angle between user vector and each job vector
3. **Skill Boosting** — Exact skill matches and experience-level matches boost scores
4. **Location Boost** — Jobs in preferred location get score bump
5. **Feedback Loop** — User actions (like, skip, apply) tracked for future improvement

---

## ✨ Features

- 🎨 **3D particle background** using Three.js
- 🌙 **Dark glassmorphism UI** 
- 🤖 **AI job matching** with TF-IDF + Cosine Similarity
- 👤 **User profiles** with skills, experience, preferences, resume paste
- 🔍 **Advanced search & filters** (category, type, location, experience)
- 💾 **Save/Like/Apply** jobs
- 📊 **Dashboard** with stats and top matches
- 📱 **Fully responsive** mobile design
- 🛡️ **Django Admin** for managing jobs

---

## 🔧 Admin Panel

Go to `/admin/` and login with your superuser credentials to:
- Add/edit/delete job listings
- View user profiles and feedback
- Manage recommendations

---

## 📦 Tech Stack

- **Backend**: Django 4.2, SQLite
- **ML**: scikit-learn (TF-IDF, Cosine Similarity)
- **Frontend**: Vanilla HTML/CSS/JS + Three.js (3D)
- **Fonts**: Syne + DM Sans (Google Fonts)

# Human Free Will Erosion Engine

A behavioral analytics system that models **how predictable human decision patterns become over time**.

The system logs human actions, analyzes behavioral entropy and predictability, and estimates a **Free Will Index** using statistical analysis, Markov transition modeling, and behavioral simulation.

---

# Live Demo

Dashboard
[https://human-free-will-erosion-dashboard.onrender.com/](https://human-free-will-erosion-dashboard.onrender.com/)

API Documentation
[https://human-free-will-api.onrender.com/docs](https://human-free-will-api.onrender.com/docs)

---

# Concept

Human behavior often becomes repetitive over time.

When actions become habitual, the **entropy of behavioral patterns decreases** and the system becomes increasingly predictable.

The **Human Free Will Erosion Engine** attempts to quantify this phenomenon by modeling behavioral sequences and measuring:

* behavioral entropy
* predictability
* habit loop formation
* future action probabilities

The system explores a central question:

> Can human behavior gradually become statistically deterministic?

---

# System Architecture

```
User
 ↓
Streamlit Dashboard
 ↓
FastAPI Backend
 ↓
Authentication Layer (JWT)
 ↓
Behavior Logging System
 ↓
PostgreSQL Database
 ↓
Behavior Analysis Engine
    ├ Entropy Analysis
    ├ Predictability Metrics
    ├ Markov Transition Model
    ├ Habit Loop Detection
    └ Behavior Simulation
```

---

# Tech Stack

Backend

* FastAPI
* Python
* SQLAlchemy ORM
* JWT Authentication

Frontend

* Streamlit Dashboard

Database

* PostgreSQL

Analytics

* Behavioral entropy calculation
* Markov transition prediction
* Habit loop detection
* Future behavior simulation

Deployment

* Render Cloud Platform

---

# Core Features

## User Authentication

Secure user authentication using JWT tokens.

Endpoints:

```
POST /auth/register
POST /auth/login
```

---

# Decision Logging

Users can log behavioral events with timestamp and domain.

Example payload

```json
{
 "action": "study",
 "domain": "work",
 "occurred_at": "2026-03-13T12:06:48+05:30"
}
```

Endpoint

```
POST /decision/log
```

Users can also

* edit decisions
* delete decisions
* view decision history

---

# Behavioral Entropy

Entropy measures how **diverse a user's actions are**.

Higher entropy

→ varied behavior

Lower entropy

→ repetitive behavior

Computed using:

```
Shannon entropy
```

---

# Predictability Score

Predictability measures how easily future actions can be predicted based on past behavior.

Computed as:

```
Predictability = 1 − (entropy / log2(unique_actions))
```

Higher score means stronger behavioral patterns.

---

# Free Will Index

A derived metric combining entropy and prediction confidence.

Conceptually:

```
Free Will Index ≈ randomness of behavior
```

Lower values indicate:

* strong routines
* deterministic patterns
* habit loops

---

# Markov Next Action Prediction

The system builds a **transition probability matrix** from historical decisions.

Example sequence

```
study → youtube → study → youtube
```

Transition matrix

```
study → youtube (0.8)
youtube → study (0.7)
```

Prediction returns

```
next action + confidence score
```

Endpoint

```
GET /analysis/predict-next
```

Example response

```json
{
 "next_action": "youtube",
 "confidence": 0.67
}
```

---

# Behavior Simulation

The engine can simulate **future behavioral sequences** using the Markov model.

Simulation outputs

* predicted 24h predictability
* dominant habit loop
* simulated future action sequence

Endpoint

```
GET /analysis/simulate
```

Example output

```
Predicted 24h Predictability: 0.78
Dominant Habit Loop:
study → youtube → study
```

---

# Analytics Endpoints

Behavior analysis

```
GET /analysis/today
GET /analysis/summary
```

Decision history

```
GET /analysis/history
```

Prediction

```
GET /analysis/predict-next
```

Simulation

```
GET /analysis/simulate
```

Full API docs

[https://human-free-will-api.onrender.com/docs](https://human-free-will-api.onrender.com/docs)

---

# Streamlit Dashboard

The Streamlit interface provides an interactive behavioral analytics dashboard.

Features

* decision logging
* decision editing and deletion
* history filtering
* entropy trend visualization
* action frequency charts
* free will index display
* next action prediction
* behavior simulation results

---

# Project Structure

```
human-free-will-erosion-engine
│
├ app
│   ├ analysis
│   │   ├ entropy.py
│   │   ├ markov.py
│   │   ├ metrics.py
│   │   └ simulation.py
│   │
│   ├ routers
│   │   ├ auth.py
│   │   ├ decision.py
│   │   └ analysis.py
│   │
│   ├ models.py
│   ├ schema.py
│   ├ crud.py
│   ├ database.py
│   └ main.py
│
├ dashboard
│   └ streamlit_app.py
│
├ requirements.txt
└ README.md
```

---

# Local Setup

Clone the repository

```
git clone https://github.com/Satadru03/human-free-will-erosion-engine.git
cd human-free-will-erosion-engine
```

Install dependencies

```
pip install -r requirements.txt
```

Set environment variable

```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

Run backend

```
uvicorn app.main:app --reload
```

Run dashboard

```
streamlit run dashboard/streamlit_app.py
```

---

# Future Improvements

Possible extensions

* time-of-day behavior modeling
* reinforcement learning behavior prediction
* anomaly detection in decision patterns
* habit break detection
* multi-user behavioral comparisons
* Markov transition graph visualization

---

# Author

Satadru Halder
BTech Electronics & Communication Engineering
IIIT Kalyani

GitHub
[https://github.com/Satadru03](https://github.com/Satadru03)

---

# Research Idea Behind the Project

Most ML systems predict external outcomes such as:

* spam detection
* recommendation systems
* fraud detection

This project explores a different direction:

**Can human behavioral freedom decrease as habits form?**

The Human Free Will Erosion Engine attempts to model this concept computationally.

---

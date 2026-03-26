# Human Free Will Erosion Engine

A behavioral analytics system that detects **habit loops and increasing predictability in human decision patterns over time**.

The system logs user actions, analyzes behavioral entropy and predictability, and estimates a **Free Will Index** using statistical analysis, Markov transition modeling, and behavioral simulation.

---

# Live Demo

Dashboard: 
[https://human-free-will-erosion-dashboard.onrender.com/](https://human-free-will-erosion-dashboard.onrender.com/)

API Documentation:
[https://human-free-will-api.onrender.com/docs](https://human-free-will-api.onrender.com/docs)

---

## Note on First Load

The backend is hosted on Render's free tier, which may put the API to sleep after inactivity.

If the dashboard does not load immediately, open the API documentation once to wake the server:

https://human-free-will-api.onrender.com/docs

After the API wakes up, the dashboard will function normally.

---

## Dashboard Walkthrough

Below are some screenshots demonstrating the main features of the system.

---

### 1. User Registration

Users can create an account to start logging behavioral decisions.

![Register](images/register.png)

---

### 2. User Login

Authentication is handled using JWT tokens.

![Login](images/login.png)

---

### 3. Log a Decision

Users log actions with domain and timestamp.

![Log Decision](images/log_decision.png)

---

### 4. Recent Decisions

Shows recently logged decisions with options to edit or delete.

![Recent Decisions](images/recent_decisions.png)

---

### 5. Filter Decisions

Users can filter historical decisions by date range.

![Filter Decisions](images/filter_decisions.png)

---

### 6. Entropy Trend

Visualizes how behavioral entropy changes over time.

![Entropy Trend Graph](images/entropy_trend_graph.png)

---

### 7. Entropy Trend Table

Shows daily entropy metrics in tabular format.

![Entropy Trend Table](images/entropy_trend_table.png)

---

### 8. Action Frequency

Displays the most frequent actions recorded by the system.

![Action Frequency Graph](images/action_frequency_graph.png)

---

### 9. Action Frequency Table

Tabular view of action counts.

![Action Frequency Table](images/action_frequency_table.png)

---

### 10. Next Action Prediction and Behavior Simulation

Predicts the most likely next action based on historical decision sequences and simulates future decision patterns using the learned Markov model.

The simulation shows:

* predicted 24-hour predictability
* dominant habit loop
* simulated future action sequence

![Next Action Prediction and Behavior Simulation](images/next_action_prediction.png)

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

> Can human decision patterns become increasingly predictable as habits form?

---

# Potential Applications

Although this project is demonstrated using personal decision logs, the underlying behavior analytics engine can be applied in several domains.

### Digital Wellbeing Apps
Platforms that track screen time or habits could detect unhealthy behavioral loops such as:

phone → instagram → youtube → phone → instagram

The system can identify when behavior becomes highly predictable and notify users.

### Productivity Analytics
Productivity tools could analyze routines and detect repetitive work patterns such as:

email → slack → email → slack

This may indicate inefficient context switching.

### Behavioral Research
Researchers studying human behavior could use entropy metrics to quantify behavioral diversity and habit formation.

### Recommendation Systems
Platforms could adapt recommendations based on predicted next actions derived from behavioral patterns.

---

## What This Project Does (Simple Explanation)

Every day we make hundreds of small decisions:

* waking up
* eating
* scrolling social media
* studying
* watching videos
* exercising

Over time, many of these actions become **habits**.

This project tries to answer a question:

**How predictable does a person's behavior become over time?**

The system works like this:

1. You log your daily actions.
2. The system analyzes how repetitive your behavior is.
3. It calculates how predictable your next action might be.
4. It estimates a **Free Will Index** — a number that represents how routine your behavior has become.

Example:

If your behavior looks like this:

```
Day 1: wake_up → phone → study → gym → dinner → youtube → sleep
Day 2: wake_up → phone → study → gym → dinner → youtube → sleep
Day 3: wake_up → phone → study → gym → dinner → youtube → sleep

Result:
Predictability: High
Free Will Index: Low
Habit Loop Detected
```

The system will detect that your behavior is becoming **highly predictable**.

It will then estimate:

* how repetitive your behavior is
* what you are likely to do next
* whether you are stuck in a habit loop

Suppose a user logs the following actions:

```
study → youtube → study → youtube → study → youtube
```

The system detects a repeating pattern and predicts:

```
Next likely action: study
Confidence: 0.67
```

This means the behavior is forming a **habit loop**.

---

## Metrics Explained Simply

### Entropy

Entropy measures **how varied your behavior is**.

* High entropy → many different actions
* Low entropy → repeating the same actions

---

### Predictability

Predictability measures **how easy it is to guess your next action**.

* High predictability → strong routines
* Low predictability → spontaneous behavior

---

### Free Will Index

The Free Will Index is an experimental metric that estimates **how much freedom your behavior has**.

* Higher value → more diverse behavior
* Lower value → stronger habits and routines

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

Higher entropy → varied behavior
Lower entropy → repetitive behavior

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
 "next_action": "study",
 "confidence": 0.67
}
```

---

# Behavior Simulation

The engine can simulate **future behavioral sequences** using the Markov model.

Query parameter

```
steps (int)
```

Number of future actions to simulate.

Simulation outputs

* predicted predictability
* dominant habit loop
* simulated future action sequence

Endpoint

```
GET /analysis/simulate
```

Example request

```
GET /analysis/simulate?steps=10
```

Example output

```json
{
 "predictability_24h": 0.78,
 "dominant_loop": ["study", "youtube", "study"],
 "simulated_sequence": [
  "study",
  "youtube",
  "study",
  "youtube",
  "study",
  "youtube"
 ]
}
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

Full API docs: [https://human-free-will-api.onrender.com/docs](https://human-free-will-api.onrender.com/docs)

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

# Quick Start

1. Open the dashboard  
2. Create an account  
3. Log daily decisions  
4. View entropy and predictability trends  
5. Explore habit loops and next-action predictions

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

Create a `.env` file in the root directory and add:

```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your_secret_key_here
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

# Limitations

- The model assumes reasonably continuous user logging.
- Large gaps between logged actions (e.g., skipping multiple activities) can introduce misleading transitions.
- Predictability scores may be unreliable for sparse or short sequences.

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

## Author

Satadru Halder

---

## License

MIT License

---

## Research Idea Behind the Project

Most ML systems predict external outcomes such as:

* spam detection
* recommendation systems
* fraud detection

This project explores a different direction:

**Can human behavioral freedom decrease as habits form?**

The Human Free Will Erosion Engine attempts to model this concept computationally.

---

# Smart-Sleep-Cycle-Alarm
Proof of concept for smart wake up alarm that wakes up the user when they are in their lightest sleep schedule during a chosen wakeup window, determined by tracking the user's heart rate. (Heart rate data is generated for this project as we did not have the time / resources to figure out a wearable tracking solution).

A Flask-based web app that simulates heart-rate tracking and triggers an alarm during a configurable wake window based on estimated sleep cycle depth.

ChatGPT was used to help write the README and the HTML.
Gemini was used to write app.py and sensor.py.
The rest of the code was written by the team. 

## Features

- Set **earliest** and **latest** wake-up times in a browser UI
- Simulated heart-rate sensor stream (`sensor.py`)
- Sleep-cycle estimation using EMA logic (`file1.py`)
- Background nap-monitoring thread (`app.py`)
- Alarm trigger + stop flow in the frontend (`index.html`)

## Project Structure
.
├── app.py           # Flask app, routes, nap thread logic
├── file1.py         # Sleep cycle detection + wake decision logic
├── sensor.py        # Simulated heart-rate generator
├── templates/
│   └── index.html   # Frontend UI
└── static/
    └── alarm.mp3    # Alarm sound

How It Works: 
User selects Earliest Wake and Latest Wake.
Frontend calculates minutes from now and sends:
min_nap
max_nap
Strict_mode
Backend starts a background thread:
Generates simulated HR every 2 seconds
Computes cycle from recent HR values
Triggers wake-up when:
current time is past min_nap, and
cycle meets wake condition (or max time reached)
Frontend polls /check_status and plays alarm when status becomes wake_up.

Sleep Cycle Logic:
Uses exponential moving average (EMA) of HR values.
Compares EMA to current HR (hr_diff) to map to cycle levels 0-3.
should_wake_up():
strict_mode=True: wakes when cycle < 2
strict_mode=False: wakes when cycle < 3

Requirements:
Python 3.8+
Flask

Installation:
pip install flask
Run:
python app.py
Then open (using follow link): http://127.0.0.1:5000


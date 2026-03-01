from flask import Flask, render_template, request, jsonify, send_from_directory
import threading
import time
import os

# Your external logic files
from file1 import get_sleep_cycle, should_wake_up 
from sensor import generate_simulated_hr 

app = Flask(__name__)

# --- GLOBAL CONFIG & STATE ---
ALPHA_HR = 0.3
nap_thread = None
nap_status = "inactive" # Statuses: inactive, active, wake_up

def start_nap_timer(min_nap, max_nap, strict_mode):
    """Background thread that monitors sleep and prints progress."""
    global nap_status
    nap_status = "active"
    
    start_time = time.time()
    wake_time_min = start_time + (min_nap * 60)
    end_time = start_time + (max_nap * 60)
    
    hr_log = []
    
    print(f"\n--- NAP TRACKING STARTED ---")
    print(f"Target Window: {min_nap} to {max_nap} minutes.")

    while nap_status == "active":
        now = time.time()
        
        # Calculate elapsed time
        elapsed_seconds = int(now - start_time)
        minutes, seconds = divmod(elapsed_seconds, 60)
        
        # 1. Get new data from sensor.py
        hr_log = generate_simulated_hr(hr_log)
        
        # 2. Process data with file1.py
        cycle = get_sleep_cycle(hr_log, ALPHA_HR)
        
        # Log to terminal
        print(f"[Elapsed: {minutes:02d}:{seconds:02d}] HR: {hr_log[-1]} | Cycle: {cycle}")

        # 3. Check if wake window is open and conditions met
        if now >= wake_time_min:
            if should_wake_up(cycle, strict_mode) or now >= end_time:
                nap_status = "wake_up" 
                print(f"!!! WAKE CONDITION MET AT {minutes:02d}:{seconds:02d} !!!")
                break

        time.sleep(2) # Frequency of "sensor" checks

# --- ROUTES ---

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Explicitly serves files to avoid 403 Forbidden errors."""
    return send_from_directory('static', filename)

@app.route("/start_nap", methods=["POST"])
def start_nap():
    global nap_thread, nap_status
    if nap_status != "inactive":
        return jsonify({"status": "A nap is already in progress."}), 400

    data = request.json
    min_val = int(data.get("min_nap", 25))
    max_val = int(data.get("max_nap", 45))
    strict = bool(data.get("strict_mode", True))

    nap_thread = threading.Thread(
        target=start_nap_timer, 
        args=(min_val, max_val, strict),
        daemon=True
    )
    nap_thread.start()
    return jsonify({"status": f"Tracking started for {min_val}-{max_val} min."})

@app.route("/check_status")
def check_status():
    return jsonify({"status": nap_status})

@app.route("/stop_alarm", methods=["POST"])
def stop_alarm():
    global nap_status
    nap_status = "inactive"
    return jsonify({"status": "Alarm stopped."})

if __name__ == "__main__":
    # Localhost configuration
    app.run(debug=True, host='127.0.0.1', port=5000)
import time
import random
from playsound import playsound  # pip install playsound

from file1 import get_sleep_cycle, should_wake_up  # your first file with logic

# ---- CONFIG ----
MIN_NAP = 25  # minutes
MAX_NAP = 45  # minutes
STRICT_MODE = True  # change True for strict mode
ALPHA_HR = 0.3  # EMA smoothing factor

# Mock function to get heart rate data
def read_heart_rate():
    """
    Replace this with actual sensor reading.
    Returns a list of last N heart rate readings.
    """
    return [random.randint(60, 75) for _ in range(10)]

# Main nap function
def start_nap_timer(min_nap=MIN_NAP, max_nap=MAX_NAP, strict_mode=STRICT_MODE):
    start_time = time.time()
    end_time = start_time + max_nap * 60  # convert minutes to seconds
    wake_time_min = start_time + min_nap * 60

    print(f"Nap started! Target window: {min_nap}-{max_nap} minutes.")

    while True:
        now = time.time()

        # Read heart rate
        hr_values = read_heart_rate()
        sleep_cycle_number = get_sleep_cycle(hr_values, ALPHA_HR)
        print(f"Current sleep cycle number: {sleep_cycle_number}")

        # Check if it's time to wake up
        if now >= wake_time_min:
            if should_wake_up(sleep_cycle_number, strict_mode):
                print("Optimal wake point reached! Waking up...")
                playsound("alarm.mp3")
                break

        # Check if max nap time reached
        if now >= end_time:
            print("Max nap time reached. Waking up!")
            playsound("alarm.mp3")
            break

        # Wait 5 minutes before next check
        print("Sleeping for 5 minutes before next check...")
        time.sleep(5 * 60)  # 5 minutes

if __name__ == "__main__":
    start_nap_timer()
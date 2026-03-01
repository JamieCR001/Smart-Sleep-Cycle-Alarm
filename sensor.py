import random

def generate_simulated_hr(hr_log):
    """
    Simulates heart rate data collection.
    Adds a new value based on the previous one to simulate a trend.
    """
    if not hr_log:
        new_hr = random.randint(60, 75)
    else:
        # Subtle drift for more realistic simulation
        last_hr = hr_log[-1]
        new_hr = last_hr + random.randint(-2, 2)
    
    # Keep HR within a realistic resting range
    new_hr = max(55, min(95, new_hr))
    hr_log.append(new_hr)
    
    # Return the last 10 readings for the sleep cycle logic
    return hr_log[-10:]
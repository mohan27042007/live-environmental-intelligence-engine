import time
import random

# pull tuning parameters from config rather than hardcoding
from src.config import SPIKE_PROBABILITY, DRIFT_RATE, TIME_FORMAT, SLEEP_INTERVAL

# Environmental sensor state (globals for prototype)
pm25 = 35.0
co2 = 420.0
temp = 25.0

# seed for reproducibility during demos
random.seed(42)


def generate_reading():
    global pm25, co2, temp
    
    # Small random noise each iteration
    pm25 += random.uniform(-2, 2)
    co2 += random.uniform(-8, 8)
    temp += random.uniform(-0.5, 0.5)
    
    # slow upward drift to simulate changing baseline
    pm25 += DRIFT_RATE * 0.1
    co2 += DRIFT_RATE * 1.0
    temp += DRIFT_RATE * 0.02
    
    # Occasional anomaly spike with correlated perturbation
    if random.random() < SPIKE_PROBABILITY:
        pm25 += random.uniform(30, 60)
        co2 += random.uniform(5, 15)
        temp += random.uniform(0.5, 1.5)
    
    # Clamp to realistic ranges (don't squash anomalies excessively)
    pm25 = max(10, min(100, pm25))
    co2 = max(350, min(650, co2))
    temp = max(20, min(40, temp))

    timestamp = time.strftime(TIME_FORMAT, time.localtime())
    
    return {
        'pm25': round(pm25, 1),
        'co2': round(co2, 1),
        'temp': round(temp, 1),
        'timestamp': timestamp
    }

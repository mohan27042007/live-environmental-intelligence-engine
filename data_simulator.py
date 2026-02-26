import time
import random

# Environmental sensor state
pm25 = 35.0
co2 = 420.0
temp = 25.0


def generate_reading():
    global pm25, co2, temp
    
    # Small random changes each iteration
    pm25 += random.uniform(-2, 2)
    co2 += random.uniform(-8, 8)
    temp += random.uniform(-0.5, 0.5)
    
    # Occasional anomaly spike
    if random.random() < 0.05:
        pm25 += random.uniform(30, 60)
    
    # Clamp to realistic ranges
    pm25 = max(10, min(80, pm25))
    co2 = max(350, min(600, co2))
    temp = max(20, min(35, temp))
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    return {
        'pm25': round(pm25, 1),
        'co2': round(co2, 1),
        'temp': round(temp, 1),
        'timestamp': timestamp
    }

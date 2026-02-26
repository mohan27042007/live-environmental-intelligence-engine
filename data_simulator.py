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
    
    # Clamp to realistic ranges
    pm25 = max(10, min(80, pm25))
    co2 = max(350, min(600, co2))
    temp = max(20, min(35, temp))
    
    return {
        'pm25': round(pm25, 1),
        'co2': round(co2, 1),
        'temp': round(temp, 1),
        'timestamp': time.time()
    }


def stream_data():
    while True:
        reading = generate_reading()
        print(f"PM2.5: {reading['pm25']} µg/m³ | CO2: {reading['co2']} ppm | Temp: {reading['temp']}°C")
        time.sleep(1)


if __name__ == "__main__":
    stream_data()

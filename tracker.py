# tracker.py
import time
from utils.sensors import get_environment_data

def main():
    while True:
        data = get_environment_data()
        if data:
            print(f"Humidity: {data['humidity']:.2f}% | Temp: {data['temp']:.2f}°C | CPU Temp: {data['cpu_temp']:.2f}°C")
        else:
            print("Sensor read error.")
        time.sleep(10)

if __name__ == "__main__":
    main()

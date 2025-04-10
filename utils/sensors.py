# sensors.py
import os

def read_sensor_value(path):
    try:
        with open(path, "r") as file:
            return float(file.read().strip())
    except Exception as e:
        print(f"Sensor error reading {path}: {e}")
        return None

def get_environment_data():
    humidity_raw_path = "/sys/bus/iio/devices/iio:device0/in_humidityrelative_raw"
    humidity_scale_path = "/sys/bus/iio/devices/iio:device0/in_humidityrelative_scale"
    temp_raw_path = "/sys/bus/iio/devices/iio:device0/in_temp_raw"
    temp_scale_path = "/sys/bus/iio/devices/iio:device0/in_temp_scale"

    humidity_raw = read_sensor_value(humidity_raw_path)
    humidity_scale = read_sensor_value(humidity_scale_path)
    temp_raw = read_sensor_value(temp_raw_path)
    temp_scale = read_sensor_value(temp_scale_path)

    if None in (humidity_raw, humidity_scale, temp_raw, temp_scale):
        return None

    humidity = humidity_raw * humidity_scale
    temp = temp_raw * temp_scale

    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            cpu_temp = float(f.read().strip()) / 1000.0
    except Exception as e:
        print(f"CPU Temp error: {e}")
        cpu_temp = 0.0

    # Less aggressive temperature compensation
    adjusted_temp = temp - ((cpu_temp - temp) / 5.0)

    return {
        "humidity": humidity,
        "temp": adjusted_temp,
        "cpu_temp": cpu_temp
    }

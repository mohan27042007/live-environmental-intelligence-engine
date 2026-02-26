import time
import pathway as pw

from data_simulator import generate_reading
from anomaly_model import AnomalyDetector


def reading_stream():
    while True:
        yield generate_reading()
        time.sleep(1)


def main():
    detector = AnomalyDetector(buffer_size=30)

    def detect(pm25):
        detector.add_value(pm25)
        return detector.is_anomaly(pm25)

    src = pw.io.python.read(reading_stream, schema={
        'timestamp': str,
        'pm25': float,
        'co2': float,
        'temp': float,
    }, mode='streaming')

    tbl = src.with_columns(anomaly=pw.apply(detect, src.pm25))

    pw.io.print(tbl)
    pw.run()


if __name__ == '__main__':
    main()

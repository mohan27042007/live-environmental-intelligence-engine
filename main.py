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

    def detect(pm25, co2, temp):
        # predict first, then update buffer
        anomaly = detector.is_anomaly(pm25, co2, temp)
        detector.add_value(pm25, co2, temp)
        return anomaly

    src = pw.io.python.read(reading_stream, schema={
        'timestamp': str,
        'pm25': float,
        'co2': float,
        'temp': float,
    }, mode='streaming')

    tbl = src.with_columns(
        anomaly=pw.apply(
            lambda p, c, t: detect(p, c, t),
            src.pm25,
            src.co2,
            src.temp
        )
    )

    pw.io.print(tbl)
    pw.run()


if __name__ == '__main__':
    main()

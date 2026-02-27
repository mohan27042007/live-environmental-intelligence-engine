import time
import logging
import pathway as pw

from src.data_simulator import generate_reading
from src.anomaly_model import AnomalyDetector
from src.config import SLEEP_INTERVAL, TIME_FORMAT


def reading_stream():
    while True:
        yield generate_reading()
        time.sleep(SLEEP_INTERVAL)


class ReadingSubject(pw.io.python.ConnectorSubject):
    """ConnectorSubject wrapper that feeds simulated readings into Pathway."""
    def run(self) -> None:
        # run in a separate thread inside Pathway; feed values using `next`
        while True:
            r = generate_reading()
            # next expects keyword args compatible with the schema passed to read
            self.next(timestamp=r['timestamp'], pm25=r['pm25'], co2=r['co2'], temp=r['temp'])
            time.sleep(SLEEP_INTERVAL)


class ReadingSchema(pw.Schema):
    timestamp: str
    pm25: float
    co2: float
    temp: float


def main():
    detector = AnomalyDetector()

    def detect(pm25, co2, temp):
        anomaly = detector.is_anomaly(pm25, co2, temp)
        detector.add_value(pm25, co2, temp)
        if anomaly:
            print(f"[{time.strftime(TIME_FORMAT)}] ALERT: environmental anomaly detected")
        return anomaly

    # Use a ConnectorSubject instance (required by current Pathway API)
    src = pw.io.python.read(ReadingSubject(), schema=ReadingSchema, mode='streaming')

    tbl = src.with_columns(
        anomaly=pw.apply(
            lambda p, c, t: detect(p, c, t),
            src.pm25,
            src.co2,
            src.temp
        )
    )

    # reduce verbosity from pathway internals
    logging.getLogger("pathway").setLevel(logging.ERROR)

    # show only the columns we care about and print update stream
    tbl = tbl.select(src.timestamp, src.pm25, src.co2, src.temp, tbl.anomaly)
    pw.debug.compute_and_print_update_stream(tbl)
    pw.run()


if __name__ == '__main__':
    main()

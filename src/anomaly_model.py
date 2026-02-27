from sklearn.ensemble import IsolationForest

from src.config import BUFFER_SIZE, CONTAMINATION, RETRAIN_INTERVAL


class AnomalyDetector:
    def __init__(self):
        self.buffer_size = BUFFER_SIZE
        self.contamination = CONTAMINATION
        self.retrain_interval = RETRAIN_INTERVAL

        self.buffer = []
        self.model = None
        self.trained = False
        self.samples_since_retrain = 0

    def add_value(self, pm25, co2, temp):
        self.buffer.append([pm25, co2, temp])
        if len(self.buffer) > self.buffer_size:
            self.buffer.pop(0)

        if not self.trained:
            if len(self.buffer) == self.buffer_size:
                self._train_model()
                self.samples_since_retrain = 0
            return

        self.samples_since_retrain += 1
        if self.samples_since_retrain >= self.retrain_interval:
            self._train_model()
            self.samples_since_retrain = 0

    def _train_model(self):
        self.model = IsolationForest(
            contamination=self.contamination,
            random_state=42,
        )
        self.model.fit(self.buffer)
        self.trained = True

    def is_anomaly(self, pm25, co2, temp):
        if not self.trained:
            return False
        pred = self.model.predict([[pm25, co2, temp]])
        return bool(pred[0] == -1)


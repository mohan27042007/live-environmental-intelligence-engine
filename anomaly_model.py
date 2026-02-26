from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self, buffer_size=30):
        self.buffer_size = buffer_size
        self.buffer = []
        self.model = None
        self.trained = False

    def add_value(self, value):
        self.buffer.append(value)
        if len(self.buffer) > self.buffer_size:
            self.buffer.pop(0)
        if len(self.buffer) == self.buffer_size and not self.trained:
            # fit once on baseline
            X = [[v] for v in self.buffer]
            self.model = IsolationForest(contamination=0.05, random_state=42)
            self.model.fit(X)
            self.trained = True

    def is_anomaly(self, value):
        if not self.trained:
            return False
        pred = self.model.predict([[value]])
        return bool(pred[0] == -1)


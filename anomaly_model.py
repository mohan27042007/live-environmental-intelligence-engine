from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self, buffer_size=30, contamination=0.05):
        self.buffer_size = buffer_size
        self.buffer = []
        self.model = None
        self.trained = False
        self.contamination = contamination

    def add_value(self, pm25, co2, temp):
        # append new point and keep rolling buffer
        self.buffer.append([pm25, co2, temp])
        if len(self.buffer) > self.buffer_size:
            self.buffer.pop(0)

        if not self.trained:
            # still collecting baseline data
            print(f"collecting baseline data ({len(self.buffer)}/{self.buffer_size})")
        
        if len(self.buffer) == self.buffer_size:
            if not self.trained:
                self._train_model()
            else:
                # periodic retraining on sliding window
                self._train_model()

    def _train_model(self):
        print("training isolation forest on current buffer")
        self.model = IsolationForest(
            contamination=self.contamination,
            random_state=42
        )
        self.model.fit(self.buffer)
        if not self.trained:
            print("model trained")
        self.trained = True

    def is_anomaly(self, pm25, co2, temp):
        if not self.trained:
            return False
        pred = self.model.predict([[pm25, co2, temp]])
        return bool(pred[0] == -1)


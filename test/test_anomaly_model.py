from src.anomaly_model import AnomalyDetector


def test_detector_initial_state():
    detector = AnomalyDetector()
    assert detector.trained is False


def test_training_after_buffer_fill():
    detector = AnomalyDetector()

    # Fill buffer to trigger initial training
    for _ in range(30):
        detector.add_value(10.0, 400.0, 25.0)

    assert detector.trained is True


def test_is_anomaly_before_training():
    detector = AnomalyDetector()
    result = detector.is_anomaly(10.0, 400.0, 25.0)
    assert result is False
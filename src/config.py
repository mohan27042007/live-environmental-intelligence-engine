# Configuration constants for the environmental intelligence engine

# ---------------------------------------------------------------------------
# Model parameters
BUFFER_SIZE = 30           # number of readings to keep in sliding window
RETRAIN_INTERVAL = 50      # how many new samples trigger a retrain
CONTAMINATION = 0.05       # expected fraction of anomalies for IsolationForest

# ---------------------------------------------------------------------------
# Simulator parameters
SPIKE_PROBABILITY = 0.05    # chance of a pollution spike on each tick
DRIFT_RATE = 0.01          # slow upward drift applied per tick
SLEEP_INTERVAL = 1         # seconds between generated readings

# ---------------------------------------------------------------------------
# Logging / display settings
TIME_FORMAT = "%H:%M:%S"  # format used for console timestamps


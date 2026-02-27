"""Launcher removed.

This repository uses a package layout with the application entrypoint in
``src/main.py``. To run the application use:

    python -m src.main

The top-level launcher was intentionally removed to keep the package layout
clean and avoid duplicate entrypoints.
"""

if __name__ == "__main__":
    print("This launcher has been removed. Run: python -m src.main")

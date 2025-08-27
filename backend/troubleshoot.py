import os
import sys

print("--- Environment Variables ---")
for key, value in os.environ.items():
    if "BLINKA" in key:
        print(f"{key}={value}")

print("\n--- Python Board Import ---")
try:
    import board
    print("board imported successfully.")
except NotImplementedError as e:
    print(f"Error importing board: {e}")
except Exception as e:
    print(f"Unexpected error importing board: {e}")

print("\n--- adafruit_blinka version ---")
try:
    import adafruit_blinka
    print(f"adafruit_blinka version: {adafruit_blinka.__version__}")
except AttributeError:
    print("adafruit_blinka has no __version__ attribute.")
except Exception as e:
    print(f"Unexpected error getting adafruit_blinka version: {e}")

print("\n--- adafruit_platformdetect version ---")
try:
    import adafruit_platformdetect
    print(f"adafruit_platformdetect version: {adafruit_platformdetect.__version__}")
except AttributeError:
    print("adafruit_platformdetect has no __version__ attribute.")
except Exception as e:
    print(f"Unexpected error getting adafruit_platformdetect version: {e}")

print("\n--- adafruit_platformdetect board ID ---")
try:
    from adafruit_platformdetect.constants import boards
    print(f"Generic Linux Board ID: {boards.generic_linux.id}")
except AttributeError:
    print("adafruit_platformdetect.constants.boards has no 'generic_linux' attribute.")
except Exception as e:
    print(f"Unexpected error getting board ID: {e}")

print("\n--- Troubleshooting complete ---")

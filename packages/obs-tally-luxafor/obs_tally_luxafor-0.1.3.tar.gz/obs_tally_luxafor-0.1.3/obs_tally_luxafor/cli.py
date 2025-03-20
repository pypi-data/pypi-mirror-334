#!/usr/bin/env python3
"""
Entry point for obs-tally-luxafor integration.

Listens for scene changes from OBS via obsws-python and updates the Luxafor LED color.
"""

import time
import logging
import obsws_python as obs
from .client import LuxaforClient

# Configuration for Luxafor API
BASE_URL = "http://127.0.0.1:5383"
SECRET_TOKEN = "luxafor"

# Create Luxafor client instance
luxafor = LuxaforClient(BASE_URL, SECRET_TOKEN)

# OBS WebSocket configuration
HOST = "localhost"
PORT = 4455  # default for OBS WebSocket v5
PASSWORD = "password"

def on_current_program_scene_changed(data):
    """
    Callback function for when the current program scene changes in OBS.

    Args:
        data (object): Data object containing the scene name.
    """
    logging.info(f"Scene changed to: {data.scene_name}")
    if data.scene_name == "scene":
        if not luxafor.change_color("#FF0000"):
            logging.error("Failed to change Luxafor color to red.")
    else:
        if not luxafor.change_color("#00FF00"):
            logging.error("Failed to change Luxafor color to green.")

def main():
    """
    Initialize the OBS event client and keep the integration running.
    """
    # Test Luxafor connectivity with a quick color change
    if not luxafor.change_color("#FFFFFF"):
        logging.error("Failed to communicate with Luxafor device. Check connection and configuration.")
    else:
        logging.info("Luxafor device is connected successfully.")

    # Attempt to connect to OBS WebSocket
    try:
        client = obs.EventClient(host=HOST, port=PORT, password=PASSWORD, timeout=10)
    except Exception as e:
        logging.exception("Failed to connect to OBS WebSocket. Is OBS running?")
        return

    client.callback.register(on_current_program_scene_changed)
    logging.info("Connected to OBS WebSocket and registered callback.")

    try:
        logging.info("obs-tally-luxafor integration running. Press Ctrl+C to exit.")
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received. Exiting...")
    except Exception as e:
        logging.exception("An unexpected error occurred during the integration loop.")
    finally:
        client.disconnect()
        logging.info("Disconnected from OBS WebSocket.")

if __name__ == "__main__":
    main()

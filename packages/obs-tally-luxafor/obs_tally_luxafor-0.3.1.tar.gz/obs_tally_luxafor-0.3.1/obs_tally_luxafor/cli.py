#!/usr/bin/env python3
"""
Entry point for obs-tally-luxafor integration.

Listens for scene changes from OBS via obsws-python and updates the Luxafor LED color.
"""

import time
import logging
import argparse
import obsws_python as obs
from .client import LuxaforClient

# Set up logging for our script
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
# Suppress verbose logging from external libraries
logging.getLogger("websocket").setLevel(logging.CRITICAL)
logging.getLogger("obsws_python").setLevel(logging.CRITICAL)

# Global variables to be set after parsing arguments
luxafor = None
trigger_scene_name = None

def parse_args():
    parser = argparse.ArgumentParser(
        description='OBS Tally Luxafor integration. Listens for scene changes from OBS and updates the Luxafor LED color.'
    )
    parser.add_argument(
        '--base-url',
        default="http://127.0.0.1:5383",
        help='Base URL for Luxafor API (default: %(default)s)'
    )
    parser.add_argument(
        '--secret-token',
        default="luxafor",
        help='Secret token for Luxafor API (default: %(default)s)'
    )
    parser.add_argument(
        '--host',
        default="localhost",
        help='OBS WebSocket host (default: %(default)s)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=4455,
        help='OBS WebSocket port (default: %(default)s)'
    )
    parser.add_argument(
        '--password',
        default="password",
        help='OBS WebSocket password (default: %(default)s)'
    )
    parser.add_argument(
        '--scene-name',
        default="scene",
        help='Scene name that should trigger the red color (default: %(default)s)'
    )
    return parser.parse_args()

def on_current_program_scene_changed(data):
    """
    Callback function for when the current program scene changes in OBS.

    Args:
        data (object): Data object containing the scene name.
    """
    logging.info("Scene changed to: %s", data.scene_name)
    if data.scene_name == trigger_scene_name:
        logging.info("Scene '%s' matches trigger scene. Setting Luxafor LED to red (#FF0000).", trigger_scene_name)
        if not luxafor.change_color("#FF0000"):
            logging.error("Failed to change Luxafor color to red.")
        else:
            logging.info("Successfully changed Luxafor color to red.")
    else:
        logging.info("Scene '%s' does not match trigger scene '%s'. Setting Luxafor LED to green (#00FF00).", data.scene_name, trigger_scene_name)
        if not luxafor.change_color("#00FF00"):
            logging.error("Failed to change Luxafor color to green.")
        else:
            logging.info("Successfully changed Luxafor color to green.")

def main():
    """
    Initialize the OBS event client and keep the integration running.
    """
    global luxafor, trigger_scene_name

    args = parse_args()
    trigger_scene_name = args.scene_name

    # Create Luxafor client instance using command line arguments
    luxafor = LuxaforClient(args.base_url, args.secret_token)

    # Test Luxafor connectivity with a quick color change
    try:
        logging.info("Testing Luxafor connectivity by setting color to white (#FFFFFF).")
        if not luxafor.change_color("#FFFFFF"):
            logging.error("Failed to communicate with Luxafor device. Check connection and configuration.")
        else:
            logging.info("Luxafor device is connected successfully and set to white.")
    except Exception as e:
        logging.error("Error communicating with Luxafor device: %s", e)

    # Attempt to connect to OBS WebSocket using provided arguments
    try:
        logging.info("Connecting with parameters: host='%s' port=%d password='%s'", args.host, args.port, args.password)
        client = obs.EventClient(host=args.host, port=args.port, password=args.password, timeout=10)
    except ConnectionRefusedError:
        logging.error("OBS WebSocket connection refused. Is OBS running and the WebSocket plugin enabled?")
        return
    except Exception as e:
        logging.error("Failed to connect to OBS WebSocket: %s", e)
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
        logging.error("An unexpected error occurred during the integration loop: %s", e)
    finally:
        client.disconnect()
        logging.info("Disconnected from OBS WebSocket.")

if __name__ == "__main__":
    main()

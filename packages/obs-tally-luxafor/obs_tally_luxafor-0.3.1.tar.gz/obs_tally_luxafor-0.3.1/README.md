# obs-tally-luxafor

**obs-tally-luxafor** is a Python package that integrates OBS (Open Broadcaster Software) with Luxafor LED devices. It listens for scene changes via OBS WebSocket and automatically updates the color of your Luxafor device.

## Features

- **OBS Integration:** Uses [obsws-python](https://pypi.org/project/obsws-python/) to listen for scene changes.
- **Luxafor Control:** Provides a simple API client to control Luxafor LED devices (brightness, color, patterns).
- **Command-Line Configuration:** Customize connection parameters and behavior via command-line arguments.

## Installation

To install the package in development (editable) mode:

```bash
cd obs-tally-luxafor
pip install -e .
```

After publishing to PyPI, you can install it via:

```bash
pip install obs-tally-luxafor
```

## Configuration

The package can be configured both by modifying default values in the source code and via command-line arguments when launching the integration. The available command-line parameters include:

### Luxafor API:

- **`--base-url`**  
  The URL of your Luxafor API server (default: `http://127.0.0.1:5383`).

- **`--secret-token`**  
  The secret token for the Luxafor API (default: `luxafor`).

### OBS WebSocket:

- **`--host`**  
  OBS host (default: `localhost`).

- **`--port`**  
  Port for OBS WebSocket (default: `4455` for OBS WebSocket v5).

- **`--password`**  
  Password for OBS WebSocket (default: `password`).

### Scene Trigger:

- **`--scene-name`**  
  The scene name that should trigger the red LED color (default: `scene`). When the current program scene in OBS matches this value, the Luxafor LED will change to red. For any other scene, the LED will change to green.

## Usage

Once installed, run the integration using the command-line script:

```bash
obs-tally-luxafor [OPTIONS]
```

For example, to run with a custom scene name:

```bash
obs-tally-luxafor --scene-name "my_custom_scene"
```

To see all available options, run:

```bash
obs-tally-luxafor --help
```

This command will start the OBS event listener. When the current program scene changes, the package will update the Luxafor LED color accordingly, with detailed logs indicating which color is set and why.

## API Reference

### LuxaforClient

The `LuxaforClient` class (found in `obs_tally_luxafor/client.py`) provides methods to interact with your Luxafor device:

- **`change_color(color)`**  
  Changes the LED color to the specified hex value.

- **`play_pattern(pattern_id)`**  
  Plays a pre-defined lighting pattern on the device.

## Dependencies

- [requests](https://pypi.org/project/requests/)
- [obsws_python](https://pypi.org/project/obsws-python/)

## License

This project is licensed under the MIT License.

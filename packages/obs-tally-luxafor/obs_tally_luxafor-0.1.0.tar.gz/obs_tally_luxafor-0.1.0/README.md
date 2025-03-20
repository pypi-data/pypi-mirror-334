# obs-tally-luxafor

**obs-tally-luxafor** is a Python package that integrates OBS (Open Broadcaster Software) with Luxafor LED devices.
It listens for scene changes via OBS WebSocket and automatically updates the color of your Luxafor device.

## Features

- **OBS Integration:** Uses [obsws-python](https://pypi.org/project/obsws-python/) to listen for scene changes.
- **Luxafor Control:** Provides a simple API client to control Luxafor LED devices (brightness, color, patterns).

## Installation

To install the package in development (editable) mode:

```bash
cd obs-tally-luxafor
pip install -e .
```

After publishing to PyPI, you can install via:

```bash
pip install obs-tally-luxafor
```

## Configuration

The default configuration in `obs_luxafor/cli.py` includes:

- **Luxafor API:**
  - `BASE_URL`: The URL of your Luxafor API server (default: `http://127.0.0.1:5383`).
  - `SECRET_TOKEN`: The secret token for the Luxafor API (default: `luxafor`).

- **OBS WebSocket:**
  - `HOST`: OBS host (default: `localhost`).
  - `PORT`: Port for OBS WebSocket (default for OBS WebSocket v5 is `4455`).
  - `PASSWORD`: Password for OBS WebSocket (default: `password`).

Customize these settings as needed.

## Usage

Once installed, run the integration using the command-line script:

```bash
obs-tally-luxafor
```

This command will start the OBS event listener. When the current program scene changes, the package will change the Luxafor LED color accordingly.


## API Reference

### LuxaforClient

The `LuxaforClient` class (found in `obs_luxafor/client.py`) provides methods to interact with your Luxafor device:

- **`change_color(color)`**  
  Changes the LED color to the specified hex value.

- **`play_pattern(pattern_id)`**  
  Plays a pre-defined lighting pattern on the device.

## Dependencies

- [requests](https://pypi.org/project/requests/)
- [obsws_python](https://pypi.org/project/obsws-python/)

## License

This project is licensed under the MIT License.

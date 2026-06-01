# META Power Station Microcontroller

## Overview

This repository provides a lightweight Python implementation for polling a Shelly-based power monitoring device over BLE and optionally publishing results via MQTT.

The `/app` package is organized by responsibility:

- `app/app.py` - application entry point that initializes device setup and starts the polling loop.
- `app/mqtt/publisher.py` - MQTT helper layer for building payloads and publishing messages to a broker.
- `app/shelley/rpc.py` - Shelly BLE RPC utilities, including payload serialization, response parsing, and BLE characteristic UUID definitions.
- `app/shelley/poll.py` - Shelly device polling layer that connects over BLE, sends RPC calls, retries on failure, and supports continuous status polling.

The `/scripts` folder contains a proof-of-concept script:

- `scripts/polling_shelley.py` - a standalone example that demonstrates BLE connection, RPC negotiation, device configuration, relay control, and continuous status polling.

## Quickstart

### Windows PowerShell

Create and activate a virtual environment, then install the runtime dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the app with:

```powershell
python -m app.app
```

### Linux / macOS

### Creating the virtual environment

Create and activate a virtual environment, then install the runtime dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

#### Activating the virtual environment

```bash
source .venv/bin/activate
```

Run the app with:

```bash
python -m app.app
```

#### Configuration

On intial setup, enter corrosponding values that will be saved into the config file:

- Building ID (Format: 'station_\<name\>')
- MQTT Broker Address (default: 192.168.1.115)
- Broker Port (default: 1883)
- Quality of Service level (0, 1, or 2; default: 1)
- MQTT Retain Flag (true or false; default: false)
- Shelley Device Address (no default, Bluetooth MAC Address, example: {config.shelley_address})
- Sleep Interval Seconds (default: 5 seconds)

After initial creation, you can update the device's config by editing the created file itself. Do this by using this command

```
cd <config filepath>
sudo nano config.py
```

## Running unit tests

Run all unit tests in the repository with pytest from the project root:


```bash
python -m pytest
```

If you are running on Windows PowerShell, use the same virtual environment activation commands from the quickstart section before executing tests.

## Running in test mode

The test_mode module is for testing code locally without a shelley device or MQTT publishing

To run the code in test mode, enter this command:

```
python -m app.test_mode
```

Then respond to the prompts dependant on how you want to test the code.

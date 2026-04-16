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

Create and activate a virtual environment, then install the runtime dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the app with:

```bash
python -m app.app
```



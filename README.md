# ChargeBridge

Minimal orchestrator for EV charging sessions using OCPP 1.6.

## Features
- `OCPPClient` for WebSocket communication with OCPP 1.6 chargers
- `ChargingSession` dataclass to manage meter readings and transaction IDs
- `central.py` orchestrator for demo start/stop session flow

## Conda Installation

1. Install [Miniconda or Anaconda](https://docs.conda.io/en/latest/miniconda.html).
2. Create and activate an environment and install dependencies:

```bash
conda create -n chargebridge python=3.12
conda activate chargebridge
pip install websockets
```

## Quick Start

Run the demo orchestrator after the environment is prepared:

```bash
python charging_controller.py
```

## Local Testing

1. Start an OCPP server or simulator (e.g., `chargeforge-sim`):

```bash
python central.py  # from the simulator project
```

2. Point the client to the local server in `charging_controller.py`:

```python
client = OCPPClient("ws://127.0.0.1:9000/ocpp", "CP_1")
```

3. Run the orchestrator:

```bash
python charging_controller.py
```

## Testing with a Remote Server

1. Ensure the remote machine exposes the OCPP port (e.g., `9000`).
2. Update `charging_controller.py` with the real IP address:

```python
client = OCPPClient("ws://<real-ip>:9000/ocpp", "CP_1")
```

3. Start the client:

```bash
python charging_controller.py
```

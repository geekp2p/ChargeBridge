# ChargeBridge

Minimal orchestrator for EV charging sessions using OCPP 1.6j.
The WebSocket subprotocol can be customized for later OCPP versions,
and the project primarily targets Gresgying 120–180 kW DC charging
stations while remaining flexible for other models.

## Features
- `OCPPClient` for WebSocket communication with OCPP 1.6j and newer versions
- `ChargingSession` dataclass to manage meter readings and transaction IDs
- `central.py` orchestrator for demo start/stop session flow
- Primarily tested with Gresgying 120–180 kW DC chargers but adaptable to other stations

## Conda Installation

1. Install [Miniconda or Anaconda](https://docs.conda.io/en/latest/miniconda.html).
2. Create and activate an environment and install dependencies:

```bash
conda create -n chargebridge python=3.12
conda activate chargebridge
pip install websockets ocpp fastapi uvicorn
```

## Quick Start

Run the demo orchestrator after the environment is prepared:

```bash
python charging_controller.py
```

## Local Testing

1. Start the included `central.py` server or any OCPP simulator (e.g., `chargeforge-sim`):

```bash
python central.py
```

2. Point the client to the local server in `charging_controller.py` (note the Charge Point ID in the URL):

```python
client = OCPPClient(
    "ws://127.0.0.1:9000/ocpp/CP_1",
    "CP_1",
    ocpp_protocol="ocpp1.6",  # adjust for newer versions
    charger_model="Gresgying 120-180 kW DC",
)
```

3. Run the orchestrator:

```bash
python charging_controller.py
```

## Testing with a Remote Server

1. Ensure the remote machine exposes the OCPP port (e.g., `9000`).
2. Update `charging_controller.py` with the real IP address and include the Charge Point ID in the path:

```python
client = OCPPClient(
    "ws://<real-ip>:9000/ocpp/CP_1",
    "CP_1",
    ocpp_protocol="ocpp1.6",  # or another supported version
    charger_model="Gresgying 120-180 kW DC",
)
```

3. Start the client:

```bash
python charging_controller.py
```
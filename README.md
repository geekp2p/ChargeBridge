# ChargeBridge

Minimal orchestrator for EV charging sessions using OCPP 1.6.

## Features
- `OCPPClient` for WebSocket communication with OCPP 1.6 chargers
- `ChargingSession` dataclass to manage meter readings and transaction IDs
- `central.py` orchestrator for demo start/stop session flow

## Quick Start

```bash
pip install websockets
python central.py

import asyncio
import json
import uuid
from datetime import datetime

import websockets


class OCPPClient:
    """Minimal OCPP client for interacting with charging stations.

    The client targets OCPP 1.6j by default but the WebSocket subprotocol
    can be adjusted to support newer revisions.  It was written with
    Gresgying 120–180 kW DC stations in mind yet keeps messaging
    generic so other vendors and models can be supported as well.
    """

    def __init__(
        self,
        uri: str,
        charge_point_id: str,
        ocpp_protocol: str = "ocpp1.6",
        charger_model: str = "Gresgying 120-180 kW DC",
    ) -> None:
        self.uri = uri
        self.charge_point_id = charge_point_id
        self.ocpp_protocol = ocpp_protocol
        self.charger_model = charger_model
        self._ws: websockets.WebSocketClientProtocol | None = None
        self._heartbeat_task: asyncio.Task | None = None
        self._listener_task: asyncio.Task | None = None
        self._active_tx: dict | None = None
        self._last_meter: int = 0

    async def connect(self) -> None:
        """Establish a WebSocket connection and announce the charge point."""
        self._ws = await websockets.connect(self.uri, subprotocols=[self.ocpp_protocol])
        await self.boot_notification()
        self._listener_task = asyncio.create_task(self._listen())

    async def close(self) -> None:
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            self._heartbeat_task = None
        if self._listener_task:
            self._listener_task.cancel()
            self._listener_task = None
        if self._ws is not None:
            await self._ws.close()
            self._ws = None

    async def _listen(self) -> None:
        """Listen for incoming CALL messages and dispatch handlers."""
        assert self._ws is not None
        try:
            while True:
                raw = await self._ws.recv()
                msg = json.loads(raw)
                if not isinstance(msg, list) or len(msg) < 4:
                    continue
                if msg[0] != 2:
                    continue
                _, message_id, action, payload = msg
                handler = getattr(self, f"on_{action.lower()}", None)
                if handler:
                    resp_payload = await handler(payload)
                    response = [3, message_id, resp_payload]
                else:
                    response = [4, message_id, "NotImplemented", {}]
                await self._ws.send(json.dumps(response))
        except asyncio.CancelledError:
            pass
        except websockets.ConnectionClosed:
            pass

    async def _call(self, action: str, payload: dict) -> dict:
        """Send an OCPP CALL message and return the payload of the result."""
        if self._ws is None:
            raise RuntimeError("Client is not connected")

        message_id = str(uuid.uuid4())
        request = [2, message_id, action, payload]
        await self._ws.send(json.dumps(request))

        raw_response = await self._ws.recv()
        response = json.loads(raw_response)
        # OCPP result frames are of the form [3, message_id, payload]
        return response[2]

    async def boot_notification(self) -> None:
        """Send a BootNotification and schedule periodic heartbeats."""
        payload = {
            "chargePointModel": self.charger_model,
            "chargePointVendor": "Unknown"
        }
        resp = await self._call("BootNotification", payload)
        interval = int(resp.get("interval", 0)) or 60
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop(interval))

    async def _heartbeat_loop(self, interval: int) -> None:
        try:
            while True:
                await asyncio.sleep(interval)
                await self._call("Heartbeat", {})
        except asyncio.CancelledError:
            pass

    async def start_transaction(
        self, connector_id: int, id_tag: str, meter_start: int
    ) -> dict:
        payload = {
            "connectorId": connector_id,
            "idTag": id_tag,
            "meterStart": meter_start,
            "timestamp": datetime.utcnow().isoformat(),
        }
        resp = await self._call("StartTransaction", payload)
        tx_id = resp.get("transactionId")
        if tx_id is not None:
            self._active_tx = {
                "id": tx_id,
                "id_tag": id_tag,
                "connector_id": connector_id,
            }
            self._last_meter = meter_start
        return resp

    async def stop_transaction(
        self,
        transaction_id: int,
        id_tag: str,
        meter_stop: int,
        reason: str | None = None,
    ) -> dict:
        payload = {
            "transactionId": transaction_id,
            "idTag": id_tag,
            "meterStop": meter_stop,
            "timestamp": datetime.utcnow().isoformat(),
        }
        if reason:
            payload["reason"] = reason
        resp = await self._call("StopTransaction", payload)
        if self._active_tx and self._active_tx.get("id") == transaction_id:
            self._active_tx = None
        return resp

    async def send_meter_values(
        self,
        transaction_id: int,
        connector_id: int,
        sample: dict,
    ) -> dict:
        """Send a MeterValues message for the given sample."""

        entry = {
            "timestamp": sample.get("timestamp", datetime.utcnow().isoformat()),
            "sampledValue": [],
        }

        mapping = {
            "current": "Current.Import",
            "voltage": "Voltage",
            "soc": "SoC",
            "temperature": "Temperature",
            "energy": "Energy.Active.Import.Register",
        }

        for key, measurand in mapping.items():
            value = sample.get(key)
            if value is not None:
                entry["sampledValue"].append({"value": str(value), "measurand": measurand})
                if key == "energy":
                    try:
                        self._last_meter = int(value)
                    except Exception:
                        pass

        payload = {
            "transactionId": transaction_id,
            "connectorId": connector_id,
            "meterValue": [entry],
        }
        resp = await self._call("MeterValues", payload)
        return resp

    async def on_reset(self, payload: dict) -> dict:
        """Handle a Reset request and stop active transactions."""
        reset_type = payload.get("type")
        if reset_type not in ("Hard", "Soft"):
            return {"status": "Rejected"}
        reason = "HardReset" if reset_type == "Hard" else "SoftReset"
        if self._active_tx:
            await self.stop_transaction(
                self._active_tx["id"],
                self._active_tx.get("id_tag", ""),
                self._last_meter,
                reason=reason,
            )
        return {"status": "Accepted"}
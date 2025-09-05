# TODO

Tasks inferred from `rddPOC01140136.csv` and current codebase:

- [ ] Implement `BootNotification` and periodic `Heartbeat` in `OCPPClient` to allow the station to register and maintain connection.
- [ ] Support `Authorize` to send `idTag` before starting sessions.
- [ ] Send and persist `MeterValues` (Current, Voltage, Power, SoC, Temperature, etc.) during charging.
- [ ] Handle vendor-specific `DataTransfer` messages both incoming and outgoing.
- [ ] Extend session data structures to store additional sensor values beyond energy and duration.
- [ ] Handle remote operations such as `RemoteStartTransaction` and `RemoteStopTransaction`.
- [ ] Process `StatusNotification` messages to keep connector state updated.
- [ ] Implement configuration management via `ChangeConfiguration` and `GetConfiguration`, and support `TriggerMessage` requests.
<!-- - [ ] Support firmware management through `UpdateFirmware` requests. -->
- [x] Allow remote `Reset` commands (Hard/Soft) and handle resulting `StopTransaction` reasons.
# MnemonicForge

MnemonicForge is a playground for experimenting with high volume mnemonic and address processing. It demonstrates a producer/worker model that distributes work between CPU and GPU pools while monitoring throughput in real time.

## Features

- **Dedicated CPU and GPU queues** – separate task channels ensure that work is dispatched to the appropriate worker type.
- **Context-aware producer** – the task producer respects cancellation signals and closes queues cleanly for a graceful shutdown.
- **Per-second throughput counters** – optional counters report how many tasks each worker pool completes every second.
- **Runtime configuration** – settings such as batch size, enabled workers and mnemonic sizes are adjustable via command-line flags provided by the `config` package.

## Running

Fetch dependencies and build the project:

```bash
go build ./...
```

Run with default settings:

```bash
./MnemonicForge
```

Use `-h` to see available configuration flags.

### Command-line options

MnemonicForge can be customized at runtime with several flags:

- `-sizes` – comma separated mnemonic lengths to generate (default `12,15,18,21,24`).
- `-cpu` – enable CPU workers.
- `-gpu` – enable GPU workers when an NVIDIA device is available.
- `-count` – print how many tasks each worker pool completes per second.
- `-silent` – suppress enqueue logging.
- `-simulation` – run in simulation mode without real address checking.
- `-showAllResults`, `-showGenerated`, `-showCompared` – output additional details during processing.

Example:

```bash
./MnemonicForge -count -sizes=12 -cpu
```
# Trading Automation Worker

Distributed execution node for the Trading Automation platform. Each worker boots, registers with the main control plane, exposes a gRPC task surface, and drives brokerage automation through the AutoRSA CLI.

## System Architecture

- **Entry point** (`app/main.py`) – loads configuration, wires logging, and kicks off the worker bootstrap sequence.
- **Bootstrap Orchestrator** (`app/bootstrap.py`) – initializes the gRPC client/server, task facade, and AutoRSA services, then blocks on task consumption.
- **gRPC Task Server** (`app/data/strategy/grpc/DefaultServicer.py`) – receives activation/deactivation/transaction RPCs from Trading-Automation-Main and normalises payloads.
- **Task Dispatch Layer** (`app/taskFacade/TaskFacade.py`) – maps protobuf tasks to use cases, handles retries, and raises structured errors back over gRPC.
- **AutoRSA Integration** (`app/services/autoRsaService/AutoRSAService.py`) – wraps the AutoRSA CLI to perform brokerage logins, account activation, and trade execution.
- **Structured Logging** (`app/logger.py`) – streams JSON logs to stdout and rotates error output into `error.log` for local debugging.

```
┌─────────────────────────────┐       Ping (startup)        ┌──────────────────────────┐
│ Trading-Automation-Worker   │────────────────────────────▶│ Trading-Automation-Main  │
├─────────────────────────────┤                             ├──────────────────────────┤
│ GrpcTaskFetcher server      │◀── Activation / Task RPC ───│ Worker stub registry     │
│ DefaultServicer handlers    │                             │ Redis-backed routing     │
│ TaskFacade + UseCases       │─── Task responses ─────────▶│ REST / gRPC orchestrator │
│ AutoRSA runner              │                             │                          │
└─────────────────────────────┘                             └──────────────────────────┘
        ▲
        │ AutoRSA CLI (commands)
        ▼
   Brokerage / Exchange APIs
```

<details>
<summary>Worker Runtime Walkthrough (ASCII)</summary>

```
                         ┌────────────────────────┐
                         │ Trading Automation Main│
                         │────────────────────────│
                         │ • FastAPI REST router  │
                         │ • Redis group registry │
                         │ • Worker stub manager  │
                         └──────────┬─────────────┘
                                    │ secure gRPC
                                    ▼
        ┌────────────────────────────────────────────────────────────┐
        │               Trading Automation Worker                    │
        │────────────────────────────────────────────────────────────│
        │  Bootstrap (app/bootstrap.py)                              │
        │    • loads configs/app.json                                │
        │    • spins up GrpcTaskFetcher server                       │
        │    • issues startup ping to MainTradingService             │
        │                                                            │
        │ DefaultServicer(app/data/strategy/grpc/DefaultServicer.py) │
        │    • exposes Activate/Deactivate/Transaction RPCs          │
        │    • emits protobuf Payload → Task models                  │
        │                                                            │
        │  TaskFacade (app/taskFacade/TaskFacade.py)                 │
        │    • selects Activation/Deactivation/Transaction use case  │
        │    • coordinates AutoRSAService execution                  │
        │                                                            │
        │  AutoRSAService (app/services/autoRsaService/...)          │
        │    • shells out to lib/auto-rsa/ scripts                   │
        │    • parses CLI responses → gRPC replies                   │
        └────────────────────────────────────────────────────────────┘
```

</details>

## Capabilities

- Registers itself with the main control plane via periodic ping/keepalive and replays queued tasks on reconnect.
- Exposes a gRPC task API for account activation, deactivation, and transaction execution.
- Transforms strongly typed protobuf requests into AutoRSA commands with credential validation and error surfacing.
- Ships with Dockerfiles for standalone worker containers or Compose-based multi-service stacks.
- Provides configurable logging and retry hooks suitable for headless deployment.

## Prerequisites

- Python 3.9+
- Poetry (recommended for dependency management)
- AutoRSA CLI dependencies (`pip install -r lib/auto-rsa/requirements.txt`)
- Access to a running Trading-Automation-Main instance over gRPC
- Docker (optional) for containerized workloads

## Getting Started (Local)

1. **Clone**
   ```bash
   git clone <repository-url>
   cd Trading-Automation-Worker
   ```

2. **Install Poetry** (if needed)
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies**
   ```bash
   poetry install
   ```

4. **Provision AutoRSA**
   ```bash
   pip install -r lib/auto-rsa/requirements.txt
   ```
   Populate `lib/auto-rsa/creds` and `.env` according to brokerage requirements.

5. **Generate protobuf stubs**
   ```bash
   poetry run bash scripts/proto_build.sh
   ```

6. **Configure worker endpoints** – update `configs/app.json` with the main server host/port and the worker's listening address.

7. **Launch the worker**
   ```bash
   poetry run python app/main.py
   ```
   The worker pings the main service, binds its gRPC server (default `0.0.0.0:50051`), and begins consuming tasks.

## Docker & Compose

- **Build image**
  ```bash
  docker build -t trading-worker .
  ```

- **Run container**
  ```bash
  docker run -d --name trading-worker \
    -p 50051:50051 \
    -v $(pwd)/configs:/app/configs \
    -v $(pwd)/lib/auto-rsa:/app/lib/auto-rsa \
    trading-worker
  ```
  Ensure the container can reach the main service gRPC endpoint and that AutoRSA credentials are mounted securely.

- **Compose stack** – when using the main project’s `docker-compose.yml`, tag the image as `worker:latest` so the orchestrator can schedule it.

## Configuration

- `configs/app.json` – declares `MAIN_SERVER_HOST`, `MAIN_SERVER_PORT`, and the worker’s `TASK_FETCHER_*` bind settings.
- `lib/auto-rsa/.env` – broker-specific secrets such as usernames, passwords, and MFA seeds.
- `lib/auto-rsa/creds/` – encrypted credential bundles consumed by AutoRSA.
- Environment variables can override defaults by extending the bootstrap logic in `app/bootstrap.py`.

## gRPC Task Lifecycle

1. Worker boots, loads config, and sends a `Ping` to `MainTradingService` with its callback host/port.
2. Trading-Automation-Main dials the worker and establishes a bidirectional gRPC channel.
3. Incoming protobuf tasks hit `DefaultServicer`, which converts them into internal task models.
4. `TaskFacade` routes each task to the matching use case and invokes `AutoRSAService` to perform the action.
5. Results (success/error payloads) are serialized back over gRPC to the main service for client responses.

## Development Tasks

- **Protobuf generation**: `poetry run bash scripts/proto_build.sh`
- **Unit tests**: `poetry run pytest` (ensure dependencies and any mocks for AutoRSA are available)
- **Linting/formatting**: integrate `ruff`, `flake8`, or `black` via Poetry as desired.

## Project Layout

```
app/
├── main.py                      # Worker entry point and runtime loop
├── bootstrap.py                 # Config loading, ping client, and gRPC bootstrap
├── logger.py                    # Structured logging configuration
├── data/
│   ├── strategy/grpc/           # GrpcTaskFetcher, DefaultServicer, generated stubs
│   └── model/task/              # Internal task DTOs and converters
├── taskFacade/TaskFacade.py     # Central task dispatcher
├── useCase/                     # Activation/Deactivation/Transaction flows
├── services/autoRsaService/     # AutoRSA command execution wrapper
├── router/Router.py             # Factory wiring for task handlers
configs/app.json                 # Worker runtime configuration
scripts/proto_build.sh           # Regenerate protobuf definitions
lib/auto-rsa/                    # Embedded AutoRSA CLI toolkit
Dockerfile                       # Container image definition
```

## Observability & Ops

- `app/logger.py` emits JSON logs to stdout and mirrors exceptions into `error.log`—ship the stream to your log aggregator in production.
- gRPC keepalive is managed in the bootstrap; tune intervals/timeouts before deployment to noisy networks.
- AutoRSA commands may surface sensitive output—mask logs and secure the `lib/auto-rsa` directory.

## Troubleshooting

- **Ping failures**: verify `MAIN_SERVER_HOST`/`PORT` and that the worker can reach the orchestrator over the network.
- **AutoRSA errors**: ensure Python dependencies are installed and credentials in `lib/auto-rsa` are valid.
- **gRPC port conflicts**: adjust `TASK_FETCHER_PORT` in `configs/app.json` or the Docker port mapping.
- **Permission issues**: AutoRSA scripts require execution permission (`chmod +x`) when mounted into containers.

## Related Projects

- [Trading-Automation-Main](https://github.com/roieGolst/Trading-Automation-Main) – FastAPI control plane and worker orchestrator.

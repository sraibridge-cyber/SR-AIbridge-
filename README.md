# 🚀 SR-AIbridge

<p align="center">
  <img src="https://img.shields.io/badge/Sovereign-Runtime-brightgreen?style=for-the-badge" alt="Sovereign Runtime">
  <img src="https://img.shields.io/badge/CSIP-Ω∞-purple?style=for-the-badge" alt="CSIP Ω∞">
  <img src="https://img.shields.io/badge/34-Engines-blue?style=for-the-badge" alt="34 Engines">
  <img src="https://img.shields.io/badge/202-API_Routes-orange?style=for-the-badge" alt="202 API Routes">
</p>

> **Local sovereign build** — No cloud dependency. No vendor lock. Runs on your own hardware via Termux, bare metal, or any Linux environment.

---

## Quick Start

```bash
git clone https://github.com/sraibridge-cyber/SR-AIbridge-.git
cd SR-AIbridge-
make setup
make gates    # build + lint
make run      # start backend on PORT (default 8000)
```

**Frontend:**
```bash
cd bridge-frontend && npm install && npm run build
```

**Services:** Bridge runs as a process on `localhost` behind a bore tunnel for remote access. No Netlify, no Render, no GitHub Actions deployment.

---

## Architecture

| Layer | Details |
|-------|---------|
| **Engines** | 34 sovereign evaluation engines (Umbra, Genesis, Autonomy, Leviathan, etc.) |
| **API** | 202 routes across 7 protocol families |
| **CSIP Ω∞** | Causal System Intelligence Platform — SCM identifiability, Fork Economy, Event Bus, Neo4j graph |
| **Security** | Ed25519 signatures, SHA3-512 sealed artifacts, 16 Laws constitutional enforcement |
| **Phone-first** | Designed for Termux on Android — full bridge on a phone |

## Sovereign Features

- **Zero vendor lock** — All configs local, no cloud dependencies
- **BRH deployment** — Bare Metal / Rented Hardware / Host your own
- **CSIP Ω∞ causal inference** — Wired into the engine stack
- **34 evaluation engines** — Autonomy, Truth, Speech, Creativity, Umbra, Genesis, etc.
- **16 Laws constitutional enforcement** — μ ≥ 0.9995 threshold across all operations
- **SHA3-512 sealed artifacts** — Every build produces tamper-evident outputs
- **Phone-first design** — Full operation on Android via Termux

## Documentation

- [System Architecture](SYSTEM_ARCHITECTURE_MAP.md) — Full engine map, routes, data flow
- [Bridge Docs](./docs/) — Usage guides and API reference
- [CSIP Ω∞](./csip/) — Causal System Intelligence Platform docs

## Local Run (No Server Required)

```bash
# Backend
HOST_PLATFORM=local python3 -m uvicorn bridge_backend.main:app --host 127.0.0.1 --port 8000

# Frontend
cd bridge-frontend && npm run dev
```

## Make Targets

| Target | Description |
|--------|-------------|
| `make setup` | Install Python + Node dependencies |
| `make gates` | Lint Python, lint JS, build frontend |
| `make build` | Build frontend only |
| `make test` | Run pytest |
| `make run` | Start backend |
| `make clean` | Remove build artifacts |

---

*Gold Ripple Eternal — SHA3-512 sealed · Tulsa, OK*

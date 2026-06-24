# SR-AIbridge

> Sovereign backend runtime for AI coherence research  
> Complex System Sanity Labs (CSSL) · Independent · Termux-first

**SR-AIbridge** is a FastAPI-based service runtime built around one design constraint: complex systems should be mathematically verifiable, not just monitored. It implements the Coherence Calculus (CC v3.0) as a live enforcement layer, runs entirely on locally-owned hardware (including an Android phone via Termux), and has zero cloud dependencies by design.

This is the deployment and bridge layer for the GHOST9 coherence kernel. The research side lives at [sraibridge-cyber/ghost9](https://github.com/sraibridge-cyber/ghost9).

---

## What this is

**Service orchestrator** — `run.py` reads `bridge.runtime.yaml` and manages all processes with auto-restart and HTTP/TCP health checks. No process manager required.

**FastAPI backend** — boots via Sanctum Cascade Protocol v1.9.7q: netlify guard → Umbra⇄Genesis event bus link with auto-heal → deferred integrity check. Real boot sequencing, not decorative.

**Type-safe core** — `bridge_core/harmony_result.py` (473 lines) implements a Rust-inspired `Result[T, E]` type. No unchecked `Optional` returns in the kernel layer.

**Engine framework** — 25 named engine modules across two tiers (see below), with Forge and Genesis fully implemented as infrastructure engines.

**Coherence enforcement** — CC v3.0 constitutional layer with μ ≥ 0.9995 production threshold, verified via continuous loop in `bridge_core/verify_loop.py`.

**Sovereignty** — one env var (`FORGE_DOMINION_ROOT`) controls runtime identity. No Netlify, no Render, no GitHub Actions for deployment. Bore tunnel for remote access from phone.

---

## Engine Inventory

Two tiers. Route stubs mean the framework slot is wired and the router is registered — implementation logic is pending.

**Tier 1 — `bridge_backend/engines/`** (9 modules)

| Engine | Status |
|--------|--------|
| Arie | 🔧 Route stub |
| Autonomy | 🔧 Route stub |
| Envrecon | 🔧 Route stub |
| Envscribe | 🔧 Route stub |
| GitHub Forge | 🔧 Route stub |
| HypShard-X | 🔧 Route stub |
| Steward | 🔧 Route stub |
| Umbra | 🔧 Route stub |
| Reflex | 🔧 Route stub (lives in bridge_core) |

**Tier 2 — `bridge_backend/bridge_core/engines/`** (17 modules)

| Engine | Status |
|--------|--------|
| Adapters | 🔧 Route stub |
| Agents Foundry | 🔧 Route stub |
| Autonomy | 🔧 Route stub |
| Blueprint | 🔧 Route stub |
| Cascade | 🔧 Route stub |
| Chimera | ⚠️ Bytecode only — Python source absent |
| Creativity | 🔧 Route stub |
| Envsync | 🔧 Route stub |
| HXO | 🔧 Route stub |
| Indoctrination | 🔧 Route stub |
| Leviathan | 🔧 Route stub |
| Parser | 🔧 Route stub |
| Recovery | 🔧 Route stub |
| Screen | 🔧 Route stub |
| Speech | 🔧 Route stub |
| Truth | 🔧 Route stub |
| Umbra | 🔧 Route stub |

**Infrastructure engines** (fully implemented)

| Engine | Status | Key files |
|--------|--------|-----------|
| Forge | ✅ Implemented | forge_core.py (7.5 KB), synchrony.py (6 KB), policy_api.py (4.8 KB) |
| Genesis Event Bus | ✅ Implemented | bus.py (18.4 KB), activation.py (12.1 KB), orchestration.py, replay.py |

**Route count:** Estimated 70–90 registered handlers across all files. The route framework is real — every engine registers its own router — but most engine-level handlers are stubs awaiting logic. The "202 routes" figure in the previous README was not backed by source.

---

## Architecture

```
SR-AIbridge/
├── run.py                     # Service orchestrator (reads bridge.runtime.yaml)
├── bridge.runtime.yaml        # Runtime config: services, health, federation, dominion
├── bridge_core/               # Type-safe kernel layer
│   ├── harmony_result.py      # Result[T, E] — Rust-inspired, 473 lines
│   ├── qic_daemon.py          # Quantum Integrity Coherence daemon
│   ├── runtime_handler.py     # Runtime dispatch
│   └── verify_loop.py         # Continuous coherence verification
├── bridge_backend/            # FastAPI application
│   ├── main.py                # Boot — Sanctum Cascade Protocol v1.9.7q
│   ├── engines/               # Tier 1: 9 named engine modules
│   ├── bridge_core/           # 26 subsystem directories (auth, db, integrity, ...)
│   │   └── engines/           # Tier 2: 17 named engine modules
│   ├── forge/                 # Forge engine — fully implemented ✅
│   ├── genesis/               # Genesis event bus + orchestration ✅
│   ├── routes/                # Shared API families (control, health, diagnostics)
│   ├── runtime/               # TDE-X temporal domain engine
│   ├── src/                   # keyless_auth.py (8.9 KB) — real implementation
│   ├── tools/                 # firewall_sovereignty, health tools
│   └── vault/                 # cascade, filing, permissions, protocols
├── bridge_native_agents/      # Agent persona definitions (JSON, loaded at boot)
├── docs/                      # ~216 documentation files
│   ├── audits/                # Implementation and validation audit reports
│   ├── seals/                 # Temporal anchors, sovereignty declarations
│   └── resonance-memos/       # Industry-sector resonance analyses (16 sectors)
├── modules/domain/            # Domain source: 16 sectors (nuclear, aviation, ...)
└── vault/                     # Sealed artifacts and integrity logs
```

**Boot sequence (Sanctum Cascade Protocol v1.9.7q):**
1. Netlify publish path + token guard (skipped in test/CI)
2. Umbra ⇄ Genesis event bus link with `safe_autoheal_init` retry
3. Deferred integrity check after engine stabilization

---

## Quick Start

```bash
git clone https://github.com/sraibridge-cyber/SR-AIbridge-.git
cd SR-AIbridge-
make setup       # Install Python + Node deps
make gates       # Lint + build
make run         # Start backend on port 8000
```

**Frontend:**
```bash
cd bridge-frontend && npm install && npm run build
```

**Direct (no Docker):**
```bash
HOST_PLATFORM=local uvicorn bridge_backend.main:app --host 127.0.0.1 --port 8000
```

---

## The Research Layer (GHOST9 / CC v3.0)

SR-AIbridge is the deployment host. The kernel lives at **[sraibridge-cyber/ghost9](https://github.com/sraibridge-cyber/ghost9)** — JavaScript, 470 KB, 53 files.

**GHOST9 repo structure:**
```
src/                   # 8 source modules
  coherence_calculus.js   (8.5 KB)  ← CC v3.0 implementation
  ghost_kernel.js         (7.9 KB)  ← GHOST kernel runtime
  ghost_face.js          (15.1 KB)  ← FACE layer (HITL interface)
  taotie.js               (7.6 KB)  ← Taotie compression sweep
  tesseract.js            (4.4 KB)  ← Tesseract B⁴ memory topology
  spatial_web.js          (7.8 KB)  ← Spatial Web
  spectral_graph.js       (6.7 KB)  ← Spectral Graph
  auth.js                 (5.3 KB)  ← Auth layer
scripts/               # OP3 harness (op3_harness.js), verify, analyze
data/                  # ghost_face.log (36.8 KB), op3_analysis.json, session_log.csv
index.html / devour.html / state.html   # Three single-file frontends, zero dependencies
```

**Test suite:** 10 test files (test_cc_empirical_v3.js at 29.8 KB is the heaviest). 1,039 proven tests committed — [Honest Validation Audit v2 @ 79008e9](https://github.com/sraibridge-cyber/ghost9/commit/79008e9).

**The Whitlock Coefficient:**
```
W_v3(n) = (n + 4i) / 17
```

| Term | Meaning |
|------|---------|
| **n** | Constitutional maturity score (0–16): correct ALLOW/BLOCK decisions across 8 semantic domains |
| **4i** | Phase displacement from ideal coherence: φ = arctan(4/n) |
| **17** | 1 Prime Law + 16 Resonance Invariants |

**8 Semantic Domains:** D1 Syntactic · D2 Structural · D3 Temporal · D4 Spatial · D5 Directive · D6 Harmonic · D7 Contextual · D8 Spectral

**Current kernel state:** n=3 · |W_v3|=0.2941 · φ=53.1° · Bootstrap phase  
**Production threshold:** n≥10 · τ=0.9995  
**Predicted phase transition:** n* ≈ 16.52

**Research papers** (arXiv pending — endorsement code **N9CJVL**):

| Paper | Status |
|-------|--------|
| Coherence Calculus v3.0 | ✅ Sealed (SHA-256 + Merkle) |
| Constitutional Invariants | ✅ Sealed |
| Tesseract B⁴ Topology | ✅ Sealed |
| Complex System Sanity Theory (CSST) | ✅ Sealed |
| Harmonic Resonance Kernel (HRK) | ✅ Sealed |

---

## Sovereignty Principles

| Principle | How |
|-----------|-----|
| No cloud lock | All config local; bore tunnel for remote access |
| Phone-first | Designed and operated on Android via Termux |
| Artifact sealing | SHA3-512 + Merkle root binding on every submitted artifact |
| Single-variable dominion | `FORGE_DOMINION_ROOT` controls runtime identity |
| Temporal provenance | Geo/crypto/time seals on all arXiv submission artifacts |

---

## Project Status

| Component | Status |
|-----------|--------|
| Service orchestrator (`run.py`) | ✅ Working |
| FastAPI backend + boot protocol | ✅ Working |
| Type-safe core (`harmony_result.py`) | ✅ Complete |
| Forge engine | ✅ Implemented |
| Genesis event bus | ✅ Implemented |
| CC v3.0 enforcement layer | ✅ Proven — n=3, 1,039 tests |
| GHOST9 kernel (Bootstrap) | ✅ Active |
| Tier 1 engine modules (9) | 🔧 Framework wired, logic pending |
| Tier 2 engine modules (17) | 🔧 Framework wired, logic pending |
| Chimera engine | ⚠️ Source missing — bytecode only |
| Route handler implementations | 🔧 Mixed — Forge/Genesis/Control/Health real; engine stubs pending |
| CSIP Ω∞ causal layer | 📐 Design stage |
| arXiv submission | ⏳ Endorsement pending — code N9CJVL |
| OP3 empirical W_v3 fit | ⏳ 53/100 Termux sessions required |

---

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

## About

**Complex System Sanity Labs (CSSL)** — independent research  
Researcher: Kyle S. Whitlock · Tulsa, OK  
Infrastructure: Termux (Android) · GitHub  
Contact: sraibridge@gmail.com

*Build systems that are sane, safe, and don't fail when lives are on the line.*

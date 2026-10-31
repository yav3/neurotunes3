# Evidence Protocol — NeuroTunesAI Cross-Repo Schema Definitions

Canonical schemas for the governed evidence layer shared across:
- **NeuroTunesAI** — governed solver and training harness
- **merlinaineuralplus2** — evidence engine, patent estate, data harvest
- **neurotunes** (Flutter) — mobile therapeutic delivery
- **neurotunescopy4privatesharing** — web product surface

## What This Defines

| Module | Purpose |
|---|---|
| `evidence_protocol.schemas` | Dataclass definitions for evidence records, study declarations, predictions |
| `evidence_protocol.firewall` | Species and regime validation rules |
| `evidence_protocol.hashing` | Canonical SHA-256 hashing for lineage chains and content addressing |

## Design Principle

**Declare or refuse, never default.** Every prediction carries its species, regime, and spec_hash.
The firewall rejects undeclared species rather than silently assuming human.
Regime is classified from data shape, not asserted.

## Usage

```python
from evidence_protocol.schemas import PredictionEnvelope, StudyDeclaration
from evidence_protocol.firewall import classify_regime, validate_species

validate_species("human")  # passes
regime = classify_regime(n_samples=44, n_control=23, n_treated=21)  # "data_driven"
```

"""Canonical dataclass definitions for the cross-repo evidence protocol."""
from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any

from evidence_protocol.hashing import chain_hash, content_hash


@dataclass
class EvidenceRecord:
    """A single record in a hash-chained lineage."""

    record_id: str
    prev_hash: str
    problem_spec: dict[str, Any]
    answer_values: dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    hash: str = ""

    def __post_init__(self) -> None:
        if not self.hash:
            self.hash = chain_hash(
                self.prev_hash,
                self.record_id,
                self.problem_spec,
                self.answer_values,
                self.timestamp,
            )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> EvidenceRecord:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})

    def content_hash(self) -> str:
        return content_hash(
            json.dumps(self.to_dict(), sort_keys=True).encode()
        )


@dataclass
class StudyDeclaration:
    """Pre-registration record — criterion declared before the run."""

    study_id: str
    title: str
    criterion: str
    data_kind: str
    species: str
    regime: str
    declared_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> StudyDeclaration:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})

    def content_hash(self) -> str:
        return content_hash(
            json.dumps(self.to_dict(), sort_keys=True).encode()
        )


@dataclass
class Verdict:
    """Immutable study verdict."""

    study_id: str
    verdict: str  # "met" | "not_met" | "pending"
    evidence_hash: str = ""
    recorded_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Verdict:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})

    def content_hash(self) -> str:
        return content_hash(
            json.dumps(self.to_dict(), sort_keys=True).encode()
        )


@dataclass
class PerturbationSpec:
    """Perturbation parameters for a single prediction."""

    ptype: str  # "knockout" | "drug" | "time_course"
    gene_idx: int = 0
    drug_idx: int = 0
    dose: float = 0.0
    duration: float = 0.0
    time_point: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> PerturbationSpec:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class PredictionEnvelope:
    """Wraps a prediction with full provenance."""

    prediction_id: str
    spec_hash: str
    regime: str
    species: str
    perturbation: PerturbationSpec
    n_genes: int
    latent_variance: float = 0.0
    data_hash: str = ""

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> PredictionEnvelope:
        pert_data = d.get("perturbation", {})
        if isinstance(pert_data, dict):
            pert = PerturbationSpec.from_dict(pert_data)
        else:
            pert = pert_data
        return cls(
            prediction_id=d["prediction_id"],
            spec_hash=d["spec_hash"],
            regime=d["regime"],
            species=d["species"],
            perturbation=pert,
            n_genes=d["n_genes"],
            latent_variance=d.get("latent_variance", 0.0),
            data_hash=d.get("data_hash", ""),
        )

    def content_hash(self) -> str:
        return content_hash(
            json.dumps(self.to_dict(), sort_keys=True).encode()
        )


@dataclass
class DatasetManifest:
    """Describes a committed expression dataset."""

    accession: str
    n_samples: int
    n_genes: int
    n_control: int
    n_treated: int
    species: str
    regime: str
    content_hash_hex: str
    path: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> DatasetManifest:
        field_map = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        if "content_hash" in d and "content_hash_hex" not in d:
            field_map["content_hash_hex"] = d["content_hash"]
        return cls(**field_map)

    def content_hash(self) -> str:
        return content_hash(
            json.dumps(self.to_dict(), sort_keys=True).encode()
        )

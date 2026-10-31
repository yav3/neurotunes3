"""Canonical hashing utilities for evidence chains and content addressing."""
from __future__ import annotations

import hashlib
import json


def content_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def chain_hash(
    prev_hash: str,
    record_id: str,
    problem_spec: dict,
    answer_values: dict,
    timestamp: float,
) -> str:
    payload = json.dumps(
        {
            "prev_hash": prev_hash,
            "record_id": record_id,
            "problem_spec": problem_spec,
            "answer_values": answer_values,
            "timestamp": timestamp,
        },
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def prediction_hash(
    baseline_hash: str,
    predicted_hash: str,
    ptype: str,
    spec_hash: str,
) -> str:
    payload = json.dumps(
        {
            "baseline_hash": baseline_hash[:16],
            "predicted_hash": predicted_hash[:16],
            "ptype": ptype,
            "spec_hash": spec_hash,
        },
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()

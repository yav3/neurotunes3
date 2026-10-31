"""Species and regime firewall rules.

Declare or refuse, never default.
"""
from __future__ import annotations

ALLOWED_SPECIES: frozenset[str] = frozenset({"human"})

REGIME_THRESHOLDS = {
    "data_driven": 30,
    "prior_contrast": 2,
    "prior_mean": 1,
}


def validate_species(species: str) -> None:
    if species not in ALLOWED_SPECIES:
        raise ValueError(
            f'Species firewall: "{species}" refused. Allowed: {sorted(ALLOWED_SPECIES)}'
        )


def classify_regime(
    n_samples: int,
    n_control: int = 0,
    n_treated: int = 0,
) -> str:
    if n_samples >= REGIME_THRESHOLDS["data_driven"] and n_control > 0 and n_treated > 0:
        return "data_driven"
    if n_control > 0 and n_treated > 0:
        return "prior_contrast"
    return "prior_mean"


def validate_regime_sufficiency(
    regime: str,
    n_samples: int,
    n_control: int = 0,
    n_treated: int = 0,
) -> bool:
    actual = classify_regime(n_samples, n_control, n_treated)
    if regime == "data_driven":
        return actual == "data_driven"
    if regime == "prior_contrast":
        return actual in ("data_driven", "prior_contrast")
    return True

<<<<<<< HEAD
"""Spatial hearing: ITD, ILD, HRTF synthesis, binaural cue analysis."""
from __future__ import annotations

from dataclasses import dataclass
=======
"""Spatial hearing: binaural cues, HRTF, interaural differences.

Models the psychoacoustic mechanisms of spatial hearing including
interaural time difference (ITD), interaural level difference (ILD),
head-related transfer functions (HRTF), and distance perception.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
>>>>>>> 9a0c6893 (Add missing modules: concept embeddings, mood ontology, spatial hearing, timbre perception, and 7 more)

import numpy as np

SPEED_OF_SOUND = 343.0
HEAD_RADIUS = 0.0875


@dataclass
class SpatialSource:
<<<<<<< HEAD
    azimuth_deg: float
    elevation_deg: float = 0.0
    distance_m: float = 1.5
=======
    azimuth: float  # degrees, 0=front, 90=right
    elevation: float = 0.0  # degrees
    distance: float = 1.0  # meters
>>>>>>> 9a0c6893 (Add missing modules: concept embeddings, mood ontology, spatial hearing, timbre perception, and 7 more)


@dataclass
class BinauralCues:
<<<<<<< HEAD
    itd_us: float
    ild_db: float
    ic: float
=======
    itd: float  # seconds
    ild: float  # dB
    ic: float = 1.0  # interaural coherence [0,1]
>>>>>>> 9a0c6893 (Add missing modules: concept embeddings, mood ontology, spatial hearing, timbre perception, and 7 more)


@dataclass
class HRTFPair:
    left: np.ndarray
    right: np.ndarray
<<<<<<< HEAD
    sample_rate: int


def interaural_time_difference(azimuth_deg: float, head_radius: float = HEAD_RADIUS) -> float:
    theta = np.radians(azimuth_deg)
    if abs(theta) < 1e-8:
        return 0.0
    itd_s = (head_radius / SPEED_OF_SOUND) * (np.sin(theta) + theta)
    return float(itd_s * 1e6)


def interaural_level_difference(azimuth_deg: float, freq_hz: float,
                                 head_radius: float = HEAD_RADIUS) -> float:
    theta = np.radians(azimuth_deg)
    ka = 2.0 * np.pi * freq_hz * head_radius / SPEED_OF_SOUND
    shadow = 1.0 + ka * abs(np.sin(theta))
    if shadow < 1e-12:
        return 0.0
    return float(20.0 * np.log10(shadow))


def head_shadow_filter(freq_hz: float, azimuth_deg: float,
                       head_radius: float = HEAD_RADIUS) -> tuple[float, float]:
    theta = np.radians(azimuth_deg)
    ka = 2.0 * np.pi * freq_hz * head_radius / SPEED_OF_SOUND
    shadow_factor = ka * abs(np.sin(theta))
    if theta >= 0:
        left_gain = 1.0 / (1.0 + shadow_factor)
        right_gain = 1.0
    else:
        left_gain = 1.0
        right_gain = 1.0 / (1.0 + shadow_factor)
    return (float(left_gain), float(right_gain))


def distance_attenuation(distance_m: float, ref_distance: float = 1.0) -> float:
    if distance_m <= 0 or ref_distance <= 0:
        return 0.0
    return float(-20.0 * np.log10(distance_m / ref_distance))


def air_absorption(distance_m: float, freq_hz: float,
                   temperature_c: float = 20.0, humidity_pct: float = 50.0) -> float:
    f_khz = freq_hz / 1000.0
    alpha = 0.01 * (f_khz ** 1.7) * (1.0 + 0.01 * (100 - humidity_pct))
    alpha *= (293.15 / (temperature_c + 273.15))
    return float(alpha * distance_m)


def generate_synthetic_hrtf(azimuth_deg: float, elevation_deg: float = 0.0,
                            n_taps: int = 128, sr: int = 44100) -> HRTFPair:
    itd_us = interaural_time_difference(azimuth_deg)
    itd_samples = itd_us * 1e-6 * sr
    left_ir = np.zeros(n_taps)
    right_ir = np.zeros(n_taps)
    left_delay = max(0, int(round(-itd_samples / 2)))
    right_delay = max(0, int(round(itd_samples / 2)))
    freq_test = 1000.0
    lg, rg = head_shadow_filter(freq_test, azimuth_deg)
    if left_delay < n_taps:
        left_ir[left_delay] = lg
    if right_delay < n_taps:
        right_ir[right_delay] = rg
    return HRTFPair(left=left_ir, right=right_ir, sample_rate=sr)


def apply_hrtf(mono_signal: np.ndarray, hrtf: HRTFPair) -> tuple[np.ndarray, np.ndarray]:
    left = np.convolve(mono_signal, hrtf.left, mode="full")[: len(mono_signal)]
    right = np.convolve(mono_signal, hrtf.right, mode="full")[: len(mono_signal)]
    return left, right


def interaural_coherence(left: np.ndarray, right: np.ndarray) -> float:
    nl = np.linalg.norm(left)
    nr = np.linalg.norm(right)
    if nl < 1e-12 or nr < 1e-12:
        return 0.0
    return float(np.dot(left, right) / (nl * nr))


def estimate_azimuth(itd_us: float, head_radius: float = HEAD_RADIUS) -> float:
    itd_s = itd_us * 1e-6
    max_itd = (head_radius / SPEED_OF_SOUND) * (1.0 + np.pi / 2.0)
    if abs(itd_s) > max_itd:
        return 90.0 * np.sign(itd_s)
    theta = np.arcsin(np.clip(itd_s * SPEED_OF_SOUND / (2.0 * head_radius), -1, 1))
    for _ in range(20):
        f = (head_radius / SPEED_OF_SOUND) * (np.sin(theta) + theta) - itd_s
        fp = (head_radius / SPEED_OF_SOUND) * (np.cos(theta) + 1.0)
        if abs(fp) < 1e-15:
            break
        theta -= f / fp
        theta = np.clip(theta, -np.pi / 2, np.pi / 2)
    return float(np.degrees(theta))
=======
    sample_rate: int = 44100
    azimuth: float = 0.0
    elevation: float = 0.0


def interaural_time_difference(azimuth_deg: float,
                                head_radius: float = HEAD_RADIUS,
                                c: float = SPEED_OF_SOUND) -> float:
    theta = np.radians(azimuth_deg)
    return float(head_radius / c * (np.sin(theta) + theta))


def interaural_level_difference(azimuth_deg: float, freq_hz: float,
                                 head_radius: float = HEAD_RADIUS,
                                 c: float = SPEED_OF_SOUND) -> float:
    theta = np.radians(azimuth_deg)
    ka = 2 * np.pi * freq_hz * head_radius / c
    if ka < 0.01:
        return 0.0
    shadow = 1.0 + ka * abs(np.sin(theta))
    ild_linear = shadow
    return float(20 * np.log10(max(ild_linear, 1e-12)))


def head_shadow_filter(freq_hz: float, azimuth_deg: float,
                       head_radius: float = HEAD_RADIUS,
                       c: float = SPEED_OF_SOUND) -> tuple[float, float]:
    theta = np.radians(azimuth_deg)
    ka = 2 * np.pi * freq_hz * head_radius / c
    shadow_factor = min(ka * abs(np.sin(theta)), 10.0)
    if np.sin(theta) >= 0:
        gain_right = 1.0 / (1.0 + shadow_factor)
        gain_left = 1.0
    else:
        gain_left = 1.0 / (1.0 + shadow_factor)
        gain_right = 1.0
    return (float(gain_left), float(gain_right))


def distance_attenuation(distance: float, ref_distance: float = 1.0) -> float:
    if distance <= 0:
        return 0.0
    return float(ref_distance / max(distance, 1e-12))


def air_absorption(distance: float, freq_hz: float,
                   temperature: float = 20.0, humidity: float = 50.0) -> float:
    alpha = 1.84e-11 * (temperature / 293.15) ** 0.5 * freq_hz ** 2
    alpha += 0.01275 * np.exp(-2239.1 / (temperature + 273.15)) * freq_hz ** 2 / (
        freq_hz ** 2 + 0.01275 * np.exp(-2239.1 / (temperature + 273.15))
    )
    return float(np.exp(-alpha * distance))


def generate_synthetic_hrtf(azimuth_deg: float, elevation_deg: float = 0.0,
                            n_samples: int = 128, sr: int = 44100) -> HRTFPair:
    t = np.arange(n_samples) / sr
    itd = interaural_time_difference(azimuth_deg)
    itd_samples = int(abs(itd) * sr)

    left = np.zeros(n_samples)
    right = np.zeros(n_samples)

    center = n_samples // 4
    width = max(n_samples // 8, 2)
    impulse = np.exp(-0.5 * ((np.arange(n_samples) - center) / width) ** 2)

    ild = interaural_level_difference(azimuth_deg, 1000.0)
    ild_linear = 10 ** (ild / 20)

    if itd >= 0:
        left[:] = impulse
        shift = min(itd_samples, n_samples - 1)
        right[:] = np.roll(impulse, shift) / max(ild_linear, 1e-12)
    else:
        right[:] = impulse
        shift = min(abs(itd_samples), n_samples - 1)
        left[:] = np.roll(impulse, shift) * max(ild_linear, 1e-12)

    left /= np.max(np.abs(left)) + 1e-12
    right /= np.max(np.abs(right)) + 1e-12

    return HRTFPair(left, right, sr, azimuth_deg, elevation_deg)


def apply_hrtf(signal: np.ndarray, hrtf: HRTFPair) -> tuple[np.ndarray, np.ndarray]:
    n = len(signal)
    nh = len(hrtf.left)
    out_len = n + nh - 1
    left_out = np.convolve(signal, hrtf.left)[:out_len]
    right_out = np.convolve(signal, hrtf.right)[:out_len]
    return (left_out, right_out)


def interaural_coherence(left: np.ndarray, right: np.ndarray) -> float:
    if len(left) == 0 or len(right) == 0:
        return 0.0
    n = min(len(left), len(right))
    l, r = left[:n], right[:n]
    l_norm = np.linalg.norm(l)
    r_norm = np.linalg.norm(r)
    if l_norm < 1e-12 or r_norm < 1e-12:
        return 0.0
    return float(np.abs(np.dot(l, r)) / (l_norm * r_norm))


def estimate_azimuth(itd: float, head_radius: float = HEAD_RADIUS,
                     c: float = SPEED_OF_SOUND) -> float:
    max_itd = head_radius / c * (1 + np.pi / 2)
    itd_clipped = np.clip(itd, -max_itd, max_itd)
    azimuth_rad = np.arcsin(np.clip(itd_clipped * c / head_radius, -1, 1))
    return float(np.degrees(azimuth_rad))
>>>>>>> 9a0c6893 (Add missing modules: concept embeddings, mood ontology, spatial hearing, timbre perception, and 7 more)


def binaural_cue_analysis(left: np.ndarray, right: np.ndarray,
                          sr: int = 44100) -> BinauralCues:
<<<<<<< HEAD
    max_lag = int(0.001 * sr)
    best_lag = 0
    best_val = -np.inf
    nl = np.linalg.norm(left)
    nr = np.linalg.norm(right)
    if nl < 1e-12 or nr < 1e-12:
        return BinauralCues(itd_us=0.0, ild_db=0.0, ic=0.0)
    for lag in range(-max_lag, max_lag + 1):
        if lag >= 0:
            l_seg = left[lag:]
            r_seg = right[: len(l_seg)]
        else:
            r_seg = right[-lag:]
            l_seg = left[: len(r_seg)]
        if len(l_seg) == 0:
            continue
        val = np.dot(l_seg, r_seg) / (np.linalg.norm(l_seg) * np.linalg.norm(r_seg) + 1e-12)
        if val > best_val:
            best_val = val
            best_lag = lag
    itd_us = float(best_lag / sr * 1e6)
    rms_l = np.sqrt(np.mean(left ** 2))
    rms_r = np.sqrt(np.mean(right ** 2))
    ild_db = float(20.0 * np.log10((rms_l + 1e-12) / (rms_r + 1e-12)))
    ic = float(best_val)
    return BinauralCues(itd_us=itd_us, ild_db=ild_db, ic=ic)
=======
    n = min(len(left), len(right))
    l, r = left[:n], right[:n]
    cross_corr = np.correlate(l, r, mode="full")
    peak = np.argmax(np.abs(cross_corr))
    lag = peak - (n - 1)
    itd = lag / sr

    l_power = np.mean(l ** 2)
    r_power = np.mean(r ** 2)
    if l_power < 1e-12 or r_power < 1e-12:
        ild = 0.0
    else:
        ild = 10 * np.log10(l_power / r_power)

    ic = interaural_coherence(l, r)
    return BinauralCues(float(itd), float(ild), ic)
>>>>>>> 9a0c6893 (Add missing modules: concept embeddings, mood ontology, spatial hearing, timbre perception, and 7 more)

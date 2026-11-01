"""Practice planning: spaced repetition, skill tracking, session planning."""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SkillRecord:
    name: str
    ease_factor: float = 2.5
    interval_days: float = 1.0
    repetitions: int = 0
    last_score: float = 0.0

    def next_review_interval(self, quality: int) -> float:
        q = min(max(quality, 0), 5)
        if q < 3:
            self.repetitions = 0
            self.interval_days = 1.0
        else:
            if self.repetitions == 0:
                self.interval_days = 1.0
            elif self.repetitions == 1:
                self.interval_days = 6.0
            else:
                self.interval_days *= self.ease_factor
            self.repetitions += 1
        self.ease_factor = max(
            1.3,
            self.ease_factor + 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02),
        )
        self.last_score = q / 5.0
        return self.interval_days


class SpacedRepetition:
    def __init__(self):
        self._skills: dict[str, SkillRecord] = {}

    def add_skill(self, name: str) -> SkillRecord:
        if name not in self._skills:
            self._skills[name] = SkillRecord(name=name)
        return self._skills[name]

    def review(self, name: str, quality: int) -> float:
        skill = self._skills.get(name)
        if skill is None:
            skill = self.add_skill(name)
        return skill.next_review_interval(quality)

    def due_skills(self, current_day: float = 0.0) -> list[str]:
        due = []
        for name, skill in self._skills.items():
            if skill.repetitions == 0 or current_day >= skill.interval_days:
                due.append(name)
        return due

    @property
    def skills(self) -> dict[str, SkillRecord]:
        return dict(self._skills)


class SkillTracker:
    def __init__(self):
        self._sessions: list[dict[str, Any]] = []
        self._skill_scores: dict[str, list[float]] = {}

    def log_session(self, skill: str, score: float, duration_min: float = 0.0) -> None:
        self._sessions.append({
            "skill": skill, "score": score, "duration_min": duration_min,
        })
        self._skill_scores.setdefault(skill, []).append(score)

    def trend(self, skill: str, window: int = 5) -> float:
        scores = self._skill_scores.get(skill, [])
        if len(scores) < 2:
            return 0.0
        recent = scores[-window:]
        if len(recent) < 2:
            return 0.0
        return recent[-1] - recent[0]

    def total_practice_minutes(self) -> float:
        return sum(s.get("duration_min", 0.0) for s in self._sessions)

    def average_score(self, skill: str) -> float:
        scores = self._skill_scores.get(skill, [])
        return sum(scores) / len(scores) if scores else 0.0


class PracticePlanner:
    def __init__(self, daily_minutes: float = 60.0):
        self._daily = daily_minutes

    def plan_session(
        self, skills: list[str], priorities: dict[str, float] | None = None,
    ) -> list[dict[str, float]]:
        if not skills:
            return []
        prio = priorities or {}
        total_weight = sum(prio.get(s, 1.0) for s in skills)
        plan = []
        for s in skills:
            w = prio.get(s, 1.0)
            minutes = self._daily * w / total_weight
            plan.append({"skill": s, "minutes": round(minutes, 1)})
        return plan

    def warmup_exercises(self, skill: str) -> list[str]:
        warmups = {
            "scales": ["chromatic scale", "major scale pattern", "minor scale pattern"],
            "arpeggios": ["major triad arpeggio", "minor triad arpeggio", "7th arpeggio"],
            "rhythm": ["metronome subdivision", "syncopation exercise"],
            "sight_reading": ["interval recognition", "rhythm reading"],
            "ear_training": ["interval singing", "chord quality identification"],
        }
        return warmups.get(skill, ["long tones", "slow scales"])

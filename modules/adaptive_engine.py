"""
Adaptive Difficulty & Cognitive Fatigue Engine (EDA-Engine).
Implements transparent, multi-parametric rule-based cognitive progression
and real-time agitation/fatigue detection for elderly patients with MCI/Dementia.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import numpy as np

@dataclass
class AdaptiveDecision:
    current_level: int
    next_level: int
    action: str  # "INCREASE", "MAINTAIN", "DECREASE", "FATIGUE_BREAK"
    composite_score: float
    accuracy_pct: float
    avg_response_time_sec: float
    fatigue_detected: bool
    explanation_en: str
    explanation_ta: str
    mathematical_rationale: str

class AdaptiveDifficultyEngine:
    def __init__(
        self,
        min_level: int = 1,
        max_level: int = 5,
        target_accuracy_upper: float = 80.0,
        target_accuracy_lower: float = 60.0,
        target_rt_upper_sec: float = 4.5,
        target_rt_lower_sec: float = 2.5,
        w_acc: float = 0.65,
        w_speed: float = 0.35,
        consecutive_error_fatigue_limit: int = 3
    ):
        self.min_level = min_level
        self.max_level = max_level
        self.target_accuracy_upper = target_accuracy_upper
        self.target_accuracy_lower = target_accuracy_lower
        self.target_rt_upper_sec = target_rt_upper_sec
        self.target_rt_lower_sec = target_rt_lower_sec
        self.w_acc = w_acc
        self.w_speed = w_speed
        self.consecutive_error_limit = consecutive_error_fatigue_limit

    def evaluate_session_performance(
        self,
        current_level: int,
        trial_results: List[Dict[str, Any]],
        max_allowed_time_per_trial: float = 10.0
    ) -> AdaptiveDecision:
        """
        Evaluates a batch of trials from a session and computes the next optimal difficulty level.
        
        trial_results: List of dicts with keys: {'is_correct': bool, 'response_time_sec': float}
        """
        if not trial_results:
            return AdaptiveDecision(
                current_level=current_level,
                next_level=current_level,
                action="MAINTAIN",
                composite_score=50.0,
                accuracy_pct=50.0,
                avg_response_time_sec=0.0,
                fatigue_detected=False,
                explanation_en="No trial data available. Maintaining current level.",
                explanation_ta="விவரங்கள் இல்லை. தற்போதைய நிலை தொடர்கிறது.",
                mathematical_rationale="N=0 trials."
            )

        n_trials = len(trial_results)
        correct_count = sum(1 for t in trial_results if t.get("is_correct", False))
        accuracy_pct = (correct_count / n_trials) * 100.0
        
        response_times = [float(t.get("response_time_sec", 3.0)) for t in trial_results]
        avg_rt = float(np.mean(response_times))
        rt_std = float(np.std(response_times)) if len(response_times) > 1 else 0.0

        # Calculate Normalized Speed Score S_speed in [0, 1]
        # Faster RT yields higher score (clamped between 0 and 1)
        speed_score = max(0.0, min(1.0, 1.0 - (avg_rt / max_allowed_time_per_trial)))
        
        # Normalized Accuracy Score in [0, 1]
        acc_score = accuracy_pct / 100.0

        # Composite Cognitive Performance Index C in [0, 100]
        composite_index = (self.w_acc * acc_score + self.w_speed * speed_score) * 100.0

        # Fatigue & Agitation Detection:
        # 1. Check for max consecutive errors
        consecutive_errors = 0
        max_consecutive_errors = 0
        for t in trial_results:
            if not t.get("is_correct", False):
                consecutive_errors += 1
                if consecutive_errors > max_consecutive_errors:
                    max_consecutive_errors = consecutive_errors
            else:
                consecutive_errors = 0

        # 2. Check for high RT volatility or sluggish response latency
        fatigue_detected = (
            max_consecutive_errors >= self.consecutive_error_limit or
            (avg_rt > (self.target_rt_upper_sec * 1.5) and accuracy_pct < 50.0)
        )

        # Determine Progression Action
        if fatigue_detected:
            action = "FATIGUE_BREAK"
            next_level = max(self.min_level, current_level - 1)
            explanation_en = f"Fatigue pattern detected ({max_consecutive_errors} repeated errors or high latency). Stepping down to Level {next_level} and prompting therapeutic breathing break."
            explanation_ta = f"சோர்வு முறை கண்டறியப்பட்டது ({max_consecutive_errors} பிழைகள்). நிலை {next_level}-க்கு எளிதாக்கப்பட்டு ஓய்வு பரிந்துரைக்கப்படுகிறது."
        elif accuracy_pct >= self.target_accuracy_upper and avg_rt <= self.target_rt_upper_sec:
            if current_level < self.max_level:
                action = "INCREASE"
                next_level = current_level + 1
                explanation_en = f"High mastery achieved (Accuracy: {accuracy_pct:.1f}%, Mean RT: {avg_rt:.2f}s). Advancing to Level {next_level}."
                explanation_ta = f"சிறந்த தேர்ச்சி (துல்லியம்: {accuracy_pct:.1f}%, வேகம்: {avg_rt:.2f}வி). அடுத்த நிலை {next_level}-க்கு முன்னேற்றம்."
            else:
                action = "MAINTAIN"
                next_level = self.max_level
                explanation_en = f"Maximum difficulty level ({self.max_level}) already reached with stellar performance."
                explanation_ta = f"உயர் நிலை ({self.max_level}) அடைந்துவிட்டார். தொடர்ந்து அதே நிலையில் பயிற்சி."
        elif accuracy_pct <= self.target_accuracy_lower or avg_rt > self.target_rt_upper_sec:
            if current_level > self.min_level:
                action = "DECREASE"
                next_level = current_level - 1
                explanation_en = f"Performance indicates cognitive load overload (Accuracy: {accuracy_pct:.1f}%, Mean RT: {avg_rt:.2f}s). Lowering complexity to Level {next_level}."
                explanation_ta = f"அதிக சுமை தவிர்க்க நிலை {next_level}-க்கு எளிதாக்கப்படுகிறது (துல்லியம்: {accuracy_pct:.1f}%)."
            else:
                action = "MAINTAIN"
                next_level = self.min_level
                explanation_en = "Patient at foundational level. Maintaining supportive exercises."
                explanation_ta = "அடிப்படை நிலையில் ஆதரவுப் பயிற்சிகள் தொடர்கின்றன."
        else:
            action = "MAINTAIN"
            next_level = current_level
            explanation_en = f"Stable performance in optimal learning zone (Accuracy: {accuracy_pct:.1f}%, Score: {composite_index:.1f}). Maintaining Level {current_level}."
            explanation_ta = f"சமநிலையான செயல்பாடு (துல்லியம்: {accuracy_pct:.1f}%). தற்போதைய நிலை {current_level} தொடர்கிறது."

        math_rationale = (
            f"Composite Score C = {self.w_acc:.2f}*(Acc={accuracy_pct:.1f}%) + "
            f"{self.w_speed:.2f}*(Speed={speed_score*100:.1f}%) = {composite_index:.2f}/100 | "
            f"Thresholds: Upper={self.target_accuracy_upper}%, Lower={self.target_accuracy_lower}%, "
            f"RT_mean={avg_rt:.2f}s (σ={rt_std:.2f}s)"
        )

        return AdaptiveDecision(
            current_level=current_level,
            next_level=next_level,
            action=action,
            composite_score=round(composite_index, 2),
            accuracy_pct=round(accuracy_pct, 1),
            avg_response_time_sec=round(avg_rt, 2),
            fatigue_detected=fatigue_detected,
            explanation_en=explanation_en,
            explanation_ta=explanation_ta,
            mathematical_rationale=math_rationale
        )

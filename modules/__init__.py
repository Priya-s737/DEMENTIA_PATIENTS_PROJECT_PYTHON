"""Core engineering & analytical modules for NeuroCare platform."""
from .adaptive_engine import AdaptiveDifficultyEngine, AdaptiveDecision
from .personalization import PersonalizationEngine
from .voice_assistant import VoiceAssistant
from .research_stats import ResearchStatsEngine
from .motivational_story import render_motivational_story, generate_login_cocomelon_hero_html
from .celebration import render_celebration, generate_celebration_stage_html, CELEBRATION_RHYMES

__all__ = [
    "AdaptiveDifficultyEngine",
    "AdaptiveDecision",
    "PersonalizationEngine",
    "VoiceAssistant",
    "ResearchStatsEngine",
    "render_motivational_story",
    "generate_login_cocomelon_hero_html",
    "render_celebration",
    "generate_celebration_stage_html",
    "CELEBRATION_RHYMES"
]

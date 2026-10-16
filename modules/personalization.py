"""
Personalization Engine for Reminiscence Therapy (RT) & Cognitive Anchoring.
Injects ALL caregiver-uploaded personal photos (people, places, objects, routines, pets) into games.
Strictly localized for 100% Pure Tamil and 100% Pure English modes without any mixed language.
Includes visual icons for daily routine sequencing activities.
"""

import os
import random
from typing import List, Dict, Any, Optional
from database.db_manager import DatabaseManager

TRANSLATION_MAP = {
    "mother": {"en": "Mother", "ta": "அம்மா / தாய்", "detail_en": "Mother", "detail_ta": "அம்மா"},
    "mom": {"en": "Mother", "ta": "அம்மா / தாய்", "detail_en": "Mother", "detail_ta": "அம்மா"},
    "father": {"en": "Father", "ta": "அப்பா / தந்தை", "detail_en": "Father", "detail_ta": "அப்பா"},
    "dad": {"en": "Father", "ta": "அப்பா / தந்தை", "detail_en": "Father", "detail_ta": "அப்பா"},
    "daughter": {"en": "Daughter", "ta": "மகள்", "detail_en": "Daughter", "detail_ta": "மகள்"},
    "son": {"en": "Son", "ta": "மகன்", "detail_en": "Son", "detail_ta": "மகன்"},
    "grandson": {"en": "Grandson", "ta": "பேரன்", "detail_en": "Grandson", "detail_ta": "பேரன்"},
    "granddaughter": {"en": "Granddaughter", "ta": "பேத்தி", "detail_en": "Granddaughter", "detail_ta": "பேத்தி"},
    "wife": {"en": "Wife", "ta": "மனைவி", "detail_en": "Wife", "detail_ta": "மனைவி"},
    "husband": {"en": "Husband", "ta": "கணவர்", "detail_en": "Husband", "detail_ta": "கணவர்"},
    "dog": {"en": "Pet Dog", "ta": "வளர்ப்பு நாய்", "detail_en": "Pet Dog", "detail_ta": "வளர்ப்பு நாய்"},
    "lucky": {"en": "Pet Dog", "ta": "வளர்ப்பு நாய்", "detail_en": "Pet Dog", "detail_ta": "வளர்ப்பு நாய்"},
    "taj mahal": {"en": "Taj Mahal", "ta": "தாஜ் மஹால்", "detail_en": "Taj Mahal", "detail_ta": "தாஜ் மஹால்"},
    "taj": {"en": "Taj Mahal", "ta": "தாஜ் மஹால்", "detail_en": "Taj Mahal", "detail_ta": "தாஜ் மஹால்"},
    "paint brush": {"en": "Paint Brush", "ta": "ஓவிய தூரிகை", "detail_en": "Paint Brush", "detail_ta": "ஓவிய தூரிகை"},
    "paintbrush": {"en": "Paint Brush", "ta": "ஓவிய தூரிகை", "detail_en": "Paint Brush", "detail_ta": "ஓவிய தூரிகை"},
    "தூரிகை": {"en": "Paint Brush", "ta": "ஓவிய தூரிகை", "detail_en": "Paint Brush", "detail_ta": "ஓவிய தூரிகை"},
    "toothbrush": {"en": "Toothbrush", "ta": "பல் துலக்கும் பிரஷ்", "detail_en": "Toothbrush", "detail_ta": "பல் துலக்கும் பிரஷ்"},
    "temple": {"en": "Meenakshi Temple", "ta": "மீனாட்சி அம்மன் கோவில்", "detail_en": "Temple", "detail_ta": "கோவில்"},
    "nature": {"en": "Nature & Greenery", "ta": "இயற்கை பசுமை காட்சி", "detail_en": "Nature", "detail_ta": "இயற்கை காட்சி"},
    "coffee": {"en": "Filter Coffee Tumbler", "ta": "காபி டம்ளர்", "detail_en": "Coffee Tumbler", "detail_ta": "காபி டம்ளர்"},
    "flute": {"en": "Carnatic Flute", "ta": "புல்லாங்குழல்", "detail_en": "Flute", "detail_ta": "புல்லாங்குழல்"},
    "spectacles": {"en": "Reading Glasses", "ta": "மூக்குக் கண்ணாடி", "detail_en": "Reading Glasses", "detail_ta": "மூக்குக் கண்ணாடி"}
}

class PersonalizationEngine:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def normalize_label(self, label: str, lang: str = "en") -> str:
        """Translates and cleans any label into pure selected language without mixed script or bracketed hints."""
        cleaned = label.strip().lower()
        for key, trans in TRANSLATION_MAP.items():
            if key in cleaned:
                return trans["ta"] if lang == "ta" else trans["en"]
        
        if lang == "ta" and label.isascii() and len(label) > 0:
            for key, trans in TRANSLATION_MAP.items():
                if any(w in cleaned for w in key.split()):
                    return trans["ta"]
            return "குடும்ப நினைவுப் படம்"
            
        return label

    def normalize_detail(self, detail: str, label: str, lang: str = "en") -> str:
        """Translates relation detail into pure selected language without revealing the answer."""
        combined = (label + " " + detail).strip().lower()
        for key, trans in TRANSLATION_MAP.items():
            if key in combined:
                return trans["detail_ta"] if lang == "ta" else trans["detail_en"]
        
        if lang == "ta" and (detail.isascii() or not detail):
            return "விருப்பமான நினைவு"
            
        return detail if detail else ("நினைவுப் படம்" if lang == "ta" else "Cherished Memory")

    def get_face_recall_stimuli(self, patient_id: int, difficulty_level: int = 1, lang: str = "en", exclude_ids: Optional[List[int]] = None) -> Dict[str, Any]:
        """
        Generates a familiar photo memory recognition challenge drawing ONLY from caregiver-uploaded photos.
        If no photos have been uploaded, returns has_photos=False so no mock questions/options appear.
        """
        all_patient_memories = self.db.get_patient_memories(patient_id)
        
        # Filter strictly for memories with existing, valid image files
        valid_photo_memories = []
        for m in all_patient_memories:
            img_p = m.get("image_path", "")
            if img_p:
                norm_p = os.path.normpath(img_p)
                if os.path.exists(norm_p) or os.path.exists(os.path.join(os.getcwd(), norm_p)):
                    valid_photo_memories.append(m)

        if not valid_photo_memories:
            return {
                "has_photos": False,
                "prompt": "புகைப்படங்கள் எதுவும் பதிவேற்றப்படவில்லை." if lang == "ta" else "No photos uploaded yet.",
                "image_path": "",
                "target": "",
                "options": [],
                "relation_cue": "",
                "category": "family",
                "memory_id": 0,
                "difficulty_level": difficulty_level
            }

        available_pool = [m for m in valid_photo_memories if m["id"] not in (exclude_ids or [])]
        if not available_pool:
            available_pool = valid_photo_memories

        distractor_pool_en = [
            "Mother", "Daughter", "Grandson", "Wife", "Husband",
            "Pet Dog", "Taj Mahal", "Paint Brush", "Nature & Greenery", "Meenakshi Temple"
        ]

        distractor_pool_ta = [
            "அம்மா / தாய்", "மகள்", "பேரன்", "மனைவி", "கணவர்",
            "வளர்ப்பு நாய்", "தாஜ் மஹால்", "ஓவிய தூரிகை", "இயற்கை பசுமை காட்சி", "மீனாட்சி அம்மன் கோவில்"
        ]

        target_mem = random.choice(available_pool)
        raw_lbl = target_mem.get("label_ta") if lang == "ta" and target_mem.get("label_ta") else target_mem.get("label_en", "")
        target_label = self.normalize_label(raw_lbl if raw_lbl else target_mem.get("label_en", ""), lang=lang)
        
        raw_detail = target_mem.get("detail_ta") if lang == "ta" and target_mem.get("detail_ta") else target_mem.get("detail_en", "")
        target_detail = self.normalize_detail(raw_detail, target_mem.get("label_en", ""), lang=lang)
        
        image_p = target_mem.get("image_path", "")
        category = target_mem.get("category", "family")
        target_id = target_mem["id"]

        if isinstance(difficulty_level, str):
            diff_map = {"easy": 1, "medium": 2, "hard": 3}
            lvl_val = diff_map.get(difficulty_level.lower(), 2)
        else:
            lvl_val = int(difficulty_level) if difficulty_level else 2

        if lvl_val <= 1:
            num_choices = 2
        elif lvl_val == 2:
            num_choices = 3
        else:
            num_choices = 4

        from modules.visual_assets import resolve_option_visual

        target_img, _ = resolve_option_visual(target_label, valid_photo_memories)
        target_img_name = os.path.basename(target_img).lower() if target_img else ""
        seen_images = {target_img_name}

        distractors = []
        # First priority: Other uploaded memories of this patient with distinct images
        for other_m in valid_photo_memories:
            if other_m["id"] != target_id:
                o_raw = other_m.get("label_ta") if lang == "ta" and other_m.get("label_ta") else other_m.get("label_en", "")
                o_lbl = self.normalize_label(o_raw, lang=lang)
                if o_lbl and o_lbl != target_label and o_lbl not in distractors:
                    o_img, _ = resolve_option_visual(o_lbl, valid_photo_memories)
                    o_img_name = os.path.basename(o_img).lower() if o_img else ""
                    if o_img_name and o_img_name not in seen_images:
                        seen_images.add(o_img_name)
                        distractors.append(o_lbl)

        # Second priority: General pool with strictly distinct images
        d_source = distractor_pool_ta if lang == "ta" else distractor_pool_en
        for d in d_source:
            if d != target_label and d not in distractors:
                d_img, _ = resolve_option_visual(d, valid_photo_memories)
                d_img_name = os.path.basename(d_img).lower() if d_img else ""
                if d_img_name and d_img_name not in seen_images:
                    seen_images.add(d_img_name)
                    distractors.append(d)

        chosen_distractors = distractors[:num_choices - 1]
        options = [target_label] + chosen_distractors
        random.shuffle(options)

        # Clean prompt without bracketed answers
        if category == "family":
            prompt_text = (
                "புகைப்படத்தில் உள்ளவர் யார் என்று அடையாளம் காணுங்கள்:"
                if lang == "ta"
                else "Who is shown in this photo?"
            )
        elif category == "place":
            prompt_text = (
                "இந்தப் புகைப்படத்தில் உள்ள இடம் எது?"
                if lang == "ta"
                else "Which place is shown in this photo?"
            )
        elif category == "object":
            prompt_text = (
                "இந்தப் புகைப்படத்தில் உள்ள பொருள் எது?"
                if lang == "ta"
                else "Which object is shown in this photo?"
            )
        else:
            prompt_text = (
                "இந்தப் புகைப்படம் எதைக் குறிக்கிறது?"
                if lang == "ta"
                else "What is shown in this photo?"
            )

        return {
            "has_photos": True,
            "prompt": prompt_text,
            "image_path": image_p,
            "target": target_label,
            "options": options,
            "relation_cue": target_detail,
            "category": category,
            "memory_id": target_id,
            "difficulty_level": difficulty_level
        }

    def get_timeline_sequencing_stimuli(self, patient_id: int, difficulty_level: int = 1, lang: str = "en") -> Dict[str, Any]:
        daily_routine_sets_en = [
            [
                "☕ Wake up and drink warm filter coffee",
                "📰 Read the morning newspaper on the porch",
                "💊 Take prescribed medicine after breakfast",
                "🚶‍♂️ Evening walk in the neighborhood park",
                "🎶 Enjoy dinner and listen to soothing devotional music"
            ],
            [
                "🪥 Brush teeth and wash face in the morning",
                "🍽️ Eat healthy breakfast with idli and sambar",
                "🌺 Water garden flower plants",
                "🛏️ Have a short afternoon resting nap",
                "📺 Watch evening news on television"
            ]
        ]

        daily_routine_sets_ta = [
            [
                "☕ காலை எழுந்து சுவையான பில்டர் காபி அருந்துதல்",
                "📰 வராண்டாவில் அமர்ந்து செய்தித்தாள் வாசித்தல்",
                "💊 காலை உணவுக்குப் பின் மருந்து மாத்திரை உட்கொள்ளுதல்",
                "🚶‍♂️ மாலை பூங்காவில் மிதமான நடைப்பயிற்சி",
                "🎶 இரவு உணவு உண்டு பக்திப் பாடல் கேட்டல்"
            ],
            [
                "🪥 காலையில் பல் துலக்கி முகம் கழுவுதல்",
                "🍽️ காலை இட்லி, சாம்பார் சாப்பிடுதல்",
                "🌺 வீட்டுத் தோட்டத்துச் செடிகளுக்குத் தண்ணீர் ஊற்றுதல்",
                "🛏️ மதிய உணவுக்குப் பின் சிறிது நேரம் ஓய்வெடுத்தல்",
                "📺 மாலையில் தொலைக்காட்சி செய்தி பார்த்தல்"
            ]
        ]

        if isinstance(difficulty_level, str):
            diff_map = {"easy": 1, "medium": 2, "hard": 3}
            t_lvl = diff_map.get(difficulty_level.lower(), 2)
        else:
            t_lvl = int(difficulty_level) if difficulty_level else 2

        if t_lvl <= 1:
            num_steps = 2
        elif t_lvl == 2:
            num_steps = 3
        else:
            num_steps = 4
        set_idx = random.randint(0, len(daily_routine_sets_en) - 1)
        
        full_steps = daily_routine_sets_ta[set_idx] if lang == "ta" else daily_routine_sets_en[set_idx]
        selected_steps = full_steps[:num_steps]
        
        scrambled_steps = list(selected_steps)
        while scrambled_steps == selected_steps:
            random.shuffle(scrambled_steps)

        prompt_text = (
            "கீழே உள்ள அன்றாட செயல்களை சரியான கால வரிசைப்படி அடுக்கவும்:"
            if lang == "ta"
            else "Arrange these daily routine steps in the correct chronological order:"
        )

        return {
            "prompt": prompt_text,
            "correct_sequence": selected_steps,
            "scrambled_steps": scrambled_steps,
            "difficulty_level": difficulty_level
        }

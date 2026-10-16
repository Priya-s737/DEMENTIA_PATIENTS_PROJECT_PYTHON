import os
import hashlib
from modules.voice_assistant import VoiceAssistant, AUDIO_CACHE_DIR

CELEBRATION_RHYMES = [
    {
        "id": "rhyme_bunny_balloons",
        "title_ta": "துள்ளும் முயலும் வண்ணப் பலூன்களும் 🎈🐰",
        "title_en": "The Dancing Bunny & Balloons 🎈🐰",
        "rhyme_ta": "வண்ண வண்ணப் பலூன்கள் வானில் பறக்குது பாரீர்! துள்ளும் குட்டி முயலும் மகிழ்ச்சியாய் ஆடுது கேளீர்! அற்புதம் பாட்டி, சரியான விடை! உங்கள் நினைவாற்றல் மின்னுகிறது!",
        "rhyme_en": "Balloons fly high into the cheerful sky, happy little bunnies dance and smile! Wonderful job Grandma, that is the exact right answer! You are amazing!",
        "animal": "🐰",
        "animal_name_ta": "துள்ளும் முயல் குட்டி",
        "animal_name_en": "Dancing Bunny"
    },
    {
        "id": "rhyme_sun_puppy",
        "title_ta": "புன்னகைக்கும் சூரியனும் செல்ல நாய்க்குட்டியும் ☀️🐶",
        "title_en": "The Smiling Sun & Joyful Puppy ☀️🐶",
        "rhyme_ta": "சூரியன் சிரிக்குது காலையிலே, பூக்கள் ஆடுது சோலையிலே! பாசமிகு தாத்தா சொன்ன பதில் மிகச் சரி! நீங்கள் என்றுமே எங்கள் நாயகன்!",
        "rhyme_en": "The morning sun is smiling bright, dancing flowers bring delight! Super memory Grandpa, you solved it with love and light! You are our hero!",
        "animal": "🐶",
        "animal_name_ta": "செல்ல நாய்க்குட்டி",
        "animal_name_en": "Playful Puppy"
    },
    {
        "id": "rhyme_rainbow_butterfly",
        "title_ta": "வண்ண வானவில்லும் வண்ணத்துப் பூச்சியும் 🌈🦋",
        "title_en": "The Magic Rainbow & Butterfly 🌈🦋",
        "rhyme_ta": "மழைவில் வண்ணங்கள் வானில் தெரியுது, வண்ணத்துப் பூச்சிகள் மெல்லப் பறக்குது! நினைவாற்றல் மேதை நீங்கள் பாட்டி, வெற்றி என்றும் உங்கள் கைகளில்!",
        "rhyme_en": "Look at the magic rainbow shine, gentle butterflies dance in line! Amazing memory Grandma, victory is yours every single time!",
        "animal": "🦋",
        "animal_name_ta": "வண்ணத்துப் பூச்சி",
        "animal_name_en": "Gentle Butterfly"
    },
    {
        "id": "rhyme_bear_elephant",
        "title_ta": "ஆடும் கரடி பொம்மையும் பாசமிகு அன்பும் 🐻🐘",
        "title_en": "The Dancing Bear & Friendly Elephant 🐻🐘",
        "rhyme_ta": "சின்னஞ்சிறு குருவி பாடுது பாட்டு, செல்லக் கரடி போடுது தாளம்! அருமையான வெற்றி தாத்தா, உங்கள் புன்னகைதான் எங்கள் செல்வம்!",
        "rhyme_en": "The friendly little teddy bear dances with cheer, sweet music fills the atmosphere! Outstanding job Grandpa, your smile is our greatest treasure!",
        "animal": "🐻",
        "animal_name_ta": "ஆடும் கரடி பொம்மை",
        "animal_name_en": "Dancing Bear"
    }
]

print("Pre-generating celebration rhyme audios...")
for idx, r in enumerate(CELEBRATION_RHYMES):
    ta_f = VoiceAssistant.get_audio_file_path(r["rhyme_ta"], lang="ta")
    en_f = VoiceAssistant.get_audio_file_path(r["rhyme_en"], lang="en")
    print(f"Rhyme {idx+1} [TA]: {ta_f} ({os.path.getsize(ta_f) if ta_f else 0} bytes)")
    print(f"Rhyme {idx+1} [EN]: {en_f} ({os.path.getsize(en_f) if en_f else 0} bytes)")

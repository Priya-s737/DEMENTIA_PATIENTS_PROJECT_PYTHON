import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

from database.db_manager import DatabaseManager
from modules.personalization import PersonalizationEngine
from modules.visual_assets import resolve_option_visual, ITEM_ASSET_MAPPING

db = DatabaseManager('database/neurocare.db')
pe = PersonalizationEngine(db)

print("=== CHECK 1: PATIENT 2 MEMORIES IN DB ===")
mems = db.get_patient_memories(2)
for m in mems:
    print(f"ID {m['id']}: EN='{m.get('label_en')}', TA='{m.get('label_ta')}', path='{m.get('image_path')}'")

print("\n=== CHECK 2: FACE RECALL STIMULI & OPTION IMAGES ===")
for lang in ['en', 'ta']:
    print(f"\n--- Testing Lang: {lang} ---")
    for i in range(10):
        stim = pe.get_face_recall_stimuli(2, difficulty_level=2, lang=lang)
        target = stim['target']
        img_file = os.path.basename(stim['image_path'])
        opts = stim['options']
        opt_imgs = [os.path.basename(resolve_option_visual(o, mems)[0]) for o in opts]
        
        has_dup = len(opt_imgs) != len(set(opt_imgs))
        status = "FAIL - DUPLICATES" if has_dup else "PASS"
        print(f"Trial {i+1} [{status}]: Target='{target}' (file: {img_file})")
        print(f"   Options: {opts}")
        print(f"   Images:  {opt_imgs}")
        assert not has_dup, f"Duplicate images found: {opt_imgs}"

print("\n=== CHECK 3: PAINT BRUSH RESOLUTION ===")
pb_en_img, pb_en_icon = resolve_option_visual("Paint Brush")
pb_ta_img, pb_ta_icon = resolve_option_visual("ஓவிய தூரிகை")
tb_en_img, tb_en_icon = resolve_option_visual("Toothbrush")
tb_ta_img, tb_ta_icon = resolve_option_visual("பல் துலக்கும் பிரஷ்")

print(f"Paint Brush (EN): {os.path.basename(pb_en_img)} {pb_en_icon}")
print(f"Paint Brush (TA): {os.path.basename(pb_ta_img)} {pb_ta_icon}")
print(f"Toothbrush  (EN): {os.path.basename(tb_en_img)} {tb_en_icon}")
print(f"Toothbrush  (TA): {os.path.basename(tb_ta_img)} {tb_ta_icon}")

assert "paintbrush" in os.path.basename(pb_en_img).lower() or "screenshot" in os.path.basename(pb_en_img).lower(), "Paint brush does not resolve to paint brush"
assert "paintbrush" in os.path.basename(pb_ta_img).lower() or "screenshot" in os.path.basename(pb_ta_img).lower(), "Paint brush (TA) does not resolve to paint brush"
assert "toothbrush" in os.path.basename(tb_en_img).lower(), "Toothbrush does not resolve to toothbrush"
assert "toothbrush" in os.path.basename(tb_ta_img).lower(), "Toothbrush (TA) does not resolve to toothbrush"

print("\nALL ASSERTIONS PASSED!")

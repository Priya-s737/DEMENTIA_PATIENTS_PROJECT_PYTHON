import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

from modules.visual_assets import resolve_distinct_option_visuals, resolve_option_visual
from games.language_games import OBJECT_ITEMS
import re

print("=== 1. TEST OBJECT NAMING IN LANGUAGE GAMES ===")
all_names_en = [o['en'] for o in OBJECT_ITEMS]
all_names_ta = [o['ta'] for o in OBJECT_ITEMS]

vis_en = resolve_distinct_option_visuals(all_names_en)
vis_ta = resolve_distinct_option_visuals(all_names_ta)

imgs_en = [os.path.basename(v[0]) for v in vis_en]
imgs_ta = [os.path.basename(v[0]) for v in vis_ta]

print("EN Objects:", all_names_en)
print("EN Images :", imgs_en)
assert len(imgs_en) == len(set(imgs_en)), "Duplicate images in EN objects!"

print("\nTA Objects:", all_names_ta)
print("TA Images :", imgs_ta)
assert len(imgs_ta) == len(set(imgs_ta)), "Duplicate images in TA objects!"

print("\n=== 2. TEST CATEGORY TASKS IN LANGUAGE GAMES ===")
# Read directly from file
with open("games/language_games.py", "r", encoding="utf-8") as f:
    lang_code = f.read()

# Extract category_tasks_en and category_tasks_ta
tasks_en_match = re.search(r'category_tasks_en = (\[.*?\]\n\s*\])', lang_code, re.DOTALL)
tasks_ta_match = re.search(r'category_tasks_ta = (\[.*?\]\n\s*\])', lang_code, re.DOTALL)

exec_dict = {}
if tasks_en_match:
    exec(f"tasks_en = {tasks_en_match.group(1)}", exec_dict)
    for idx, t in enumerate(exec_dict["tasks_en"]):
        vis = resolve_distinct_option_visuals(t["options"])
        imgs = [os.path.basename(v[0]) for v in vis]
        print(f"EN Cat Task {idx+1}: {t['options']} -> {imgs}")
        assert len(imgs) == len(set(imgs)), f"Duplicate in EN Cat Task {idx+1}"

if tasks_ta_match:
    exec(f"tasks_ta = {tasks_ta_match.group(1)}", exec_dict)
    for idx, t in enumerate(exec_dict["tasks_ta"]):
        vis = resolve_distinct_option_visuals(t["options"])
        imgs = [os.path.basename(v[0]) for v in vis]
        print(f"TA Cat Task {idx+1}: {t['options']} -> {imgs}")
        assert len(imgs) == len(set(imgs)), f"Duplicate in TA Cat Task {idx+1}"

print("\n=== 3. TEST SPATIAL TASKS IN ORIENTATION GAMES ===")
with open("games/orientation_games.py", "r", encoding="utf-8") as f:
    ori_code = f.read()

ori_en_match = re.search(r'spatial_tasks_en = (\[.*?\]\n\s*\])', ori_code, re.DOTALL)
ori_ta_match = re.search(r'spatial_tasks_ta = (\[.*?\]\n\s*\])', ori_code, re.DOTALL)

if ori_en_match:
    exec(f"spat_en = {ori_en_match.group(1)}", exec_dict)
    for idx, t in enumerate(exec_dict["spat_en"]):
        vis = resolve_distinct_option_visuals(t["options"])
        imgs = [os.path.basename(v[0]) for v in vis]
        print(f"EN Spatial Task {idx+1}: {t['options']} -> {imgs}")
        assert len(imgs) == len(set(imgs)), f"Duplicate in EN Spatial Task {idx+1}"

if ori_ta_match:
    exec(f"spat_ta = {ori_ta_match.group(1)}", exec_dict)
    for idx, t in enumerate(exec_dict["spat_ta"]):
        vis = resolve_distinct_option_visuals(t["options"])
        imgs = [os.path.basename(v[0]) for v in vis]
        print(f"TA Spatial Task {idx+1}: {t['options']} -> {imgs}")
        assert len(imgs) == len(set(imgs)), f"Duplicate in TA Spatial Task {idx+1}"

print("\n=== 4. TEST TEMPORAL (DAYS OF WEEK) IN ORIENTATION GAMES ===")
days_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
days_ta = ["திங்கட்கிழமை", "செவ்வாய்க்கிழமை", "புதன்கிழமை", "வியாழக்கிழமை", "வெள்ளிக்கிழமை", "சனிக்கிழமை", "ஞாயிற்றுக்கிழமை"]

vis_days_en = resolve_distinct_option_visuals(days_en)
imgs_days_en = [os.path.basename(v[0]) for v in vis_days_en]
print("Days EN:", days_en)
print("Images  :", imgs_days_en)
assert len(imgs_days_en) == len(set(imgs_days_en)), "Duplicate images in EN days!"

vis_days_ta = resolve_distinct_option_visuals(days_ta)
imgs_days_ta = [os.path.basename(v[0]) for v in vis_days_ta]
print("Days TA:", days_ta)
print("Images  :", imgs_days_ta)
assert len(imgs_days_ta) == len(set(imgs_days_ta)), "Duplicate images in TA days!"

print("\nALL OPTION SETS IN ALL GAMES HAVE 100% DISTINCT, NON-REPEATING IMAGES!")

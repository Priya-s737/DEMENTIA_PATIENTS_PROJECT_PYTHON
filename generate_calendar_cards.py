import os
from PIL import Image, ImageDraw, ImageFont

cards_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads", "visual_cards")
os.makedirs(cards_dir, exist_ok=True)

# SPECIFIC VIBRANT COLORS REQUESTED BY USER:
# Tuesday: BLUE (User requirement)
# Thursday: YELLOW (User requirement)
# Sunday: RED
# Wednesday: GREEN
# Monday: CYAN / TEAL
# Friday: ROSE / PINK
# Saturday: PURPLE / VIOLET

days_data = [
    {
        "filename": "day_monday.png",
        "name_en": "MONDAY",
        "abbr_en": "MON",
        "primary_rgb": (14, 165, 233),      # Cyan / Light Blue
        "dark_rgb": (2, 132, 199),
        "light_rgb": (240, 249, 255),
        "text_on_header": (255, 255, 255)
    },
    {
        "filename": "day_tuesday.png",
        "name_en": "TUESDAY",
        "abbr_en": "TUE",
        "primary_rgb": (37, 99, 235),       # Vibrant Royal Blue (User requirement)
        "dark_rgb": (29, 78, 216),
        "light_rgb": (239, 246, 255),
        "text_on_header": (255, 255, 255)
    },
    {
        "filename": "day_wednesday.png",
        "name_en": "WEDNESDAY",
        "abbr_en": "WED",
        "primary_rgb": (22, 163, 74),       # Fresh Emerald Green
        "dark_rgb": (21, 128, 61),
        "light_rgb": (240, 253, 244),
        "text_on_header": (255, 255, 255)
    },
    {
        "filename": "day_thursday.png",
        "name_en": "THURSDAY",
        "abbr_en": "THU",
        "primary_rgb": (234, 179, 8),       # Vibrant Sun Yellow (User requirement)
        "dark_rgb": (180, 83, 9),           # Deep Amber contrast
        "light_rgb": (254, 252, 232),
        "text_on_header": (120, 53, 15)      # Dark contrast text for yellow banner
    },
    {
        "filename": "day_friday.png",
        "name_en": "FRIDAY",
        "abbr_en": "FRI",
        "primary_rgb": (236, 72, 153),      # Bright Pink / Rose
        "dark_rgb": (190, 24, 93),
        "light_rgb": (253, 242, 248),
        "text_on_header": (255, 255, 255)
    },
    {
        "filename": "day_saturday.png",
        "name_en": "SATURDAY",
        "abbr_en": "SAT",
        "primary_rgb": (139, 92, 246),      # Deep Purple / Violet
        "dark_rgb": (109, 40, 217),
        "light_rgb": (245, 243, 255),
        "text_on_header": (255, 255, 255)
    },
    {
        "filename": "day_sunday.png",
        "name_en": "SUNDAY",
        "abbr_en": "SUN",
        "primary_rgb": (239, 68, 68),       # Vibrant Crimson Red
        "dark_rgb": (185, 28, 28),
        "light_rgb": (254, 242, 242),
        "text_on_header": (255, 255, 255)
    }
]

# Load fonts
font_abbr = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 78)
font_name_en = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 32)
font_header = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)
font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)

for day in days_data:
    filepath = os.path.join(cards_dir, day["filename"])
    
    # 400x300 Standardized Visual Card Dimensions
    img = Image.new("RGB", (400, 300), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Soft tinted background & solid colored border
    draw.rounded_rectangle([4, 4, 396, 296], radius=16, fill=day["light_rgb"], outline=day["dark_rgb"], width=4)
    
    # Calendar Top Banner with Day's Specific Color
    draw.rounded_rectangle([6, 6, 394, 76], radius=14, fill=day["primary_rgb"])
    draw.rectangle([6, 45, 394, 76], fill=day["primary_rgb"])
    
    # Realistic Calendar Binding Rings
    draw.rounded_rectangle([70, 2, 86, 18], radius=4, fill=(226, 232, 240), outline=(100, 116, 139), width=2)
    draw.rounded_rectangle([314, 2, 330, 18], radius=4, fill=(226, 232, 240), outline=(100, 116, 139), width=2)
    
    # Header Banner Text
    draw.text((200, 42), "CALENDAR", fill=day["text_on_header"], font=font_header, anchor="mm")
    
    # Giant Bold Day Abbreviation (TUE, THU, MON...) in Theme Color
    draw.text((200, 132), day["abbr_en"], fill=day["dark_rgb"], font=font_abbr, anchor="mm")
    
    # Full English Day Name (High Contrast Dark Slate)
    draw.text((200, 202), day["name_en"], fill=(15, 23, 42), font=font_name_en, anchor="mm")
    
    # Bottom Badge Pill
    draw.rounded_rectangle([60, 245, 340, 282], radius=10, fill=day["dark_rgb"])
    draw.text((200, 263), day['name_en'], fill=(255, 255, 255), font=font_badge, anchor="mm")
    
    img.save(filepath, "PNG")
    print(f"Generated {day['filename']}")

print("All 7 calendar day cards regenerated successfully!")

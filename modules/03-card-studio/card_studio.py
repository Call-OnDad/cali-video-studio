"""card_studio.py — Cali Card Studio Standalone Generator.

Generates high-retention 9:16 vertical presentation cards, role intros, and checklist b-roll
with strict aspect-ratio contain scaling (never cuts off avatar heads or limbs).

CLI Usage:
    python card_studio.py --art avatar.png --title "Code & Architecture" --badge "ROLE 01" --output card.png
"""
import sys
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 720, 1280
BG_COLOR = (11, 21, 38, 255)


def generate_card(
    art_path: Path,
    badge_text: str,
    title_text: str,
    bullets: list,
    highlight_label: str,
    highlight_text: str,
    highlight_color: str,
    out_path: Path
):
    im = Image.new("RGBA", (W, H), BG_COLOR)
    d = ImageDraw.Draw(im)

    # Top Cyan Accent Strip
    d.rectangle([(0, 0), (W, 8)], fill="#38bdf8")

    # Category Pill
    font_bold = ImageFont.load_default()
    b_box_x, b_box_y = 40, 35
    d.rounded_rectangle([(b_box_x, b_box_y), (W - b_box_x, b_box_y + 38)], radius=19, fill="#0f2744", outline="#38bdf8", width=2)
    d.text((W // 2, b_box_y + 19), badge_text, font=font_bold, fill="#38bdf8", anchor="mm")

    # Title
    d.text((W // 2, 95), title_text, font=font_bold, fill="#ffffff", anchor="mm")

    # Avatar Hero Window (Contain scaling - Head and limbs preserved)
    art_w, art_h = 640, 440
    art_x = (W - art_w) // 2
    art_y = 150

    if art_path and Path(art_path).exists():
        raw_art = Image.open(art_path).convert("RGBA")
        scale = min(art_w / raw_art.width, art_h / raw_art.height)
        new_w = int(raw_art.width * scale)
        new_h = int(raw_art.height * scale)
        scaled_art = raw_art.resize((new_w, new_h), Image.Resampling.LANCZOS)

        art_canvas = Image.new("RGBA", (art_w, art_h), BG_COLOR)
        paste_x = (art_w - new_w) // 2
        paste_y = (art_h - new_h) // 2
        art_canvas.paste(scaled_art, (paste_x, paste_y), scaled_art)

        mask = Image.new("L", (art_w, art_h), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (art_w, art_h)], radius=20, fill=255)
        im.paste(art_canvas, (art_x, art_y), mask)
        d.rounded_rectangle([(art_x, art_y), (art_x + art_w, art_y + art_h)], radius=20, outline="#38bdf8", width=2)
    else:
        d.rounded_rectangle([(art_x, art_y), (art_x + art_w, art_y + art_h)], radius=20, fill="#172554", outline="#38bdf8", width=2)

    # Content Container
    card_margin = 40
    card_top = 610
    card_bot = 1180
    d.rounded_rectangle([(card_margin, card_top), (W - card_margin, card_bot)], radius=22, fill="#132238", outline="#334155", width=2)

    cur_y = card_top + 28
    for i, item in enumerate(bullets, 1):
        num_circle_x = card_margin + 34
        num_circle_y = cur_y + 16
        num_r = 16
        d.ellipse(
            [(num_circle_x - num_r, num_circle_y - num_r), (num_circle_x + num_r, num_circle_y + num_r)],
            fill="#0284c7", outline="#38bdf8", width=2
        )
        d.text((num_circle_x, num_circle_y), str(i), font=font_bold, fill="#ffffff", anchor="mm")
        
        head = item if isinstance(item, str) else item[0]
        sub = "" if isinstance(item, str) or len(item) < 2 else item[1]
        
        d.text((card_margin + 66, cur_y), head, font=font_bold, fill="#f8fafc")
        if sub:
            d.text((card_margin + 66, cur_y + 24), sub, font=font_bold, fill="#94a3b8")
        cur_y += 85

    # Highlight Callout Box
    box_h = 96
    box_y = card_bot - box_h - 20
    box_x1 = card_margin + 20
    box_x2 = W - card_margin - 20
    d.rounded_rectangle([(box_x1, box_y), (box_x2, box_y + box_h)], radius=14, fill="#0b172a", outline=highlight_color, width=2)
    d.text(((box_x1 + box_x2) // 2, box_y + 20), highlight_label, font=font_bold, fill=highlight_color, anchor="mm")
    d.text(((box_x1 + box_x2) // 2, box_y + 55), highlight_text, font=font_bold, fill="#e2e8f0", anchor="mm")

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").save(out_path, quality=95)
    print(f"[Cali Card Studio] Saved card -> {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Cali Card Studio — 9:16 Vertical Scene Card Generator")
    parser.add_argument("--art", "-a", help="Avatar image path")
    parser.add_argument("--badge", default="CREW SPOTLIGHT", help="Category badge pill text")
    parser.add_argument("--title", "-t", default="Core Responsibilities", help="Card main title")
    parser.add_argument("--output", "-o", default="scene_card.png", help="Output PNG path")
    parser.add_argument("--highlight-label", default="PRIMARY FOCUS", help="Highlight box title")
    parser.add_argument("--highlight-text", default="Automate workflows and build clean tools.", help="Highlight box text")
    parser.add_argument("--highlight-color", default="#f59e0b", help="Highlight border color")

    args = parser.parse_args()
    bullets = [
        ("Full-Stack Development", "Writing clean, high-performance web applications"),
        ("API Architecture", "Connecting databases and services without bloat"),
        ("Continuous Deployment", "Shipping bug fixes and updates directly to production")
    ]
    generate_card(
        Path(args.art) if args.art else None,
        args.badge,
        args.title,
        bullets,
        args.highlight_label,
        args.highlight_text,
        args.highlight_color,
        Path(args.output)
    )


if __name__ == "__main__":
    main()

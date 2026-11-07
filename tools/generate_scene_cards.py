"""generate_scene_cards.py — Production scene card generator for Cali Video Studio.

Features:
- Aspect-ratio preserved 'contain' scaling for full-body avatars (never cuts off heads or feet).
- Professional dark navy branding, badges, bullets, and highlight boxes.
- 720x1280 (9:16) vertical video format standard.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 720, 1280
BG_COLOR = (11, 21, 38, 255)  # Studio Navy


def render_contain_art(canvas: Image.Image, art_path: Path, box_x: int, box_y: int, box_w: int, box_h: int):
    """Renders avatar art fitted completely inside the bounding box preserving aspect ratio."""
    d = ImageDraw.Draw(canvas)
    if art_path and art_path.exists():
        raw_art = Image.open(art_path).convert("RGBA")
        
        # Calculate contain scale
        scale = min(box_w / raw_art.width, box_h / raw_art.height)
        new_w = int(raw_art.width * scale)
        new_h = int(raw_art.height * scale)
        scaled_art = raw_art.resize((new_w, new_h), Image.Resampling.LANCZOS)

        # Background letterbox canvas matching studio navy
        art_canvas = Image.new("RGBA", (box_w, box_h), BG_COLOR)
        paste_x = (box_w - new_w) // 2
        paste_y = (box_h - new_h) // 2
        art_canvas.paste(scaled_art, (paste_x, paste_y), scaled_art)

        # Rounded corner mask
        mask = Image.new("L", (box_w, box_h), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (box_w, box_h)], radius=20, fill=255)
        canvas.paste(art_canvas, (box_x, box_y), mask)
        d.rounded_rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)], radius=20, outline="#38bdf8", width=2)
    else:
        d.rounded_rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)], radius=20, fill="#172554", outline="#38bdf8", width=2)


def render_scene_card(
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

    # Top accent strip
    d.rectangle([(0, 0), (W, 8)], fill="#38bdf8")

    # Category Pill
    font_bold = ImageFont.load_default()
    b_box_x, b_box_y = 40, 35
    d.rounded_rectangle([(b_box_x, b_box_y), (W - b_box_x, b_box_y + 38)], radius=19, fill="#0f2744", outline="#38bdf8", width=2)
    d.text((W // 2, b_box_y + 19), badge_text, font=font_bold, fill="#38bdf8", anchor="mm")

    # Title
    d.text((W // 2, 95), title_text, font=font_bold, fill="#ffffff", anchor="mm")

    # Avatar Hero Window (Contain scaling - Head and limbs completely preserved)
    art_w, art_h = 640, 440
    art_x = (W - art_w) // 2
    art_y = 150
    render_contain_art(im, art_path, art_x, art_y, art_w, art_h)

    # Content Card
    card_margin = 40
    card_top = 610
    card_bot = 1180
    d.rounded_rectangle([(card_margin, card_top), (W - card_margin, card_bot)], radius=22, fill="#132238", outline="#334155", width=2)

    cur_y = card_top + 28
    for i, (head, sub) in enumerate(bullets, 1):
        num_circle_x = card_margin + 34
        num_circle_y = cur_y + 16
        num_r = 16
        d.ellipse(
            [(num_circle_x - num_r, num_circle_y - num_r), (num_circle_x + num_r, num_circle_y + num_r)],
            fill="#0284c7", outline="#38bdf8", width=2
        )
        d.text((num_circle_x, num_circle_y), str(i), font=font_bold, fill="#ffffff", anchor="mm")
        d.text((card_margin + 66, cur_y), head, font=font_bold, fill="#f8fafc")
        d.text((card_margin + 66, cur_y + 24), sub, font=font_bold, fill="#94a3b8")
        cur_y += 85

    # Highlight box
    box_h = 96
    box_y = card_bot - box_h - 20
    box_x1 = card_margin + 20
    box_x2 = W - card_margin - 20
    d.rounded_rectangle([(box_x1, box_y), (box_x2, box_y + box_h)], radius=14, fill="#0b172a", outline=highlight_color, width=2)
    d.text(((box_x1 + box_x2) // 2, box_y + 20), highlight_label, font=font_bold, fill=highlight_color, anchor="mm")
    d.text(((box_x1 + box_x2) // 2, box_y + 55), highlight_text, font=font_bold, fill="#e2e8f0", anchor="mm")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").save(out_path, quality=95)
    print(f"Card generated: {out_path.name}")

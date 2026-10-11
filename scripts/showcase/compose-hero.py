"""Compose the README hero image (Vesper).

The hero is a MOCKUP, not a screenshot: real captures of the app (never altered inside the window)
are placed in a drawn Windows-style frame, over a blurred copy of the demonstration media, beside
the app's own icon and name. It adds nothing to the product's UI. docs/MEDIA-CREDITS.md says what
every picture is and where the media comes from.

Needs Pillow and numpy and the local, git-ignored demonstration media described in
docs/MEDIA-CREDITS.md ("Reproducing the pictures"). From the repository root:

    python scripts/showcase/compose-hero.py
"""
import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]

FONT = r"C:\Windows\Fonts\SegUIVar.ttf"


def font(size, weight=400):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([weight, min(36, max(5, size * 0.5))])
    return f


def cover(img, w, h):
    s = max(w / img.width, h / img.height)
    im = img.resize((math.ceil(img.width * s), math.ceil(img.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def backdrop(media, w, h, accent, tint=0.62, left_dark=0.94):
    bg = cover(media.convert("RGB"), w, h).filter(ImageFilter.GaussianBlur(46))
    bg = ImageEnhance.Brightness(bg).enhance(tint)
    bg = ImageEnhance.Color(bg).enhance(1.2)
    a = np.asarray(bg).astype(np.float32)
    # Darker on the text side, so the name stays readable whatever the media is.
    x = np.linspace(0.0, 1.0, w, dtype=np.float32)[None, :, None]
    dark = left_dark * np.clip(1.0 - x * 1.15, 0.0, 1.0) ** 1.1
    a = a * (1 - dark) + np.array([13, 14, 17], dtype=np.float32) * dark
    # A soft glow of the app's accent colour behind the icon.
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    g = np.exp(-(((xx - 260) / 520) ** 2 + ((yy - 300) / 460) ** 2))[..., None]
    a = a + (np.array(accent, dtype=np.float32) - a) * g * 0.28
    # A little grain, so the blurred gradients do not band.
    a = a + np.random.default_rng(7).normal(0, 2.0, (h, w, 1)).astype(np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")


def rounded(img, radius):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius, fill=255)
    out = img.convert("RGBA")
    out.putalpha(mask)
    return out


def window(capture, title, icon, dark=True, width=1100, bar=32):
    """The capture inside a Windows 11 style frame: title bar, caption buttons, rounded corners."""
    cap = capture.convert("RGB")
    if cap.width != width:
        cap = cap.resize((width, round(cap.height * width / cap.width)), Image.LANCZOS)
    h = cap.height + bar
    frame = Image.new("RGB", (width, h), (32, 32, 35) if dark else (243, 243, 245))
    frame.paste(cap, (0, bar))
    d = ImageDraw.Draw(frame)
    ink = (236, 236, 240) if dark else (30, 30, 34)
    ic = icon.resize((16, 16), Image.LANCZOS)
    frame.paste(ic, (12, (bar - 16) // 2), ic)
    d.text((38, bar // 2), title, font=font(12, 400), fill=ink, anchor="lm")
    for i, glyph in enumerate(("min", "max", "close")):
        cx = width - 46 * (3 - i) + 23
        cy = bar // 2
        if glyph == "min":
            d.line((cx - 5, cy, cx + 5, cy), fill=ink, width=1)
        elif glyph == "max":
            d.rectangle((cx - 5, cy - 5, cx + 5, cy + 5), outline=ink, width=1)
        else:
            d.line((cx - 5, cy - 5, cx + 5, cy + 5), fill=ink, width=1)
            d.line((cx - 5, cy + 5, cx + 5, cy - 5), fill=ink, width=1)
    out = rounded(frame, 10)
    edge = Image.new("RGBA", out.size, (0, 0, 0, 0))
    ImageDraw.Draw(edge).rounded_rectangle((0, 0, out.width - 1, out.height - 1), 10, outline=(255, 255, 255, 38), width=1)
    return Image.alpha_composite(out, edge)


def shadow(size, radius=10, blur=38, alpha=170):
    pad = blur * 3
    s = Image.new("RGBA", (size[0] + pad * 2, size[1] + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle((pad, pad, pad + size[0], pad + size[1]), radius, fill=(0, 0, 0, alpha))
    return s.filter(ImageFilter.GaussianBlur(blur)), pad


def place(canvas, win, xy, dim=0.0, shadow_alpha=170, shadow_dy=26):
    sh, pad = shadow(win.size, alpha=shadow_alpha)
    canvas.alpha_composite(sh, (xy[0] - pad, xy[1] - pad + shadow_dy))
    if dim:
        veil = Image.new("RGBA", win.size, (0, 0, 0, int(255 * dim)))
        veil.putalpha(ImageChops.multiply(veil.getchannel("A"), win.getchannel("A")))
        win = Image.alpha_composite(win, veil)
    canvas.alpha_composite(win, xy)


def wrap(draw, text, fnt, width):
    words, lines, line = text.split(), [], ""
    for w in words:
        trial = (line + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            lines.append(line)
            line = w
    lines.append(line)
    return lines


def hero(out, *, name, tagline, caption, accent, icon_path, media_path, front, front_title, front_dark=True,
         back=None, back_title=None, back_dark=False, back_offset=(120, -112), size=(1920, 1040)):
    """front = the main capture; back = a second real capture (other theme) peeking from behind it."""
    W, H = size
    media = Image.open(media_path)
    canvas = backdrop(media, W, H, accent).convert("RGBA")
    icon = Image.open(icon_path).convert("RGBA")
    fw = window(Image.open(front), front_title, icon, dark=front_dark)
    fx, fy = W - fw.width - 64, (H - fw.height) // 2 + 36
    if back:
        bw = window(Image.open(back), back_title or front_title, icon, dark=back_dark, width=round(1100 * 0.94))
        place(canvas, bw, (fx + back_offset[0], fy + back_offset[1]), dim=0.16, shadow_alpha=150, shadow_dy=18)
    place(canvas, fw, (fx, fy))
    d = ImageDraw.Draw(canvas)
    # Text column.
    x = 92
    big = icon.resize((176, 176), Image.LANCZOS)
    canvas.alpha_composite(big, (x - 14, 230))
    d.text((x, 432), name, font=font(124, 640), fill=(246, 246, 249))
    f = font(36, 360)
    y = 616
    for line in wrap(d, tagline, f, fx - x - 56):
        d.text((x, y), line, font=f, fill=(212, 214, 222))
        y += 52
    d.rounded_rectangle((x, y + 24, x + 74, y + 29), 3, fill=accent)
    d.text((x, y + 58), caption, font=font(25, 420), fill=(150, 154, 166))
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(out, quality=92, subsampling=0, optimize=True)
    print("wrote", out, canvas.size)


if __name__ == "__main__":
    C = ROOT / "demo-media" / "captures"
    hero(
        ROOT / "docs" / "media" / "hero.jpg",
        name="Vesper",
        tagline="A native video player for Windows. Responsive loading, 4K decoding and practical subtitle controls.",
        caption="Windows x64  \u00b7  no accounts  \u00b7  no telemetry",
        accent=(164, 139, 255),
        icon_path=ROOT / "shared" / "assets" / "vesper" / "icon-256.png",
        media_path=ROOT / "demo-media" / "work" / "backdrop.png",
        front=C / "bridge/composite-dark-150.png",
        front_title="Vesper",
        back=C / "bridge/composite-start-light.png",
        back_title="Vesper",
        back_dark=False,
        back_offset=(110, -150),
    )

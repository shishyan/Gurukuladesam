from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

root = Path(__file__).resolve().parent
for slug in ("rathinagiri_1", "rathinagiri_2", "seer_ulaaviya"):
    sheet = Image.new("RGB", (1200, 720), "#111111")
    draw = ImageDraw.Draw(sheet)
    for i, p in enumerate(sorted((root / slug).glob("S[0-9][0-9].png"))):
        im = Image.open(p).convert("RGB")
        im = ImageOps.fit(im, (290, 220))
        x, y = (i % 4) * 300 + 5, (i // 4) * 240 + 5
        sheet.paste(im, (x, y))
        draw.text((x + 4, y + 194), p.stem, fill="white", stroke_width=2, stroke_fill="black")
    sheet.save(root / slug / "contact.jpg", quality=90)


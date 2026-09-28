from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

root = Path(__file__).resolve().parent
prod = root.parent
folders = [prod / 'next-five-image-motion' / n for n in ('koumaram', 'muthai')]
folders += [prod / 'kaiththala-film', prod / 'new-unique-batch-2' / 'naatha_vindhugal']
for folder in folders:
    files = sorted(folder.glob('S[0-9][0-9].png'))
    sheet = Image.new('RGB', (1200, 720), '#111111')
    draw = ImageDraw.Draw(sheet)
    for i, path in enumerate(files[:12]):
        im = ImageOps.fit(Image.open(path).convert('RGB'), (290, 220))
        x, y = i % 4 * 300 + 5, i // 4 * 240 + 5
        sheet.paste(im, (x, y))
        draw.text((x + 4, y + 194), path.stem, fill='white', stroke_width=2, stroke_fill='black')
    sheet.save(root / f'{folder.name}-{folder.parent.name}-sheet.jpg', quality=88)

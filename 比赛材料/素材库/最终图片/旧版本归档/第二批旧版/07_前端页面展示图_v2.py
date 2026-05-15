from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

W, H = 1280, 1680
BG = '#FFFFFF'
PAGE = '#FAFBFA'
BORDER = '#D1D5DB'
TITLE = '#1F2937'
SUB = '#6B7280'
GREEN = '#2E6B4F'
PALE_GREEN = '#E8F3EC'
BLUE = '#355C8A'
PALE_BLUE = '#EAF0F8'
AMBER = '#A46A1F'
PALE_AMBER = '#F7F3EA'

FONT = '/System/Library/Fonts/PingFang.ttc'

def font(size, bold=False):
    idx = 0 if not bold else 0
    return ImageFont.truetype(FONT, size, index=idx)

img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

def rounded_box(xy, fill, outline=BORDER, width=2, radius=24):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def shadow_box(xy, radius=24, shadow=(0,0,0,28)):
    x1,y1,x2,y2 = xy
    layer = Image.new('RGBA', (W, H), (0,0,0,0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle((x1+8,y1+12,x2+8,y2+12), radius=radius, fill=shadow)
    layer = layer.filter(ImageFilter.GaussianBlur(18))
    return layer

# Title
 dfont = font(16)

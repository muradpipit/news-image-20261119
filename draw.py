#!/usr/bin/env python3
"""Draw the news-image-20261119 entry: a one-page newspaper front page
summing up Thursday 19 November 2026. Pure Python stdlib: own 5x7 bitmap
font, own raster canvas, own PNG encoder. Deterministic output."""

import zlib
import struct

W, H = 1024, 1024

# --- palette ---
PAPER = (246, 241, 227)
INK = (20, 33, 61)
NAVY = (20, 33, 61)
RED = (180, 35, 24)
TEAL = (14, 107, 107)
GOLD = (232, 184, 75)
WHITE = (255, 255, 255)
SAND = (214, 196, 150)
SEA = (46, 130, 150)
GREY = (90, 90, 84)

# --- 5x7 bitmap font: each glyph is 7 rows, one byte per row, bit 4 = left column ---
FONT = {
    'A': (0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    'B': (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    'C': (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E),
    'D': (0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E),
    'E': (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F),
    'F': (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10),
    'G': (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F),
    'H': (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    'I': (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    'J': (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C),
    'K': (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11),
    'L': (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F),
    'M': (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11),
    'N': (0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11),
    'O': (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    'P': (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    'Q': (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D),
    'R': (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11),
    'S': (0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E),
    'T': (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    'U': (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    'V': (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    'W': (0x11, 0x11, 0x11, 0x15, 0x15, 0x15, 0x0A),
    'X': (0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11),
    'Y': (0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04),
    'Z': (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F),
    '0': (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E),
    '1': (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E),
    '2': (0x0E, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1F),
    '3': (0x1E, 0x01, 0x01, 0x0E, 0x01, 0x01, 0x1E),
    '4': (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02),
    '5': (0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E),
    '6': (0x0E, 0x10, 0x10, 0x1E, 0x11, 0x11, 0x0E),
    '7': (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08),
    '8': (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E),
    '9': (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x01, 0x0E),
    'a': (0x00, 0x00, 0x0E, 0x01, 0x0F, 0x11, 0x0F),
    'b': (0x10, 0x10, 0x1E, 0x11, 0x11, 0x11, 0x1E),
    'c': (0x00, 0x00, 0x0E, 0x10, 0x10, 0x11, 0x0E),
    'd': (0x01, 0x01, 0x0F, 0x11, 0x11, 0x11, 0x0F),
    'e': (0x00, 0x00, 0x0E, 0x11, 0x1F, 0x10, 0x0E),
    'f': (0x06, 0x09, 0x08, 0x1E, 0x08, 0x08, 0x08),
    'g': (0x00, 0x0F, 0x11, 0x11, 0x0F, 0x01, 0x0E),
    'h': (0x10, 0x10, 0x1E, 0x11, 0x11, 0x11, 0x11),
    'i': (0x04, 0x00, 0x0C, 0x04, 0x04, 0x04, 0x0E),
    'j': (0x02, 0x00, 0x06, 0x02, 0x02, 0x12, 0x0C),
    'k': (0x10, 0x10, 0x12, 0x14, 0x18, 0x14, 0x12),
    'l': (0x0C, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    'm': (0x00, 0x00, 0x1A, 0x15, 0x15, 0x15, 0x15),
    'n': (0x00, 0x00, 0x1E, 0x11, 0x11, 0x11, 0x11),
    'o': (0x00, 0x00, 0x0E, 0x11, 0x11, 0x11, 0x0E),
    'p': (0x00, 0x00, 0x1E, 0x11, 0x11, 0x1E, 0x10),
    'q': (0x00, 0x00, 0x0F, 0x11, 0x11, 0x0F, 0x01),
    'r': (0x00, 0x00, 0x16, 0x19, 0x10, 0x10, 0x10),
    's': (0x00, 0x00, 0x0F, 0x10, 0x0E, 0x01, 0x1E),
    't': (0x08, 0x08, 0x1E, 0x08, 0x08, 0x08, 0x06),
    'u': (0x00, 0x00, 0x11, 0x11, 0x11, 0x13, 0x0D),
    'v': (0x00, 0x00, 0x11, 0x11, 0x11, 0x0A, 0x04),
    'w': (0x00, 0x00, 0x11, 0x15, 0x15, 0x15, 0x0A),
    'x': (0x00, 0x00, 0x11, 0x0A, 0x04, 0x0A, 0x11),
    'y': (0x00, 0x00, 0x11, 0x11, 0x0F, 0x01, 0x0E),
    'z': (0x00, 0x00, 0x1F, 0x02, 0x04, 0x08, 0x1F),
    ' ': (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    '.': (0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C),
    ',': (0x00, 0x00, 0x00, 0x00, 0x0C, 0x04, 0x08),
    ':': (0x00, 0x0C, 0x0C, 0x00, 0x0C, 0x0C, 0x00),
    ';': (0x00, 0x0C, 0x0C, 0x00, 0x0C, 0x04, 0x08),
    '!': (0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x04),
    '?': (0x0E, 0x11, 0x01, 0x02, 0x04, 0x00, 0x04),
    "'": (0x04, 0x04, 0x08, 0x00, 0x00, 0x00, 0x00),
    '"': (0x0A, 0x0A, 0x0A, 0x00, 0x00, 0x00, 0x00),
    '-': (0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00),
    '(': (0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02),
    ')': (0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08),
    '/': (0x01, 0x02, 0x02, 0x04, 0x08, 0x08, 0x10),
    '&': (0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D),
    '%': (0x19, 0x1A, 0x02, 0x04, 0x08, 0x0B, 0x13),
    '+': (0x00, 0x04, 0x04, 0x1F, 0x04, 0x04, 0x00),
    '=': (0x00, 0x00, 0x1F, 0x00, 0x1F, 0x00, 0x00),
    '*': (0x00, 0x15, 0x0E, 0x1F, 0x0E, 0x15, 0x00),
    '#': (0x0A, 0x0A, 0x1F, 0x0A, 0x1F, 0x0A, 0x0A),
    '@': (0x0E, 0x11, 0x17, 0x15, 0x16, 0x10, 0x0E),
    '$': (0x04, 0x0F, 0x14, 0x0E, 0x05, 0x1E, 0x04),
    '_': (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F),
    '\u00b7': (0x00, 0x00, 0x0C, 0x0C, 0x00, 0x00, 0x00),
}
BLANK = (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
NORM = {'\u2014': '-', '\u2013': '-', '\u2019': "'", '\u201c': '"', '\u201d': '"'}


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            base = (yy * self.w + x) * 3
            for xx in range(w):
                self.px[base + xx * 3: base + xx * 3 + 3] = bytes(c)

    def border(self, x, y, w, h, c, t=2):
        self.rect(x, y, w, t, c)
        self.rect(x, y + h - t, w, t, c)
        self.rect(x, y, t, h, c)
        self.rect(x + w - t, y, t, h, c)

    def hline(self, x, y, w, c, t=2):
        self.rect(x, y, w, t, c)

    def vline(self, x, y, h, c, t=2):
        self.rect(x, y, t, h, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            for a in range(t):
                for b in range(t):
                    self.set(x0 + a, y0 + b, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, c)

    def ring(self, cx, cy, r, c, t=2):
        for a in range(360):
            import math
            x = cx + int(r * math.cos(math.radians(a)))
            y = cy + int(r * math.sin(math.radians(a)))
            for dx in range(t):
                for dy in range(t):
                    self.set(x + dx, y + dy, c)

    def star(self, cx, cy, r, c):
        for ang in range(0, 360, 45):
            import math
            x = cx + int(r * math.cos(math.radians(ang)))
            y = cy + int(r * math.sin(math.radians(ang)))
            self.line(cx, cy, x, y, c, 2)
        self.disc(cx, cy, max(2, r // 4), c)

    def text(self, s, x, y, scale, c):
        s = ''.join(NORM.get(ch, ch) for ch in s)
        cx = x
        for ch in s:
            g = FONT.get(ch, BLANK)
            for row in range(7):
                bits = g[row]
                for col in range(5):
                    if bits & (0x10 >> col):
                        self.rect(cx + col * scale, y + row * scale, scale, scale, c)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale):
        return len(s) * 6 * scale - scale

    def text_center(self, s, cx, y, scale, c):
        w = self.text_w(s, scale)
        return self.text(s, cx - w // 2, y, scale, c)

    def wrap(self, s, x, y, w, scale, c, leading=None):
        if leading is None:
            leading = 9 * scale
        words = s.split(' ')
        lines, cur = [], ''
        for wd in words:
            trial = (cur + ' ' + wd).strip()
            if self.text_w(trial, scale) <= w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        for ln in lines:
            self.text(ln, x, y, scale, c)
            y += leading
        return y


def chunk(tag, data):
    out = struct.pack('>I', len(data)) + tag + data
    out += struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    return out


def write_png(cv, path):
    raw = bytearray()
    for yy in range(cv.h):
        raw.append(0)
        raw += cv.px[yy * cv.w * 3:(yy + 1) * cv.w * 3]
    ihdr = struct.pack('>IIBBBBB', cv.w, cv.h, 8, 2, 0, 0, 0)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', ihdr)
    png += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    png += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)
    return len(png)


def build():
    cv = Canvas(W, H, PAPER)
    # outer frame
    cv.border(12, 12, 1000, 1000, NAVY, 3)

    # ---- masthead ----
    cv.rect(28, 28, 968, 122, NAVY)
    cv.text_center("THE WORLD IN ONE DAY", 512, 48, 6, WHITE)
    cv.hline(120, 116, 784, GOLD, 2)
    cv.text_center("THURSDAY \u00b7 19 NOVEMBER 2026", 512, 126, 2, GOLD)

    # ---- hero: US-Iran ----
    cv.rect(28, 164, 968, 330, WHITE)
    cv.border(28, 164, 968, 330, NAVY, 2)
    cv.text("MIDDLE EAST \u00b7 WAR", 48, 182, 2, RED)
    cv.text("U.S. AND IRAN TRADE FIRE AS", 48, 208, 4, INK)
    cv.text("GULF CONFLICT SPREADS", 48, 244, 4, INK)
    cv.hline(48, 286, 560, RED, 3)
    body = ("Iran struck a U.S. base in Kuwait and hit Bahrain again, a day after "
            "U.S. forces hit a missile site on Qeshm Island. Ships in the Strait "
            "of Hormuz were attacked as Washington raised its carrier force in "
            "the region to three.")
    cv.wrap(body, 48, 300, 560, 2, INK)
    cv.text("STRAIT OF HORMUZ SHIPPING ATTACKED \u00b7 U.S. CARRIERS IN REGION: 3",
            48, 452, 2, RED)
    # stylised Gulf map, right side
    mx, my, mw, mh = 648, 196, 328, 240
    cv.rect(mx, my, mw, mh, SEA)
    cv.border(mx, my, mw, mh, NAVY, 2)
    cv.rect(mx, my, mw, 62, SAND)          # Iran, north shore
    cv.rect(mx, my + mh - 58, mw, 58, SAND)  # Arabia, south shore
    cv.text("IRAN", mx + 14, my + 22, 2, INK)
    cv.text("GULF", mx + 16, my + 72, 3, WHITE)
    cv.text("ARABIA", mx + 14, my + mh - 40, 2, INK)
    cv.star(mx + 120, my + 96, 16, RED)    # Qeshm
    cv.star(mx + 210, my + 132, 16, RED)   # Bahrain
    cv.star(mx + 262, my + 100, 14, RED)   # Kuwait
    cv.text("QESHM", mx + 92, my + 118, 2, WHITE)
    cv.text("BAHRAIN", mx + 196, my + 156, 2, WHITE)
    cv.text("KUWAIT", mx + 222, my + 72, 2, WHITE)
    # carrier triangle
    cv.line(mx + 232, my + 188, mx + 268, my + 188, WHITE, 2)
    cv.line(mx + 232, my + 188, mx + 250, my + 176, WHITE, 2)
    cv.line(mx + 268, my + 188, mx + 250, my + 176, WHITE, 2)
    cv.text("U.S. CARRIER", mx + 178, my + 204, 2, WHITE)

    # ---- middle row: GTA VI + APEC ----
    # left: GTA VI
    cv.rect(28, 514, 476, 228, WHITE)
    cv.border(28, 514, 476, 228, NAVY, 2)
    cv.text("CULTURE \u00b7 GAMES", 48, 532, 2, TEAL)
    cv.text("VICE CITY", 48, 556, 5, INK)
    cv.text("OPENS", 48, 596, 5, INK)
    cv.wrap("Grand Theft Auto VI begins its global rollout after a 13-year wait, "
            "the most anticipated game launch in years.", 48, 648, 300, 2, INK)
    # skyline + sun
    sx, sy = 372, 640
    cv.disc(sx + 56, sy + 12, 18, GOLD)
    for i, bh in enumerate((46, 70, 54, 84, 62)):
        cv.rect(sx + i * 24, sy + 92 - bh, 20, bh, NAVY)
    # right: APEC trilateral
    cv.rect(520, 514, 476, 228, WHITE)
    cv.border(520, 514, 476, 228, NAVY, 2)
    cv.text("DIPLOMACY \u00b7 APEC", 540, 532, 2, TEAL)
    cv.text("TRUMP, XI AND", 540, 556, 4, INK)
    cv.text("PUTIN MEET", 540, 592, 4, INK)
    cv.wrap("The three leaders hold trilateral talks in Shenzhen as Xi urges open "
            "trade at the APEC summit.", 540, 648, 300, 2, INK)
    # three flag bars
    fy = 700
    cv.rect(880, fy, 96, 10, RED)
    cv.rect(880, fy + 14, 96, 10, GOLD)
    cv.rect(880, fy + 28, 96, 10, TEAL)

    # ---- lower row: three small cards ----
    # Jeffries
    cv.rect(28, 762, 312, 168, WHITE)
    cv.border(28, 762, 312, 168, NAVY, 2)
    cv.text("WASHINGTON", 44, 778, 2, TEAL)
    cv.text("DEMOCRATS", 44, 800, 3, INK)
    cv.text("PICK JEFFRIES", 44, 824, 3, INK)
    cv.wrap("Poised to become the first Black Speaker of the U.S. House.",
            44, 852, 280, 2, INK)
    # Voyager 1
    cv.rect(356, 762, 312, 168, WHITE)
    cv.border(356, 762, 312, 168, NAVY, 2)
    cv.text("SPACE", 372, 778, 2, TEAL)
    cv.text("VOYAGER 1:", 372, 800, 3, INK)
    cv.text("ONE LIGHT-DAY", 372, 824, 3, INK)
    cv.wrap("NASA set to confirm the probe's record distance from Earth today.",
            372, 852, 280, 2, INK)
    cv.disc(628, 810, 9, GOLD)
    cv.ring(628, 810, 16, TEAL, 2)
    # EU loan + cyclone
    cv.rect(684, 762, 312, 168, WHITE)
    cv.border(684, 762, 312, 168, NAVY, 2)
    cv.text("EUROPE \u00b7 ASIA", 700, 778, 2, TEAL)
    cv.text("EU PLANS 45BN", 700, 800, 3, INK)
    cv.text("UKRAINE LOAN", 700, 824, 3, INK)
    cv.wrap("Brussels proposes a 45bn-euro loan for Kyiv. Cyclone Akvan nears "
            "India's coast.", 700, 852, 280, 2, INK)

    # ---- footer ----
    cv.hline(28, 946, 968, NAVY, 2)
    cv.text_center("OIL FALLS AS GULF TENSIONS RISE \u00b7 GOLD UNDER PRESSURE",
                   512, 958, 2, INK)
    cv.text_center("19 NOVEMBER 2026 \u2014 THE DAY IN ONE PAGE", 512, 980, 2, GREY)
    return cv


if __name__ == '__main__':
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else 'photo.jpg'
    cv = build()
    # PNG bytes in a .jpg-named file is fine: the entry is told apart by magic
    # bytes, and main.py copies it verbatim. Keep the .jpg name the brief uses.
    n = write_png(cv, out)
    print('wrote', out, n, 'bytes', cv.w, 'x', cv.h)

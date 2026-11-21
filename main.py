"""Draw a four-ink travel poster with no assets or external dependencies."""
import math
import os
from pathlib import Path
import struct
import zlib

WIDTH, HEIGHT = 800, 1000
PAPER, INK, SEA, SUN = range(4)
PALETTE = bytes.fromhex('F3E9CE 163D45 438D8B D46B3D')


def cubic(a, b, c, d, steps=24):
    points = []
    for i in range(steps + 1):
        t = i / steps
        s = 1 - t
        points.append(tuple(s**3 * p + 3 * s*s*t * q + 3 * s*t*t * r + t**3 * v
                            for p, q, r, v in zip(a, b, c, d)))
    return points


def oval(cx, cy, rx, ry, steps=112):
    return [(cx + rx * math.cos(math.tau * i / steps),
             cy + ry * math.sin(math.tau * i / steps)) for i in range(steps + 1)]


class Print:
    def __init__(self):
        self.pixels = bytearray(WIDTH * HEIGHT)

    def span(self, y, left, right, ink):
        x0 = max(0, math.ceil(left - 0.5))
        x1 = min(WIDTH, math.ceil(right - 0.5))
        if x1 > x0:
            start = y * WIDTH + x0
            self.pixels[start:y * WIDTH + x1] = bytes([ink]) * (x1 - x0)

    def fill(self, points, ink):
        rows = {}
        for (x0, y0), (x1, y1) in zip(points, points[1:] + points[:1]):
            if y0 == y1:
                continue
            for y in range(max(0, math.ceil(min(y0, y1) - 0.5)),
                           min(HEIGHT, math.ceil(max(y0, y1) - 0.5))):
                x = x0 + (y + 0.5 - y0) * (x1 - x0) / (y1 - y0)
                rows.setdefault(y, []).append(x)
        for y, cuts in rows.items():
            cuts.sort()
            for a, b in zip(cuts[::2], cuts[1::2]):
                self.span(y, a, b, ink)

    def stroke(self, points, width, ink):
        half = width / 2
        for (x, y), (u, v) in zip(points, points[1:]):
            length = math.hypot(u - x, v - y)
            if length:
                dx, dy = (v - y) * half / length, (x - u) * half / length
                self.fill([(x + dx, y + dy), (u + dx, v + dy),
                           (u - dx, v - dy), (x - dx, y - dy)], ink)
        for x, y in points[1:-1]:
            self.fill(oval(x, y, half, half, 12), ink)

    def box(self, x0, y0, x1, y1, ink):
        self.fill([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], ink)

    def save(self, path):
        def chunk(name, body):
            return (struct.pack('>I', len(body)) + name + body
                    + struct.pack('>I', zlib.crc32(name + body)))

        # Two bits per pixel suffice for the four-ink palette.
        p = self.pixels
        packed = bytes((a << 6) | (b << 4) | (c << 2) | d
                       for a, b, c, d in zip(p[::4], p[1::4], p[2::4], p[3::4]))
        row = WIDTH // 4
        scanlines = b''.join(b'\0' + packed[i:i + row] for i in range(0, len(packed), row))
        header = struct.pack('>IIBBBBB', WIDTH, HEIGHT, 2, 3, 0, 0, 0)
        path.write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', header)
                         + chunk(b'PLTE', PALETTE)
                         + chunk(b'IDAT', zlib.compress(scanlines, 9)) + chunk(b'IEND', b''))


# A geometric display alphabet. Coordinates describe stroke centerlines.
TOP_BOWL = cubic((.45, 0), (1.14, 0), (1.14, .48), (.45, .48))
GLYPHS = {
    'A': [[(0, 1), (.5, 0), (1, 1)], [(.19, .66), (.81, .66)]],
    'B': [[(0, 1), (0, 0)] + TOP_BOWL + [(0, .48)],
          [(0, .48), (.52, .48)] + cubic((.52, .48), (1.2, .48), (1.2, 1), (.52, 1)) + [(0, 1)]],
    'E': [[(1, 0), (0, 0), (0, 1), (1, 1)], [(0, .48), (.81, .48)]],
    'H': [[(0, 0), (0, 1)], [(1, 0), (1, 1)], [(0, .47), (1, .47)]],
    'I': [[(.5, 0), (.5, 1)]],
    'L': [[(0, 0), (0, 1), (1, 1)]],
    'N': [[(0, 1), (0, 0), (1, 1), (1, 0)]],
    'O': [oval(.5, .5, .5, .5, 72)],
    'R': [[(0, 1), (0, 0)] + TOP_BOWL + [(0, .48)], [(.42, .48), (1, 1)]],
    'S': [cubic((.96, .11), (.64, -.13), (-.05, -.02), (.05, .28))
          + cubic((.05, .28), (.15, .59), (1.05, .36), (.97, .76))
          + cubic((.97, .76), (.91, 1.06), (.33, 1.08), (0, .87))],
    'T': [[(0, 0), (1, 0)], [(.5, 0), (.5, 1)]],
}


def letterpress(poster, words, x, y, wide, high, weight, gap):
    start = x
    for letter in words:
        if letter == ' ':
            x += wide * .62 + gap
            continue
        width = wide * (.74 if letter in 'EL' else 1)
        if letter == 'I':
            width = 0
        for stroke in GLYPHS[letter]:
            poster.stroke([(x + width * u, y + high * v) for u, v in stroke], weight, INK)
        x += width + gap
    bounds = (start - weight / 2, y - weight, x - gap + weight, y + high + weight)
    assert bounds[0] >= 48 and bounds[2] <= 752 and bounds[1] >= 48 and bounds[3] < 325
    return bounds


def draw_poster():
    p = Print()
    title = [letterpress(p, 'HALO', 66, 70, 96, 77, 14, 25),
             letterpress(p, 'HARBOR', 66, 176, 91, 75, 14, 22),
             letterpress(p, 'THE INNER SEA', 66, 294, 13, 17, 2.6, 7)]
    assert all(a[3] < b[1] for a, b in zip(title, title[1:]))
    p.box(59, 330, 741, 332, INK)

    # Sunset and the perfectly level seam between sky and sea.
    p.fill(oval(659, 426, 54, 54), SUN)
    p.box(48, 610, 752, 894, SEA)
    p.box(48, 610, 752, 612, INK)

    # The front of the sea arch is a silhouette; a warm flank turns away from it.
    ring = []
    for i in range(161):
        a = math.pi + math.tau * i / 160
        r = 1 + .018 * math.sin(5 * a) + .012 * math.cos(9 * a)
        ring.append((384 + 227 * r * math.cos(a), 557 + 208 * r * math.sin(a)))
    p.fill(ring, INK)
    shoulder = cubic((411, 353), (540, 358), (604, 445), (609, 542))
    flank = cubic((609, 542), (618, 634), (574, 701), (522, 729))
    seam = cubic((522, 729), (520, 688), (559, 628), (554, 548))
    crest = cubic((554, 548), (557, 446), (504, 382), (411, 353))
    p.fill(shoulder + flank + seam + crest, SUN)
    for contour in [cubic((530, 405), (565, 451), (592, 490), (588, 564)),
                    cubic((558, 584), (557, 622), (554, 651), (531, 684)),
                    cubic((602, 542), (605, 591), (588, 634), (575, 655))]:
        p.stroke(contour, 2.5, INK)

    # Slice the same elliptical opening at the horizon to carry the sea through.
    for y in range(427, 684):
        u = (y + .5 - 555) / 128
        reach = 131 * math.sqrt(max(0, 1 - u * u))
        p.span(y, 379 - reach, 379 + reach, PAPER if y < 610 else SEA)

    # Sparse wave crests and a sail pin the scale of the arch to the harbor.
    for x, y, length in [(71, 648, 56), (650, 647, 70), (297, 641, 61),
                         (328, 662, 119), (80, 729, 78), (606, 732, 115),
                         (559, 762, 62), (219, 802, 159), (73, 854, 133),
                         (431, 839, 68)]:
        p.box(x, y, x + length, y + 2, PAPER)
    p.fill([(406, 624), (406, 578), (375, 624)], SUN)
    p.box(409, 579, 411, 629, INK)
    p.fill([(372, 629), (424, 629), (416, 636), (382, 636)], INK)

    # The promenade curves off the lower right, a human entry into the scene.
    shore = cubic((752, 742), (680, 777), (705, 842), (542, 894))
    p.fill(shore + [(752, 894)], SUN)
    path = cubic((737, 780), (692, 807), (702, 845), (606, 885))
    p.stroke(path, 4, PAPER)
    for x, y in path[2:-1:3]:
        p.stroke([(x - 5, y - 4), (x + 5, y + 4)], 2, INK)
    p.box(59, 932, 741, 934, INK)
    return p


def main():
    output = Path(os.environ.get('MAKEFUN_OUTPUT_DIR', '/output'))
    output.mkdir(parents=True, exist_ok=True)
    draw_poster().save(output / 'entry.png')


if __name__ == '__main__':
    main()

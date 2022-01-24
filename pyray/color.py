import colorsys

# An array of colors to be used when multi colored images need to be drawn.

colors = [
    (120, 80, 200),
    (200, 80, 100),
    (0, 255, 128),
    (0, 0, 255),
    (255, 153, 31),
    (51, 153, 255),
    (0, 255, 0),
    (255, 255, 255),
    (255, 255, 0),
    (255, 153, 153),
    (174, 87, 209),
    (100, 149, 237),
    (210, 105, 30),
    (176, 196, 202),
]


def colorFromAngle(angle):
    """
    Converts numbers into colors for shading effects.
    """
    return (int(230 * (angle / 450)), int(230 * (angle / 450)), 250)


def colorFromAngle2(angle, h=136, s=118, maxx=0.8):
    """
    Converts simple numbers into colors using HSL color scale. This can be used to shade surfaces more exposed to light brighter.
    args:
        angle: Higher values of this argument correspond to brighter colors. If a plane of a polyhedron makes a large angle with a light source,
                it will look brighter.
    """
    l = 96 + 64 * angle / maxx  # /450
    r, g, b = colorsys.hls_to_rgb(h / 255.0, l / 255.0, s / 255.0)
    r, g, b = [x * 255.0 for x in (r, g, b)]
    return (int(r), int(g), int(b))


def heat_rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value - minimum) / (maximum - minimum)
    b = int(max(0, 255 * (1 - ratio)))
    r = int(max(0, 255 * (ratio - 1)))
    g = 255 - b - r
    return (r, g, b)

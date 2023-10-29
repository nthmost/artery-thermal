import os

FONTMAP = {
        "megavibe9000": "zig.ttf",
}

def get_font_dir():
    os.path.join(os.getcwd(), "fonts")


def get_font_path(keyword):
    return os.path.join(get_font_dir(), FONTMAP[keyword])



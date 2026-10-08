"""Gera artes originais para o catálogo; execute uma vez se faltar a pasta assets."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent / "assets"
SCALE = 4
FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def font(size):
    for path in FONT_PATHS:
        if Path(path).exists():
            return ImageFont.truetype(path, size * SCALE)
    return ImageFont.load_default()


def gradient(size, start, end):
    width, height = size[0] * SCALE, size[1] * SCALE
    image = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(image)
    for y in range(height):
        t = y / max(1, height - 1)
        color = tuple(round(a * (1 - t) + b * t) for a, b in zip(start, end))
        draw.line((0, y, width, y), fill=color + (255,))
    return image


class SmoothDraw:
    """Aceita as coordenadas compactas e desenha tudo quatro vezes maior."""
    def __init__(self, image):
        self.draw = ImageDraw.Draw(image)

    def box(self, values):
        return tuple(round(value * SCALE) for value in values)

    def points(self, values):
        return [(round(x * SCALE), round(y * SCALE)) for x, y in values]

    def ellipse(self, box, fill=None, outline=None, width=1):
        self.draw.ellipse(self.box(box), fill=fill, outline=outline, width=width * SCALE)

    def rounded_rectangle(self, box, radius, fill=None, outline=None, width=1):
        self.draw.rounded_rectangle(self.box(box), radius=radius * SCALE,
                                    fill=fill, outline=outline, width=width * SCALE)

    def rectangle(self, box, fill=None, outline=None, width=1):
        self.draw.rectangle(self.box(box), fill=fill, outline=outline, width=width * SCALE)

    def polygon(self, points, fill=None, outline=None):
        scaled = self.points(points)
        self.draw.polygon(scaled, fill=fill, outline=outline)

    def line(self, values, fill=None, width=1):
        self.draw.line(self.box(values), fill=fill, width=width * SCALE, joint="curve")

    def arc(self, box, start, end, fill=None, width=1):
        self.draw.arc(self.box(box), start, end, fill=fill, width=width * SCALE)

    def pieslice(self, box, start, end, fill=None, outline=None, width=1):
        self.draw.pieslice(self.box(box), start, end, fill=fill,
                           outline=outline, width=width * SCALE)

    def text(self, position, text, font, fill):
        self.draw.text(self.box(position), text, font=font, fill=fill)


def save(image, category, name):
    folder = ROOT / category
    folder.mkdir(parents=True, exist_ok=True)
    image.save(folder / f"{name}.png")


def pet_image(kind):
    colors = {
        "tradicional": ((226, 243, 255), (172, 217, 255)),
        "gato": ((244, 224, 255), (215, 178, 255)),
        "cachorro": ((255, 240, 209), (250, 201, 132)),
        "coelho": ((255, 231, 243), (255, 183, 221)),
        "raposa": ((255, 231, 211), (255, 165, 114)),
        "panda": ((230, 239, 247), (191, 208, 224)),
    }
    image = gradient((150, 94), *colors[kind]); d = SmoothDraw(image)
    d.ellipse((26, 5, 124, 93), fill=(255, 255, 255), outline=(53, 81, 110), width=2)
    if kind in ("gato", "raposa"):
        ears = (239, 149, 90) if kind == "raposa" else (245, 231, 255)
        d.polygon([(39, 28), (39, 0), (61, 14)], fill=ears, outline=(53, 81, 110))
        d.polygon([(111, 28), (111, 0), (89, 14)], fill=ears, outline=(53, 81, 110))
    elif kind == "coelho":
        d.rounded_rectangle((49, 0, 65, 37), 8, fill=(255, 255, 255), outline=(53, 81, 110))
        d.rounded_rectangle((85, 0, 101, 37), 8, fill=(255, 255, 255), outline=(53, 81, 110))
    elif kind in ("panda", "cachorro"):
        ear = (40, 51, 64) if kind == "panda" else (168, 108, 76)
        d.ellipse((27, 11, 54, 46), fill=ear)
        d.ellipse((96, 11, 123, 46), fill=ear)
    if kind == "panda":
        d.ellipse((51, 36, 71, 56), fill=(43, 53, 63))
        d.ellipse((79, 36, 99, 56), fill=(43, 53, 63))
    d.ellipse((58, 42, 65, 50), fill=(29, 49, 73))
    d.ellipse((85, 42, 92, 50), fill=(29, 49, 73))
    d.arc((67, 48, 83, 66), 0, 180, fill=(48, 62, 83), width=2)
    d.ellipse((43, 55, 52, 61), fill=(255, 182, 192))
    d.ellipse((98, 55, 107, 61), fill=(255, 182, 192))
    return image


def accessory_image(kind):
    image = gradient((150, 94), (235, 245, 255), (195, 217, 255)); d = SmoothDraw(image)
    if kind == "nenhum":
        d.ellipse((52, 18, 98, 65), fill=(255, 255, 255), outline=(65, 111, 167), width=3)
        d.ellipse((64, 37, 69, 42), fill=(30, 48, 72)); d.ellipse((81, 37, 86, 42), fill=(30, 48, 72))
        d.arc((69, 43, 81, 53), 0, 180, fill=(30, 48, 72), width=2)
    elif kind == "oculos":
        for x in (39, 81):
            d.rounded_rectangle((x, 26, x + 31, 57), 9, fill=(246, 253, 255), outline=(28, 42, 61), width=5)
        d.line((70, 39, 81, 39), fill=(28, 42, 61), width=5)
    elif kind == "bone":
        d.pieslice((42, 15, 108, 76), 180, 360, fill=(31, 113, 226), outline=(19, 76, 158), width=3)
        d.rounded_rectangle((45, 48, 127, 60), 5, fill=(19, 76, 158))
    elif kind == "laco":
        d.polygon([(70, 42), (28, 15), (28, 69)], fill=(245, 86, 137), outline=(165, 48, 95))
        d.polygon([(80, 42), (122, 15), (122, 69)], fill=(245, 86, 137), outline=(165, 48, 95))
        d.ellipse((65, 31, 85, 53), fill=(211, 51, 109))
    elif kind == "coroa":
        d.polygon([(39, 62), (34, 17), (59, 43), (75, 9), (92, 43), (117, 17), (111, 62)],
                  fill=(255, 202, 53), outline=(171, 116, 22))
        d.ellipse((71, 46, 79, 54), fill=(255, 255, 255))
    return image


CARDS = {
    "gift_xbox": ("XBOX", (18, 99, 55), (11, 45, 31), "X"),
    "gift_psn": ("PLAYSTATION", (19, 61, 178), (9, 23, 87), "△"),
    "gift_centauro": ("CENTAURO", (230, 73, 43), (128, 28, 25), "C"),
    "gift_microsoft": ("MICROSOFT", (41, 78, 131), (17, 39, 75), "▦"),
    "gift_roblox": ("ROBLOX", (65, 72, 91), (21, 27, 45), "◇"),
    "brinde_fisico": ("BRINDE", (128, 76, 184), (65, 39, 116), "★"),
}


def reward_image(key):
    if key.startswith("pet_"):
        return pet_image(key[4:])
    if key.startswith("acc_"):
        return accessory_image(key[4:])
    title, start, end, symbol = CARDS[key]
    image = gradient((150, 94), start, end); d = SmoothDraw(image)
    d.rounded_rectangle((5, 5, 145, 89), 12, outline=(255, 255, 255, 115), width=2)
    d.ellipse((100, -38, 188, 50), outline=(255, 255, 255, 80), width=10)
    d.text((14, 14), "CARTÃO PRESENTE", font=font(8), fill=(244, 250, 255))
    d.text((13, 32), title, font=font(14 if len(title) < 10 else 11), fill=(255, 255, 255))
    d.text((14, 71), "CONCEITO VISUAL", font=font(7), fill=(225, 236, 246))
    d.text((110, 47), symbol, font=font(24), fill=(255, 255, 255))
    return image


def main():
    pets = ["tradicional", "gato", "cachorro", "coelho", "raposa", "panda"]
    accessories = ["nenhum", "oculos", "bone", "laco", "coroa"]
    for key in pets:
        save(pet_image(key), "pets", key)
    for key in accessories:
        save(accessory_image(key), "accessories", key)
    for key in ["acc_oculos", "acc_bone", "acc_laco", "acc_coroa", "pet_raposa", "pet_panda", *CARDS]:
        save(reward_image(key), "rewards", key)
    print("23 imagens PNG criadas em", ROOT)


if __name__ == "__main__":
    main()

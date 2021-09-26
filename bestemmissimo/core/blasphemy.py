from io import BytesIO
from random import randint
import requests
from PIL import Image, ImageFont, ImageDraw
from colorthief import ColorThief
from .utils import text_wrap


def _get_text_blasphemy() -> str:
    res = requests.get("https://bestemmiajouer.herokuapp.com/api/generate?len=1")
    return res.json()["text"]


def _get_tts(text: str):
    qs = {"text": text}
    res = requests.get(
        "https://bestemmiajouer.herokuapp.com/api/tts", params=qs, stream=True
    )
    return res.raw


def generate_graphic_blasphemy():
    res = requests.get(
        "https://3.bp.blogspot.com/-WEE8Wq0MW_Y/WyYXISuE4wI/AAAAAAAARIA/P7oa00q9VyYOVCCjccuDmYb0QQkzUCASwCLcBGAs/s400/Dolce%2BGes%25C3%25B9.jpg",
    )
    text = _get_text_blasphemy()
    img = Image.open(BytesIO(res.content))

    color_thief = ColorThief(BytesIO(res.content))
    dominant_color = color_thief.get_color(quality=1)
    opposite_color = (
        abs(dominant_color[0] - 255),
        abs(dominant_color[1] - 255),
        abs(dominant_color[2] - 255),
    )

    x_min = (img.size[0] * 8) // 100
    x_max = (img.size[0] * 50) // 100
    # Randomly select x-axis
    ran_x = randint(x_min, x_max)

    font = ImageFont.truetype("fonts/moonbright.ttf", 35)

    lines = text_wrap(text, font, img.size[0] - ran_x)
    line_height = font.getsize("hg")[1]

    y_min = (img.size[1] * 4) // 100  # 4% from the top
    y_max = (img.size[1] * 90) // 100  # 90% to the bottom
    y_max -= len(lines) * line_height  # Adjust
    ran_y = randint(y_min, y_max)  # Generate random point

    color = "rgb(255,255,255)"
    draw = ImageDraw.Draw(img)

    x = ran_x
    y = ran_y
    for line in lines:
        draw.text(
            (x, y),
            line,
            fill=opposite_color,
            font=font,
            stroke_fill=color,
            stroke_width=2,
        )

        y = y + line_height  # update y-axis for new line

    img_binary = BytesIO()
    img.save(img_binary, format="png")
    img_binary.seek(0)
    return img_binary


def generate_blasphemy() -> str:
    return _get_text_blasphemy()


def generate_audio_blasphemy():
    return _get_tts(_get_text_blasphemy())

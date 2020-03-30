from typing import List

from PIL import Image, ImageFont, ImageDraw


def get_pos(width: int, height: int, k: int):
    pos = [[[int(width / 2), int(2 * height / 30)]],
           [[int(width / 2), int(2 * height / 30)],
            [int(width / 2), int(20.5 * height / 25)]],
           [[int(width / 2), int(2 * height / 30)],
            [int(width / 4), int(20.5 * height / 25)],
            [int(3 * width / 4), int(20.5 * height / 25)]],
           [[int(width / 5), int(2 * height / 30)],
            [int(4 * width / 5), int(2 * height / 30)],
            [int(width / 5), int(20.5 * height / 25)],
            [int(4 * width / 5), int(20.5 * height / 25)]]]
    return pos[k - 1]


def label(raw_picture_file: str, samples: List[str], new_picture_file) -> None:
    img = Image.open(raw_picture_file)

    # Get size
    width, height = img.size
    text_positions = get_pos(width, height, len(samples))

    # Prepare text drawing
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("fonts/Inconsolata-Bold.ttf",
                              size=60)

    # Display each sample
    for i, sample in enumerate(samples):
        loc = text_positions[i]
        text = sample.replace(" ", "\n")
        # Get textsize to offset the text in the middle on the image
        w, _ = draw.multiline_textsize(text, font=font)
        draw.multiline_text((loc[0] - w / 2, loc[1]),
                            text,
                            font=font,
                            fill=(0, 0, 0, 255),
                            spacing=10,
                            align="center")

    img.save(new_picture_file)


if __name__ == '__main__':
    samples = ['Bone-in Pork Chops', 'Bread', 'Tart Crust']
    raw_picture_file = "data/tmp_raw.jpg"
    new_picture_file = "data/tmp_new.jpg"
    label(raw_picture_file, samples, new_picture_file)

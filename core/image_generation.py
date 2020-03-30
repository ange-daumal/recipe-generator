from typing import List

from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageChops


def get_pos(width: int, height: int, k: int):
    pos = [
        [[int(width / 2), int(2 * height / 30)]],

        [[int(width / 2), int(2 * height / 30)],
         [int(width / 2), int(2 * height / 3)]],

        [[int(width / 2), int(1 * height / 6)],
         [int(width / 4), int(3 * height / 4)],
         [int(3 * width / 4), int(3 * height / 4)]],

        [[int(width / 5), int(2 * height / 30)],
         [int(4 * width / 5), int(2 * height / 30)],
         [int(width / 5), int(2 * height / 3)],
         [int(4 * width / 5), int(2 * height / 3)]]

    ]
    return pos[k - 1]


def my_halo_filter() -> ImageFilter:
    kernel = [0, 1, 2, 1, 0,
              1, 2, 4, 2, 1,
              2, 4, 8, 4, 1,
              1, 2, 4, 2, 1,
              0, 1, 2, 1, 0]
    return ImageFilter.Kernel((5, 5), kernel, scale=0.2 * sum(kernel))


def draw_shadowed_text(img, position, text, font,
                       text_color=(255, 255, 255, 255),
                       halo_color=(0, 0, 0, 255)):
    # Create new blank image with text and blur it
    halo = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(halo).multiline_text(position,
                                        text,
                                        font=font,
                                        fill=halo_color,
                                        spacing=10,
                                        align="center")
    blurred = halo.filter(my_halo_filter())
    # Display non-blurred text on top of it
    ImageDraw.Draw(blurred).multiline_text(position,
                                           text,
                                           font=font,
                                           fill=text_color,
                                           spacing=10,
                                           align="center")
    # Add composition mask to original image
    img = Image.composite(img, blurred, ImageChops.invert(blurred))
    # Convert to RGB to remove the alpha channel
    return img.convert("RGB")


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
        new_loc = (loc[0] - w / 2, loc[1])
        img = draw_shadowed_text(img, new_loc, text, font)

    img.save(new_picture_file)


if __name__ == '__main__':
    samples = ['Bone-in Pork Chops', 'Bread', 'Tart Crust']
    raw_picture_file = "data/tmp_raw.jpg"
    new_picture_file = "data/tmp_new.jpg"
    label(raw_picture_file, samples, new_picture_file)

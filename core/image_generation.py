from typing import List

from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageChops

from utils.data_paths import reacts_fp, options_reacts_fp


def get_pos(width: int, height: int, k: int):
    pos = [
        [[int(width / 2), int(2 * height / 30)]],

        [[int(width / 2), int(2 * height / 30)],
         [int(width / 2), int(2 * height / 3)]],

        [[int(width / 2), int(1 * height / 25)],
         [int(width / 5), int(6 * height / 9)],
         [int(4 * width / 5), int(6 * height / 9)]],

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


def draw_centered_text(draw, img, position, text, font):
    w, _ = draw.multiline_textsize(text, font=font)
    new_loc = (position[0] - w / 2, position[1])
    img = draw_shadowed_text(img, new_loc, text, font)
    return img


def label(raw_picture_file: str, samples: List[str], new_picture_file) -> None:
    img = Image.open(raw_picture_file)

    # Get size
    width, height = img.size
    text_positions = get_pos(width, height, len(samples))

    # Prepare text drawing
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("fonts/Inconsolata-Bold.ttf", size=60)

    # Display each sample
    for i, sample in enumerate(samples):
        loc = text_positions[i]
        text = sample.replace(" ", "\n")
        # Get textsize to offset the text in the middle on the image
        img = draw_centered_text(draw, img, loc, text, font)

    img.save(new_picture_file)


def _draw_text(img, text, height_offset=0, size=60, loc=None):
    width, height = img.size
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("fonts/Inconsolata-Bold.ttf", size=size)

    if not loc:
        loc = [int(width / 2), int(2 * height / 30 + height_offset)]

    img = draw_centered_text(draw, img, loc, text, font)
    return img


def _crop_middle(img):
    width, height = img.size
    margin = width // 4
    # crop_rectangle is a 4-tuple (left, upper, right, lower)
    crop_rectangle = (margin, 0, width - margin, height)
    img = img.crop(crop_rectangle)
    return img


def _add_react_image(img, react_img, resize=(300, 300), where: str ='middle',
                     height_offset: int = 170, text: str = ""):
    width, height = img.size
    react_img = react_img.resize(resize)
    react_width, react_height = react_img.size

    width_offset = -react_width * 2.7

    if where == 'middle':
        loc = [int(width // 2 - react_width // 2),
               int(2 * height / 30 + height_offset)]
    elif where == 'bottom':
        text_loc = [int(width // 2 - react_width // 2 + 40),
                    int(7 * height // 9 + height_offset + 15)]
        loc = [int(width // 2 - react_width // 2 + width_offset),
               int(7 * height // 9 + height_offset)]
    else:
        raise Exception(f"Does not recognize value '{where}' for "
                        "`where` keyword argument")

    react_img = react_img.convert("RGBA")
    react_img_transparent = Image.new("RGBA", img.size)
    react_img_transparent.paste(react_img, loc, react_img.convert('RGBA'))

    output = Image.new("RGBA", img.size)
    output = Image.alpha_composite(output, img.convert('RGBA'))
    output = Image.alpha_composite(output, react_img_transparent)

    if text:
        output = _draw_text(output, text, size=40, loc=text_loc)


    return output


def _generate_versus_images(images_fp, samples_text):
    react_images = [Image.open(img) for img in reacts_fp]
    images = [Image.open(img) for img in images_fp]

    for i, text in zip(range(len(images)), samples_text):
        img = images[i]
        img = _add_react_image(img, react_images[i], where='middle')
        img = _draw_text(img, text, height_offset=120, size=45)
        img = _crop_middle(img)

        images[i] = img

    return images


def _join_images(images):
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)

    # Join images
    img_out = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for img in images:
        img_out.paste(img, (x_offset, 0))
        x_offset += img.size[0]

    return img_out


def versus_label(raw_picture_files: List[str], samples: List[str],
                 new_picture_file) -> None:
    options_reacts = [Image.open(img) for img in options_reacts_fp]
    options_texts = ["I don't know", "Neither of them"]
    options_offsets = [0, 80]

    images = _generate_versus_images(raw_picture_files, samples[1:])
    img_out = _join_images(images)
    img_out = _draw_text(img_out, samples[0], height_offset=-20)

    for react, text, offset in zip(options_reacts, options_texts, options_offsets):
        img_out = _add_react_image(img_out, react, resize=(70, 70),
                                   where='bottom', height_offset=offset,
                                   text=text)

    img_out = img_out.convert('RGB')
    img_out.save(new_picture_file)


if __name__ == '__main__':
    samples = ["What's tastier?\r\nChocolate with...", "coffee", "sugar"]

    # raw_picture_file = "data/tmp_raw.jpg"
    new_picture_file = "data/tmp/tmp_new.jpg"

    versus1_img = "data/versus1_raw.jpg"
    versus2_img = "data/versus2_raw.jpg"
    versus_label([versus1_img, versus2_img], samples, new_picture_file)

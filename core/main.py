import random

from core import image_generation, ingredients
from drivers import fb_driver, unsplash_driver

raw_picture_file = "data/tmp_raw.jpg"
new_picture_file = "data/tmp_new.jpg"

ingredients_list = ingredients.get_ingredients_list()

ordinal = lambda n: "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])


def get_sample(k=3):
    samples = random.sample(ingredients_list, k=k)
    return samples


def post_sample(k=3):
    samples = random.sample(ingredients_list, k=k)
    message = ""
    for i in range(k):
        message += f"{ordinal(i + 1)} ingredient: {samples[i]}\n"

    keywords = " ".join(samples)
    success, picture_text = unsplash_driver.get_picture_by_keywords(keywords, raw_picture_file)

    post_text = f"{message}\n{picture_text}"
    print(post_text)

    if success:
        image_generation.label(raw_picture_file, samples, new_picture_file)
        return fb_driver.post_picture(post_text, new_picture_file)
    else:
        return fb_driver.post_text(post_text)


if __name__ == '__main__':
    samples = get_sample(k=40)
    print(samples)

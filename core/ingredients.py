import json
import string
import random
from drivers import fb_driver, unsplash_driver
from core import image_generation

ingredients_file = "data/train.json"
raw_picture_file = "data/tmp_raw.jpg"
new_picture_file = "data/tmp_new.jpg"


def has_trademarks(ingredient):
    return "®" in ingredient \
           or "hellmann" in ingredient \
           or "sargento" in ingredient \
           or "soy Vay" in ingredient \
           or "bertolli" in ingredient \
           or "bacardi" in ingredient


ingredients = set()
with open(ingredients_file) as f:
    rid_list = json.load(f)

    for rid in rid_list:
        ingredients.update([string.capwords(ing) for ing in rid['ingredients'] if not has_trademarks(ing)])

ingredients_list = list(ingredients)

ordinal = lambda n: "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])


def get_sample(k=3):
    samples = random.sample(ingredients_list, k=k)
    return samples


def post_sample(k=3):
    samples = random.sample(ingredients_list, k=k)
    message = ""
    for i in range(k):
        message += f"{ordinal(i + 1)} ingredient: {samples[i]}\n"

    _, picture_text = unsplash_driver.get_picture_by_keywords(samples[0], raw_picture_file)

    image_generation.label(raw_picture_file, samples, new_picture_file)
    post_text = f"{message}\n{picture_text}"

    return fb_driver.post_picture(post_text, new_picture_file)


if __name__ == '__main__':
    samples = get_sample()
    print(samples)
    image_generation.label(raw_picture_file, samples, new_picture_file)

from drivers import fb_driver
from core import ingredients

if __name__ == '__main__':
    message = ingredients.get_sample()
    fb_driver.post_text(f"Hello! This is the first recipe idea we post here. "
                        f"Hope it will give you some inspiration...\n"
                        f"{message}")

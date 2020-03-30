import json
import random
import shutil
from typing import Tuple

import requests

from utils import io_ops

verbose = True

access_key = io_ops.get_env_var("unsplash_access_key")
secret_key = io_ops.get_env_var("unsplash_secret_key")
api = io_ops.get_env_var("unsplash_api")

headers = {
    "Authorization": f"Client-ID {access_key}"
}


def get_picture_by_keywords(keywords: str, image_filepath: str) -> Tuple[str, str]:
    response = requests.get(f"{api}/search/photos?query={keywords}", headers=headers)
    response = json.loads(response.text)

    # Get Picture data
    picture_data = random.choice(response["results"][:5])

    picture_url = picture_data["urls"]["regular"]
    author = picture_data["user"]["name"]
    portfolio_url = picture_data["user"]["portfolio_url"]
    alt_description = picture_data["alt_description"]

    text = f'Picture: "{alt_description.capitalize()}", by {author}.'
    if portfolio_url:
        text += f' Find his portofolio here: {portfolio_url}'
    print(text)

    # Download picture
    response = requests.get(picture_url, stream=True)
    response.raw.decode_content = True
    with open(image_filepath, 'wb') as f:
        shutil.copyfileobj(response.raw, f)

    return image_filepath, text


if __name__ == '__main__':
    keywords = "Chili Garlic Paste"
    print(get_picture_by_keywords(keywords))

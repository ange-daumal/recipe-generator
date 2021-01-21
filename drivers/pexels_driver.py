import json
import random
import shutil

import requests

from utils import io_ops

verbose = True

api_key = io_ops.get_env_var("pexels_api_key")
api = io_ops.get_env_var("pexels_api")

headers = {
    "Authorization": api_key
}


def get_picture_by_keywords(keywords: list, image_filepath: str,
                            per_page: int = 2):
    response = requests.get(f"{api}/search?query={' '.join(keywords)}"
                            f"&per_page={per_page}",
                            headers=headers)

    if response.status_code != 200:
        # FIXME: From print to Log.
        print(f"Pexels: {response.text}")
        return False, ""

    response = json.loads(response.text)

    picture_data = random.choice(response['photos'])
    picture_url = picture_data['src']['large2x']
    author = picture_data['photographer']
    portfolio_url = picture_data['photographer_url']

    text = f"from {author}"

    if portfolio_url:
        text += f'. Find more of their work here: {portfolio_url}'

    # Download picture
    response = requests.get(picture_url, stream=True)
    response.raw.decode_content = True
    with open(image_filepath, 'wb') as f:
        shutil.copyfileobj(response.raw, f)

    return True, text


if __name__ == '__main__':
    keywords = ['peaches']
    print(get_picture_by_keywords(keywords, "data/tmp/tmp.jpg"))

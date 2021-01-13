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


def get_picture_by_keywords(keywords: str, image_filepath: str,
                            per_page: int = 20, orientation: str = "squarish",
                            page: int = 1,
                            max_try: int = 5) -> Tuple[bool, str]:
    if page == max_try:
        return False, ""

    response = requests.get(f"{api}/search/photos?query={keywords}"
                            f"&per_page={per_page}"
                            f"&page={page}"
                            f"&orientation={orientation}",
                            # "&order_by=latest",
                            headers=headers)

    if response.status_code != 200:
        # FIXME: From print to Log.
        print(f"Unsplash: {response.text}")
        return False, ""

    response = json.loads(response.text)

    # Get Picture data
    containing_keywords = [x for x in response["results"] if x["alt_description"] and
                           any(y in x["alt_description"].lower().split(" ") for y in keywords.lower().split(" "))]
    if not containing_keywords:
        return get_picture_by_keywords(keywords, image_filepath,
                                       per_page=per_page,
                                       orientation=orientation,
                                       page=page + 1)

    picture_data = random.choice(containing_keywords)

    picture_url = picture_data["urls"]["regular"]
    author = picture_data["user"]["name"]
    portfolio_url = picture_data["user"]["portfolio_url"]
    alt_description = picture_data["alt_description"]

    text = f"from {author}"
    if alt_description:
        text += f', "{alt_description.capitalize()}"'

    if portfolio_url:
        text += f'. Find their portofolio here: {portfolio_url}'

    # Download picture
    response = requests.get(picture_url, stream=True)
    response.raw.decode_content = True
    with open(image_filepath, 'wb') as f:
        shutil.copyfileobj(response.raw, f)

    return True, text


if __name__ == '__main__':
    keywords = "coconut water frisee chopped green chilies"
    keywords = "Chili Garlic Paste"
    keywords = "tortellini, cook and drain margarita salt yellow mustard seeds"
    print(get_picture_by_keywords(keywords, "data/tmp.jpg"))

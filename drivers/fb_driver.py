import json
import sys

import facebook  # noqa
import requests

from utils import io_ops

verbose = True
user_id = io_ops.get_env_var("user_id")
user_access_token = io_ops.get_env_var("user_access_token")
page_id = io_ops.get_env_var("page_id")


def _get_page_access_token(response, page_id):
    for page in response["data"]:
        if page["id"] == page_id:
            return page["access_token"]


# Get Page Access Token

query = f"https://graph.facebook.com/{user_id}/accounts?access_token={user_access_token}"
response = json.loads(requests.get(query).text)
if "error" in response.keys():
    print(response['error'])
    sys.exit(1)

page_access_token = _get_page_access_token(response, page_id)

# Post as a Page

graph = facebook.GraphAPI(access_token=page_access_token)

# FIXME: This is hardcoded
album_id= 114196000226199

def post_text(message: str):
    response = graph.put_object(parent_object=page_id,
                                connection_name="feed",
                                message=message)
    post_id = response['id']
    if verbose:
        print("Success:", post_id)
    return post_id


def post_picture(message: str, filepath: str):
    response = graph.put_photo(image=open(filepath, 'rb'),
                               message=message,
                               album_path=f"{album_id}/photos")
    post_id = response['id']
    if verbose:
        print("Success:", post_id)
    return post_id

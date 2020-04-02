import json
import sys

import facebook
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


def check_error(response: dict) -> dict:
    if "error" in response.keys():
        print(response['error'])
        sys.exit(1)
    if verbose:
        print("Success:", response)
    return response


# Get Page Access Token

query = f"https://graph.facebook.com/{user_id}/accounts?access_token={user_access_token}"
response = json.loads(requests.get(query).text)
check_error(response)

page_access_token = _get_page_access_token(response, page_id)

# Post as a Page

graph = facebook.GraphAPI(access_token=page_access_token)


def post_text(message: str) -> str:
    query = f"https://graph.facebook.com/{page_id}/feed" \
        f"?message={message}" \
        f"&fields=created_time,from,id,message,permalink_url" \
        f"&published=false" \
        f"&access_token={page_access_token}"
    response = json.loads(requests.post(query).text)
    return check_error(response)


def post_picture(message: str, filepath: str) -> str:
    response = graph.put_photo(image=open(filepath, 'rb'),
                               message=message)
    return check_error(response)


if __name__ == '__main__':
    message = "Hello, this is a test."
    post_text(message)

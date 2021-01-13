import json
import sys

import facebook
import requests

from utils import io_ops


def _get_page_access_token(response, page_id):
    for page in response["data"]:
        if page["id"] == page_id:
            return page["access_token"]


def check_error(response: dict, verbose=False) -> dict:
    if "error" in response.keys():
        print(response['error'])
        sys.exit(1)
    if verbose:
        print("Success:", response)
    return response


# Get Page Access Token

def get_page_access_token(user_id, user_access_token):
    query = f"https://graph.facebook.com/{user_id}/accounts?access_token={user_access_token}"
    response = json.loads(requests.get(query).text)
    check_error(response)

    page_access_token = _get_page_access_token(response, page_id)
    return page_access_token


# Post as a Page

def post_text_http_request(page_id, page_access_token, message: str):
    query = f"https://graph.facebook.com/{page_id}/feed" \
        f"?message={message}" \
        f"&fields=created_time,from,id,message,permalink_url" \
        f"&published=false" \
        f"&access_token={page_access_token}"
    response = json.loads(requests.post(query).text)
    return check_error(response, verbose=True)


def post_text(page_access_token, message: str):
    graph = facebook.GraphAPI(access_token=page_access_token)
    response = graph.put_object(parent_object='me',
                                connection_name='feed',
                                message=message)

    return check_error(response, verbose=True)


def post_picture(page_access_token, message: str, filepath: str):
    graph = facebook.GraphAPI(access_token=page_access_token)
    response = graph.put_photo(image=open(filepath, 'rb'),
                               message=message)
    return check_error(response, verbose=True)


def get_post_reactions(page_access_token, post_id):
    query = f"https://graph.facebook.com/{post_id}/reactions" \
        f"?access_token={page_access_token}"

    response = json.loads(requests.get(query).text)
    return check_error(response, verbose=True)


if __name__ == '__main__':
    page_id = io_ops.get_env_var("page_id")
    page_access_token = io_ops.get_env_var("page_access_token")

    post_id = '113704106942055_238997857746012'
    print(get_post_reactions(page_access_token, post_id))

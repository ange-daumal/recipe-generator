import json
import sys

import facebook
import requests

from utils import io_ops


# Get Page Access Token

def _get_page_access_token(response, page_id):
    for page in response["data"]:
        if page["id"] == page_id:
            return page["access_token"]


def get_page_access_token(user_id, user_access_token, page_id):
    query = f"https://graph.facebook.com/{user_id}/accounts?access_token={user_access_token}"
    response = json.loads(requests.get(query).text)
    FbDriver.check_error(response)

    page_access_token = _get_page_access_token(response, page_id)
    return page_access_token


class FbDriver:

    def __init__(self, access_token=None):
        if not access_token:
            self.page_access_token = io_ops.get_env_var("page_access_token")
        else:
            self.page_access_token = access_token

    @staticmethod
    def check_error(response: dict, verbose=False) -> dict:
        if "error" in response.keys():
            print(response['error'])
            sys.exit(1)
        if verbose:
            print("Success:", response)
        return response

    def get_post_reactions(self, post_id):
        query = f"https://graph.facebook.com/{post_id}/reactions" \
            f"?access_token={self.page_access_token}"

        response = json.loads(requests.get(query).text)
        return self.check_error(response, verbose=True)

    def post_comment(self, post_id, comment):
        query = f"https://graph.facebook.com/{post_id}/comments" \
            f"?access_token={self.page_access_token}"
        payload = dict(message=comment)

        response = json.loads(requests.post(query, params=payload).text)
        return self.check_error(response, verbose=True)

    def post_text_http_request(self, page_id, message: str):
        query = f"https://graph.facebook.com/{page_id}/feed" \
            f"?message={message}" \
            f"&fields=created_time,from,id,message,permalink_url" \
            f"&published=false" \
            f"&access_token={self.page_access_token}"
        response = json.loads(requests.post(query).text)
        return self.check_error(response, verbose=True)

    def post_text(self, message: str):
        graph = facebook.GraphAPI(access_token=self.page_access_token)
        response = graph.put_object(parent_object='me',
                                    connection_name='feed',
                                    message=message)

        return self.check_error(response, verbose=True)

    def post_picture(self, message: str, filepath: str):
        graph = facebook.GraphAPI(access_token=f.selpage_access_token)
        response = graph.put_photo(image=open(filepath, 'rb'),
                                   message=message)
        return self.check_error(response, verbose=True)


if __name__ == '__main__':
    page_id = io_ops.get_env_var("page_id")
    fb = FbDriver()
    post_id = '113704106942055_238997857746012'
    #print(fb.get_post_reactions(post_id))
    x = fb.post_comment(post_id, "this is a test comment.")
    print(x)

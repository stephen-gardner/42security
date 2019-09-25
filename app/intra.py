from flask import current_app
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError

import json
import os
import requests


def get_session():
    token_url = current_app.config.get("INTRA_TOKEN_URL")
    client_id = current_app.config.get("INTRA_UID")
    client_secret = current_app.config.get("INTRA_SECRET")
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=token_url, client_id=client_id, client_secret=client_secret)
    return OAuth2Session(client_id, token=token)


def get_user(intra_id):
    session = get_session()
    try:
        response = session.get("https://api.intra.42.fr/v2/users/%s" % intra_id, timeout=30)
    except TokenExpiredError:
        return get_user(intra_id)
    if response.ok:
        return json.loads(response.content)
    return None


def get_user_info(intra_id, save_photo=False):
    user = get_user(intra_id)
    if user is None:
        return None

    photo_name = None
    if save_photo:
        img_url = user.get("image_url")
        if img_url is not None:
            response = requests.get(img_url, timeout=10)
            if response.ok:
                photo_name = img_url.rsplit('/', 1)[1]
                path = os.path.join(current_app.config.get("UPLOADED_PHOTOS_DEST"), photo_name)
                with open(path, "wb") as file:
                    file.write(response.content)

    return {
        "photo_name": photo_name,
        "first_name": user.get("first_name"),
        "last_name": user.get("last_name"),
    }

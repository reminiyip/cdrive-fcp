import requests
import os
from django.core.files.base import ContentFile

from .utils import PathUtils

def get_avatar(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        url = PathUtils.get_oauth_avatar_url(response['id'], provider='facebook')
    elif backend.name == 'github':
        url = response['avatar_url']

    if url:
        temp = ContentFile(requests.get(url).content)

        if temp.read() != user.profile.avatar_image.read():
            user.profile.avatar_image.save('{}.jpg'.format(user.username), temp)

import requests
import os
from django.core.files.base import ContentFile

def get_avatar(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large"%response['id']
    elif backend.name == 'github':
        url = response['avatar_url']
    else:
        return

    if url:
        temp = ContentFile(requests.get(url).content)

        if temp.read() != user.profile.avatar_image.read():
            user.profile.avatar_image.save('{}.jpg'.format(user.username), temp)

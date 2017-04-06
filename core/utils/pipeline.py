import requests
from django.core.files.base import ContentFile

from .const import OAuthConst

def get_api_url(provider):
    if provider == 'github':
        return "{}{}".format(OAuthConst.GITHUB_API_BASE_URL, OAuthConst.GITHUB_USER_PROFILE_PATH)

def get_profile_from_provider(backend, user, response, *args, **kwargs):
    if user.profile:
        # find api url
        if backend.name == 'facebook':
            social = user.social_auth.get(provider='facebook')

        elif backend.name == 'github':
            social = user.social_auth.get(provider='github')
            url = get_api_url('github')

        else:
            return

        # call api
        response = requests.get(
            url,
            params={'access_token': social.extra_data['access_token']}
        ).json()

        # get image
        avatar_url = response['avatar_url']
        if avatar_url:
            user.profile.avatar_image.save('{}.jpg'.format(user.username), ContentFile(requests.get(avatar_url).content))

        # save other profile information
        user.profile.on_screen_name = user.username
        user.profile.save()



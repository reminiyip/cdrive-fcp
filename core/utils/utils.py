from .const import OAuthConst, UserConst

class PathUtils():
    """Any helper functions related to file/directory paths or urls"""

    def get_avatar_file_name(instance, filename):
        return '{}/{}.jpg'.format(UserConst.AVATAR_IMAGE_PATH, instance.user.username)

    def get_oauth_avatar_url(user_id, provider, image_type='large'):
        if provider == 'facebook':
            return '{}/{}/picture?type={}'.format(OAuthConst.FB_API_BASE_URL, user_id, image_type)
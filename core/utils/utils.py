from .const import UserConst

def get_avatar_image_path(instance, filename):
    return '{}/{}/{}'.format(UserConst.AVATAR_IMAGE_PATH, instance.user.id, filename)
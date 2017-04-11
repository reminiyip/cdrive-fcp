from django.urls import reverse
from collections import OrderedDict
from decimal import Decimal

from .const import OAuthConst, UserConst, RewardsConst

class PathUtils():
    """Any helper functions related to file/directory paths or urls"""

    def get_avatar_file_name(instance, filename):
        return '{}/{}.jpg'.format(UserConst.AVATAR_IMAGE_PATH, instance.user.username)

    def get_oauth_avatar_url(user_id, provider, image_type='large'):
        if provider == 'facebook':
            return '{}/{}/picture?type={}'.format(OAuthConst.FB_API_BASE_URL, user_id, image_type)

class HelperUtils():
	"""Other commonly used help functions"""

	def get_column_groups(items, num_of_cols=2):
		return [items[i:i+num_of_cols] for i in range(0, len(items), num_of_cols)]

	def get_discount(price, rewards):
		return abs(price * int(rewards) * RewardsConst.REWARD_DISCOUNT)

	def get_subtotal(price, rewards):
		return abs(price - HelperUtils.get_discount(price, rewards))

	def get_discount_str(price, rewards, prec=2):
		return format(HelperUtils.get_discount(price, rewards), '.{}f'.format(prec))

	def get_subtotal_str(price, rewards, prec=2):
		return format(HelperUtils.get_subtotal(price, rewards), '.{}f'.format(prec))




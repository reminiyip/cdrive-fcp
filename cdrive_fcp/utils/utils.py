from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage
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
    """Other commonly used helper functions"""

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

class EmailUtils():
    """Email related helper functions"""

    def confirm_purchase(user, cart_id, rewards=None):
        from core.models import Cart

        subject = '[FCP] Purchase Confirmation'
        to = [user.email]
        from_email = 'fcp@example.com'

        ctx = {
            'user': user,
            'cart': Cart.objects.get(pk=cart_id),
            'new_rewards': rewards
        }

        message = get_template('email/confirm_purchase.html').render(Context(ctx))
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()




from decimal import Decimal

class RewardsConst():
	EXPIRE_THRESHOLD = 120 
	MAX_REWARDS = 10 
	REWARD_DISCOUNT = Decimal(0.1)

class UserConst():
	INITIAL_ACC_SPENDING = 11
	DEFAULT_ON_SCREEN_NAME = 'anonymous'
	AVATAR_IMAGE_PATH = 'avatars'
	DEFAULT_AVATAR_IMAGE_PATH = 'avatars/default-img.jpg'

class OAuthConst():
	FB_API_BASE_URL = 'http://graph.facebook.com'

class GameConst():
	NUM_OF_TARGETS_FOR_RECOMMENDATION = 3

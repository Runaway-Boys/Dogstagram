from enum import Enum

class FriendRequestStatus(Enum):
	"""
	different states the friend request 
	status could be
	"""
	NO_REQUEST_SENT = -1
	THEM_SENT_TO_YOU = 0
	YOU_SENT_TO_THEM = 1
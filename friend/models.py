from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class FriendList(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")

    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,related_name="friends")


    def __str__(self):
        return self.user.username
    
    def add_friend(self,account):
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()
    
    def remove_friend(self,account):
        if account in self.friend.all():
            self.friends.remove(account)

    def unfriended(self,removee):

        """
        removee is the person who gets unfriended
        """
        remover_friend_list = self # preson unfriending someone

        remover_friend_list.remove_friend(removee)

        friend_list =FriendList.objects.get(user=removee)
        friend_list.remove_friend(self.user)

    def is_mutual_friend(self,friend):
        if friend in self.friends.all():
            return True
        return False



class FriendRequest(models.Model):
	"""
	A friend request consists of two main parts:
		1. SENDER
			- Person sending/initiating the friend request
		2. RECIVER
			- Person receiving the friend friend
	"""

	sender 	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
      
	receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")

	is_active = models.BooleanField(blank=False, null=False, default=True)

	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.sender.username

	def accept(self):
		"""
		Accept a friend request.
		Update both SENDER and RECEIVER friend lists.
		"""
		receiver_friend_list = FriendList.objects.get(user=self.receiver)
		if receiver_friend_list:
			receiver_friend_list.add_friend(self.sender)
			sender_friend_list = FriendList.objects.get(user=self.sender)
			if sender_friend_list:
				sender_friend_list.add_friend(self.receiver)
				self.is_active = False
				self.save()

	def decline(self):
		"""
		Decline a friend request.
		Is it "declined" by setting the `is_active` field to False
		"""
		self.is_active = False
		self.save()


	def cancel(self):
		"""
		Cancel a friend request.
		Is it "cancelled" by setting the `is_active` field to False.
		This is only different with respect to "declining" through the notification that is generated.
		"""
		self.is_active = False
		self.save()
from forum.models.user import User as ForumUser
from django.contrib.auth.models import User as DjangoUser
from django.test import Client


USER_AUTHENTICATED='USER_AUTHENTICATED'
USER_EXISTS_BUT_WRONG_PASSWORD='USER_EXISTS_BUT_WRONG_PASSWORD'
USER_AUTHENTICATED_BUT_WRONG_MODEL='USER_AUTHENTICATED_BUT_WRONG_MODEL'
USER_EXISTS_BUT_WRONG_PASSWORD_AND_WRONG_MODEL='USER_EXISTS_BUT_WRONG_PASWORD_AND_WRONG_MODEL'
USER_DOES_NOT_EXIST='USER_DOES_NOT_EXIST'

def has_user(username, password):
	c = Client()
	can_login = c.login(username=username, password=password)
	try:
		ForumUser.objects.get(username=username)
		if can_login:
			return USER_AUTHENTICATED
		else:
			return USER_EXISTS_BUT_WRONG_PASSWORD
	except ForumUser.DoesNotExist:
		try:
			DjangoUser.objects.get(username=username)
			if can_login:
				return USER_AUTHENTICATED_BUT_WRONG_MODEL
			else:
				return USER_EXISTS_BUT_WRONG_PASSWORD_AND_WRONG_MODEL
		except DjangoUser.DoesNotExist:
			return USER_DOES_NOT_EXIST



def create_user(username, password):
	result = has_user(username, password)
	if result != USER_DOES_NOT_EXIST:
		return result
	user = ForumUser.objects.create(username=username)
	user.set_password(password)
	user.save()
	return user
from django.contrib.auth.models import User
from glue_osqa.tools import downcastUserToExtendedUser
from django.conf import settings

USING_EXTENDED_USER_MODEL = 'forum.middleware.extended_user.ExtendedUser' in settings.MIDDLEWARE_CLASSES
print 'Using extended user model: %s' % (USING_EXTENDED_USER_MODEL)

def create_test_user(username, email, password):
	user = User.objects.create_user(username, email, password)
	# Create the extended user counterpart, but do not return it!
	extended_user = downcastUserToExtendedUser(user)
	# Return an ordinary User.
	return user

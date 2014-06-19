from django.contrib.auth import get_user_model
DjangoUser = get_user_model()
from forum.models.user import User as ExtendedUser



# Given an existing, regular Django-style user, we may want to create an
# ExtendedUser for this user, so he will have a full OSQA profile.
# Otherwise, say, the ordinary Django root would not be able to 
# login into OSQA. Of course, one might also just go forward and create
# another superuser for OSQA, but overall it is nice to have this
# functionality available.
# Django, or Python for that matter, does not naturally allow to
# "downcast" a model, or any other class, so we are using a hack.
#
# Sample usage:
#
#
# https://code.djangoproject.com/ticket/7623
# http://stackoverflow.com/questions/4064808/django-model-inheritance-create-sub-instance-of-existing-instance-downcast
#
# For some reason, that method does not work here, neither with sqlite nor with PostGRESql, though it works with PostGRESql + a fresh OSQA installation. It should have to do with the other models that we have...
#
# Two workarounds: either save before __dict__.update, and then after, or
# set extended_user.id=None before save()
def downcastUserToExtendedUser(user):
    extended_user = ExtendedUser(user_ptr_id = user.pk)


    extended_user.save() # workaround; other option is to set extended_user.id=None before saving, as below
    extended_user.__dict__.update(user.__dict__)

#    extended_user.id=None # It seems that we need that. I don't understand, why. The resources linked above do not mention it, and with a standalone installation of OSQA, everything works OK without it. 

#    for field in user._meta.fields:
#        print field
#        if field.attname != 'id':
#            setattr(extended_user, field.attname, getattr(user, field.attname))
#        count -= 1
#        if count==0:
#            extended_user.save()
    extended_user.save()


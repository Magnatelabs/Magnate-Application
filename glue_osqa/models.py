from django.db import models

from zinnia.models.entry import Entry
from forum.models.node import Node
from forum.models import Action

#     Zinnia entries are linked with OSQA nodes, so we can have
#     e.g. questions ABOUT a particular post (Zinnia entry).
#     Ideally, perhaps, we should just remove Zinnia and use OSQA
#     nodes for everything in the first place, but so far that did not
#     happen for historical reasons. We started using Zinnia before OSQA,
#     and things just work...
#
#     Now, why are we doing adding it here, not as a ManyToMany relationship
#     defined for the Entry or for the Node, possibly with a 
#     setting through=EntryNodeAboutRelationship?
#     First of all, we want to change the code of OSQA (forum) as 
#     little as possible, and there is no natural way of modifying
#     forum.models.node.Node without it.
#     Secondly, remember that Zinnia entry is created using 
#     glue_zinnia.models.EntryCheck, an abstract entry. If we
#     add to it a ManyToMany relationship between zinnia.models.Entry
#     and forum.models.node.Node, this creates a circular reference.
#     In order to define zinnia.models.Entry we have to first import
#     glue_zinnia.models.EntryCheck, which then tries to resolve the
#     EntryNodeAboutRelationship, which refers to a complete 
#     zinnia.models.entry.Entry, which in turn again requires
#     glue_zinnia.models.EntryCheck.
#
#     Thus, we just create a separate model with two foreign keys,
#     and avoid using Django's ManyToMany feature alltogether.
#     This way we are still keeping Entry and Node as decoupled as possible,
#     yet we can write things like entry.about_nodes.all()[1].node or
#     node.about_entries.all()[2].entry. In effect, we still have a full
#     many-to-many relationship. 
class EntryNodeAboutRelationship(models.Model):
    entry = models.ForeignKey(Entry, related_name='about_nodes')
    node  = models.ForeignKey(Node, related_name='about_entries')


# Users can follow certain categories such as "Education". 
from django.contrib.auth.models import User
from forum.models.user import User as ForumUser
from zinnia.models import Category
class UserCategoryFollowing(models.Model):
	user = models.ForeignKey(ForumUser, related_name='following')
	category = models.ForeignKey(Category, related_name='users')

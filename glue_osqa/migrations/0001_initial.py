# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EntryNodeAboutRelationship'
        db.create_table(u'glue_osqa_entrynodeaboutrelationship', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(related_name='about_nodes', to=orm['zinnia.Entry'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='about_entries', to=orm['forum.Node'])),
        ))
        db.send_create_signal(u'glue_osqa', ['EntryNodeAboutRelationship'])

        # Adding model 'UserCategoryFollowing'
        db.create_table(u'glue_osqa_usercategoryfollowing', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='following', to=orm['auth.User'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='users', to=orm['zinnia.Category'])),
        ))
        db.send_create_signal(u'glue_osqa', ['UserCategoryFollowing'])


    def backwards(self, orm):
        # Deleting model 'EntryNodeAboutRelationship'
        db.delete_table(u'glue_osqa_entrynodeaboutrelationship')

        # Deleting model 'UserCategoryFollowing'
        db.delete_table(u'glue_osqa_usercategoryfollowing')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'forum.action': {
            'Meta': {'object_name': 'Action'},
            'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'canceled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'canceled_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'canceled_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'canceled_actions'", 'null': 'True', 'to': "orm['forum.User']"}),
            'canceled_ip': ('django.db.models.fields.CharField', [], {'max_length': '39'}),
            'extra': ('forum.models.utils.PickledObjectField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '39'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'null': 'True', 'to': "orm['forum.Node']"}),
            'real_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proxied_actions'", 'null': 'True', 'to': "orm['forum.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': "orm['forum.User']"})
        },
        'forum.markedtag': {
            'Meta': {'object_name': 'MarkedTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_selections'", 'to': "orm['forum.Tag']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tag_selections'", 'to': "orm['forum.User']"})
        },
        'forum.node': {
            'Meta': {'object_name': 'Node'},
            'abs_parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'all_children'", 'null': 'True', 'to': "orm['forum.Node']"}),
            'active_revision': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'active'", 'unique': 'True', 'null': 'True', 'to': "orm['forum.NodeRevision']"}),
            'added_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 26, 0, 0)'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': "orm['forum.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'extra': ('forum.models.utils.PickledObjectField', [], {'null': 'True'}),
            'extra_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'extra_ref': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Node']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_activity_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_activity_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.User']", 'null': 'True'}),
            'last_edited': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'edited_node'", 'unique': 'True', 'null': 'True', 'to': "orm['forum.Action']"}),
            'marked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'node_type': ('django.db.models.fields.CharField', [], {'default': "'node'", 'max_length': '16'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': "orm['forum.Node']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'state_string': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'tagnames': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'nodes'", 'symmetrical': 'False', 'to': "orm['forum.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'forum.noderevision': {
            'Meta': {'unique_together': "(('node', 'revision'),)", 'object_name': 'NodeRevision'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'noderevisions'", 'to': "orm['forum.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'to': "orm['forum.Node']"}),
            'revised_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 26, 0, 0)'}),
            'revision': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'tagnames': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'forum.questionsubscription': {
            'Meta': {'object_name': 'QuestionSubscription'},
            'auto_subscription': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_view': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 26, 0, 0)'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Node']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.User']"})
        },
        'forum.tag': {
            'Meta': {'ordering': "('-used_count', 'name')", 'object_name': 'Tag'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_tags'", 'to': "orm['forum.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marked_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'marked_tags'", 'symmetrical': 'False', 'through': "orm['forum.MarkedTag']", 'to': "orm['forum.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'used_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'forum.user': {
            'Meta': {'object_name': 'User', '_ormbases': [u'auth.User']},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'bronze': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email_isvalid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'real_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'reputation': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'silver': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'subscriptions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'subscribers'", 'symmetrical': 'False', 'through': "orm['forum.QuestionSubscription']", 'to': "orm['forum.Node']"}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'glue_osqa.entrynodeaboutrelationship': {
            'Meta': {'object_name': 'EntryNodeAboutRelationship'},
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'about_nodes'", 'to': "orm['zinnia.Entry']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'about_entries'", 'to': "orm['forum.Node']"})
        },
        u'glue_osqa.usercategoryfollowing': {
            'Meta': {'object_name': 'UserCategoryFollowing'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'users'", 'to': "orm['zinnia.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'following'", 'to': u"orm['auth.User']"})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'zinnia.category': {
            'Meta': {'ordering': "['title']", 'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['zinnia.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'zinnia.entry': {
            'Meta': {'ordering': "['-creation_date']", 'object_name': 'Entry', 'index_together': "[['slug', 'creation_date'], ['status', 'creation_date', 'start_publication', 'end_publication']]"},
            'authorized_users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'authorized_entries'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'entries'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'entries'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['zinnia.Category']"}),
            'comment_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comment_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_template': ('django.db.models.fields.CharField', [], {'default': "'zinnia/_entry_detail.html'", 'max_length': '250'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'detail_template': ('django.db.models.fields.CharField', [], {'default': "'entry_detail.html'", 'max_length': '250'}),
            'end_publication': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'excerpt': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'pingback_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pingback_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'related': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_rel_+'", 'null': 'True', 'to': "orm['zinnia.Entry']"}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'entries'", 'symmetrical': 'False', 'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'start_publication': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'trackback_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'trackback_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['glue_osqa']
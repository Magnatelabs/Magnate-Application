# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'KeyValue'
        db.create_table(u'forum_keyvalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('value', self.gf('forum.models.utils.PickledObjectField')(null=True)),
        ))
        db.send_create_signal('forum', ['KeyValue'])

        # Adding model 'User'
        db.create_table(u'forum_user', (
            (u'user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('is_approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email_isvalid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reputation', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('gold', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('silver', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('bronze', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('last_seen', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('real_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('about', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('forum', ['User'])

        # Adding model 'UserProperty'
        db.create_table(u'forum_userproperty', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='properties', to=orm['forum.User'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('value', self.gf('forum.models.utils.PickledObjectField')(null=True)),
        ))
        db.send_create_signal('forum', ['UserProperty'])

        # Adding unique constraint on 'UserProperty', fields ['user', 'key']
        db.create_unique(u'forum_userproperty', ['user_id', 'key'])

        # Adding model 'SubscriptionSettings'
        db.create_table(u'forum_subscriptionsettings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='subscription_settings', unique=True, to=orm['forum.User'])),
            ('enable_notifications', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('member_joins', self.gf('django.db.models.fields.CharField')(default='n', max_length=1)),
            ('new_question', self.gf('django.db.models.fields.CharField')(default='n', max_length=1)),
            ('new_question_watched_tags', self.gf('django.db.models.fields.CharField')(default='i', max_length=1)),
            ('subscribed_questions', self.gf('django.db.models.fields.CharField')(default='i', max_length=1)),
            ('all_questions', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('all_questions_watched_tags', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('questions_viewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notify_answers', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notify_reply_to_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notify_comments_own_post', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notify_comments', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notify_accepted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('send_digest', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('forum', ['SubscriptionSettings'])

        # Adding model 'ValidationHash'
        db.create_table(u'forum_validationhash', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hash_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('seed', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('expiration', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 16, 0, 0))),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.User'])),
        ))
        db.send_create_signal('forum', ['ValidationHash'])

        # Adding unique constraint on 'ValidationHash', fields ['user', 'type']
        db.create_unique(u'forum_validationhash', ['user_id', 'type'])

        # Adding model 'AuthKeyUserAssociation'
        db.create_table(u'forum_authkeyuserassociation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('provider', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='auth_keys', to=orm['forum.User'])),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('forum', ['AuthKeyUserAssociation'])

        # Adding model 'Tag'
        db.create_table(u'forum_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='created_tags', to=orm['forum.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('used_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('forum', ['Tag'])

        # Adding model 'MarkedTag'
        db.create_table(u'forum_markedtag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_selections', to=orm['forum.Tag'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tag_selections', to=orm['forum.User'])),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('forum', ['MarkedTag'])

        # Adding model 'Node'
        db.create_table(u'forum_node', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('tagnames', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nodes', to=orm['forum.User'])),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('node_type', self.gf('django.db.models.fields.CharField')(default='node', max_length=16)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', null=True, to=orm['forum.Node'])),
            ('abs_parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='all_children', null=True, to=orm['forum.Node'])),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('state_string', self.gf('django.db.models.fields.TextField')(default='')),
            ('last_edited', self.gf('django.db.models.fields.related.ForeignKey')(related_name='edited_node', unique=True, null=True, to=orm['forum.Action'])),
            ('last_activity_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.User'], null=True)),
            ('last_activity_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('active_revision', self.gf('django.db.models.fields.related.OneToOneField')(related_name='active', unique=True, null=True, to=orm['forum.NodeRevision'])),
            ('extra', self.gf('forum.models.utils.PickledObjectField')(null=True)),
            ('extra_ref', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.Node'], null=True)),
            ('extra_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('marked', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('forum', ['Node'])

        # Adding M2M table for field tags on 'Node'
        m2m_table_name = db.shorten_name(u'forum_node_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('node', models.ForeignKey(orm['forum.node'], null=False)),
            ('tag', models.ForeignKey(orm['forum.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['node_id', 'tag_id'])

        # Adding model 'NodeRevision'
        db.create_table(u'forum_noderevision', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('tagnames', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='noderevisions', to=orm['forum.User'])),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revisions', to=orm['forum.Node'])),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('revision', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('revised_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('forum', ['NodeRevision'])

        # Adding unique constraint on 'NodeRevision', fields ['node', 'revision']
        db.create_unique(u'forum_noderevision', ['node_id', 'revision'])

        # Adding model 'NodeState'
        db.create_table(u'forum_nodestate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='states', to=orm['forum.Node'])),
            ('state_type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('action', self.gf('django.db.models.fields.related.OneToOneField')(related_name='node_state', unique=True, to=orm['forum.Action'])),
        ))
        db.send_create_signal('forum', ['NodeState'])

        # Adding unique constraint on 'NodeState', fields ['node', 'state_type']
        db.create_unique(u'forum_nodestate', ['node_id', 'state_type'])

        # Adding model 'Action'
        db.create_table(u'forum_action', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actions', to=orm['forum.User'])),
            ('real_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='proxied_actions', null=True, to=orm['forum.User'])),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=39)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actions', null=True, to=orm['forum.Node'])),
            ('action_type', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('action_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('extra', self.gf('forum.models.utils.PickledObjectField')(null=True)),
            ('canceled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('canceled_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='canceled_actions', null=True, to=orm['forum.User'])),
            ('canceled_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('canceled_ip', self.gf('django.db.models.fields.CharField')(max_length=39)),
        ))
        db.send_create_signal('forum', ['Action'])

        # Adding model 'ActionRepute'
        db.create_table(u'forum_actionrepute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reputes', to=orm['forum.Action'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reputes', to=orm['forum.User'])),
            ('value', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('by_canceled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('forum', ['ActionRepute'])

        # Adding model 'QuestionSubscription'
        db.create_table(u'forum_questionsubscription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.User'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.Node'])),
            ('auto_subscription', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('last_view', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 15, 0, 0))),
        ))
        db.send_create_signal('forum', ['QuestionSubscription'])

        # Adding model 'Vote'
        db.create_table(u'forum_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['forum.User'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['forum.Node'])),
            ('value', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('action', self.gf('django.db.models.fields.related.OneToOneField')(related_name='vote', unique=True, to=orm['forum.Action'])),
            ('voted_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('forum', ['Vote'])

        # Adding unique constraint on 'Vote', fields ['user', 'node']
        db.create_unique(u'forum_vote', ['user_id', 'node_id'])

        # Adding model 'Flag'
        db.create_table(u'forum_flag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='flags', to=orm['forum.User'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='flags', to=orm['forum.Node'])),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('action', self.gf('django.db.models.fields.related.OneToOneField')(related_name='flag', unique=True, to=orm['forum.Action'])),
            ('flagged_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('forum', ['Flag'])

        # Adding unique constraint on 'Flag', fields ['user', 'node']
        db.create_unique(u'forum_flag', ['user_id', 'node_id'])

        # Adding model 'Badge'
        db.create_table(u'forum_badge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('cls', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('awarded_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('forum', ['Badge'])

        # Adding model 'Award'
        db.create_table(u'forum_award', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.User'])),
            ('badge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='awards', to=orm['forum.Badge'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.Node'], null=True)),
            ('awarded_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('trigger', self.gf('django.db.models.fields.related.ForeignKey')(related_name='awards', null=True, to=orm['forum.Action'])),
            ('action', self.gf('django.db.models.fields.related.OneToOneField')(related_name='award', unique=True, to=orm['forum.Action'])),
        ))
        db.send_create_signal('forum', ['Award'])

        # Adding unique constraint on 'Award', fields ['user', 'badge', 'node']
        db.create_unique(u'forum_award', ['user_id', 'badge_id', 'node_id'])

        # Adding model 'OpenIdNonce'
        db.create_table(u'forum_openidnonce', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('timestamp', self.gf('django.db.models.fields.IntegerField')()),
            ('salt', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('forum', ['OpenIdNonce'])

        # Adding model 'OpenIdAssociation'
        db.create_table(u'forum_openidassociation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server_url', self.gf('django.db.models.fields.TextField')(max_length=2047)),
            ('handle', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('secret', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('issued', self.gf('django.db.models.fields.IntegerField')()),
            ('lifetime', self.gf('django.db.models.fields.IntegerField')()),
            ('assoc_type', self.gf('django.db.models.fields.TextField')(max_length=64)),
        ))
        db.send_create_signal('forum', ['OpenIdAssociation'])


    def backwards(self, orm):
        # Removing unique constraint on 'Award', fields ['user', 'badge', 'node']
        db.delete_unique(u'forum_award', ['user_id', 'badge_id', 'node_id'])

        # Removing unique constraint on 'Flag', fields ['user', 'node']
        db.delete_unique(u'forum_flag', ['user_id', 'node_id'])

        # Removing unique constraint on 'Vote', fields ['user', 'node']
        db.delete_unique(u'forum_vote', ['user_id', 'node_id'])

        # Removing unique constraint on 'NodeState', fields ['node', 'state_type']
        db.delete_unique(u'forum_nodestate', ['node_id', 'state_type'])

        # Removing unique constraint on 'NodeRevision', fields ['node', 'revision']
        db.delete_unique(u'forum_noderevision', ['node_id', 'revision'])

        # Removing unique constraint on 'ValidationHash', fields ['user', 'type']
        db.delete_unique(u'forum_validationhash', ['user_id', 'type'])

        # Removing unique constraint on 'UserProperty', fields ['user', 'key']
        db.delete_unique(u'forum_userproperty', ['user_id', 'key'])

        # Deleting model 'KeyValue'
        db.delete_table(u'forum_keyvalue')

        # Deleting model 'User'
        db.delete_table(u'forum_user')

        # Deleting model 'UserProperty'
        db.delete_table(u'forum_userproperty')

        # Deleting model 'SubscriptionSettings'
        db.delete_table(u'forum_subscriptionsettings')

        # Deleting model 'ValidationHash'
        db.delete_table(u'forum_validationhash')

        # Deleting model 'AuthKeyUserAssociation'
        db.delete_table(u'forum_authkeyuserassociation')

        # Deleting model 'Tag'
        db.delete_table(u'forum_tag')

        # Deleting model 'MarkedTag'
        db.delete_table(u'forum_markedtag')

        # Deleting model 'Node'
        db.delete_table(u'forum_node')

        # Removing M2M table for field tags on 'Node'
        db.delete_table(db.shorten_name(u'forum_node_tags'))

        # Deleting model 'NodeRevision'
        db.delete_table(u'forum_noderevision')

        # Deleting model 'NodeState'
        db.delete_table(u'forum_nodestate')

        # Deleting model 'Action'
        db.delete_table(u'forum_action')

        # Deleting model 'ActionRepute'
        db.delete_table(u'forum_actionrepute')

        # Deleting model 'QuestionSubscription'
        db.delete_table(u'forum_questionsubscription')

        # Deleting model 'Vote'
        db.delete_table(u'forum_vote')

        # Deleting model 'Flag'
        db.delete_table(u'forum_flag')

        # Deleting model 'Badge'
        db.delete_table(u'forum_badge')

        # Deleting model 'Award'
        db.delete_table(u'forum_award')

        # Deleting model 'OpenIdNonce'
        db.delete_table(u'forum_openidnonce')

        # Deleting model 'OpenIdAssociation'
        db.delete_table(u'forum_openidassociation')


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
        'forum.actionrepute': {
            'Meta': {'object_name': 'ActionRepute'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reputes'", 'to': "orm['forum.Action']"}),
            'by_canceled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reputes'", 'to': "orm['forum.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'forum.authkeyuserassociation': {
            'Meta': {'object_name': 'AuthKeyUserAssociation'},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'auth_keys'", 'to': "orm['forum.User']"})
        },
        'forum.award': {
            'Meta': {'unique_together': "(('user', 'badge', 'node'),)", 'object_name': 'Award'},
            'action': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'award'", 'unique': 'True', 'to': "orm['forum.Action']"}),
            'awarded_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'awards'", 'to': "orm['forum.Badge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Node']", 'null': 'True'}),
            'trigger': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'awards'", 'null': 'True', 'to': "orm['forum.Action']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.User']"})
        },
        'forum.badge': {
            'Meta': {'object_name': 'Badge'},
            'awarded_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'awarded_to': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'badges'", 'symmetrical': 'False', 'through': "orm['forum.Award']", 'to': "orm['forum.User']"}),
            'cls': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'forum.flag': {
            'Meta': {'unique_together': "(('user', 'node'),)", 'object_name': 'Flag'},
            'action': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'flag'", 'unique': 'True', 'to': "orm['forum.Action']"}),
            'flagged_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flags'", 'to': "orm['forum.Node']"}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flags'", 'to': "orm['forum.User']"})
        },
        'forum.keyvalue': {
            'Meta': {'object_name': 'KeyValue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'value': ('forum.models.utils.PickledObjectField', [], {'null': 'True'})
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
            'added_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
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
            'revised_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'revision': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'tagnames': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'forum.nodestate': {
            'Meta': {'unique_together': "(('node', 'state_type'),)", 'object_name': 'NodeState'},
            'action': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'node_state'", 'unique': 'True', 'to': "orm['forum.Action']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'states'", 'to': "orm['forum.Node']"}),
            'state_type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'forum.openidassociation': {
            'Meta': {'object_name': 'OpenIdAssociation'},
            'assoc_type': ('django.db.models.fields.TextField', [], {'max_length': '64'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issued': ('django.db.models.fields.IntegerField', [], {}),
            'lifetime': ('django.db.models.fields.IntegerField', [], {}),
            'secret': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'server_url': ('django.db.models.fields.TextField', [], {'max_length': '2047'})
        },
        'forum.openidnonce': {
            'Meta': {'object_name': 'OpenIdNonce'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'server_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {})
        },
        'forum.questionsubscription': {
            'Meta': {'object_name': 'QuestionSubscription'},
            'auto_subscription': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_view': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 15, 0, 0)'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Node']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.User']"})
        },
        'forum.subscriptionsettings': {
            'Meta': {'object_name': 'SubscriptionSettings'},
            'all_questions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'all_questions_watched_tags': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enable_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member_joins': ('django.db.models.fields.CharField', [], {'default': "'n'", 'max_length': '1'}),
            'new_question': ('django.db.models.fields.CharField', [], {'default': "'n'", 'max_length': '1'}),
            'new_question_watched_tags': ('django.db.models.fields.CharField', [], {'default': "'i'", 'max_length': '1'}),
            'notify_accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notify_answers': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notify_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notify_comments_own_post': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notify_reply_to_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'questions_viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'send_digest': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'subscribed_questions': ('django.db.models.fields.CharField', [], {'default': "'i'", 'max_length': '1'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'subscription_settings'", 'unique': 'True', 'to': "orm['forum.User']"})
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
        'forum.userproperty': {
            'Meta': {'unique_together': "(('user', 'key'),)", 'object_name': 'UserProperty'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'properties'", 'to': "orm['forum.User']"}),
            'value': ('forum.models.utils.PickledObjectField', [], {'null': 'True'})
        },
        'forum.validationhash': {
            'Meta': {'unique_together': "(('user', 'type'),)", 'object_name': 'ValidationHash'},
            'expiration': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 16, 0, 0)'}),
            'hash_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seed': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.User']"})
        },
        'forum.vote': {
            'Meta': {'unique_together': "(('user', 'node'),)", 'object_name': 'Vote'},
            'action': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'vote'", 'unique': 'True', 'to': "orm['forum.Action']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': "orm['forum.Node']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': "orm['forum.User']"}),
            'value': ('django.db.models.fields.SmallIntegerField', [], {}),
            'voted_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        }
    }

    complete_apps = ['forum']
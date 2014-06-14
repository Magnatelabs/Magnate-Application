# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WaitingListEntry'
        db.create_table(u'waitinglist_waitinglistentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'waitinglist', ['WaitingListEntry'])

        # Adding model 'Survey'
        db.create_table(u'waitinglist_survey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'waitinglist', ['Survey'])

        # Adding model 'SurveyInstance'
        db.create_table(u'waitinglist_surveyinstance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='instances', to=orm['waitinglist.Survey'])),
            ('entry', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['waitinglist.WaitingListEntry'], unique=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'waitinglist', ['SurveyInstance'])

        # Adding model 'SurveyQuestion'
        db.create_table(u'waitinglist_surveyquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questions', to=orm['waitinglist.Survey'])),
            ('question', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('kind', self.gf('django.db.models.fields.IntegerField')()),
            ('help_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('ordinal', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'waitinglist', ['SurveyQuestion'])

        # Adding unique constraint on 'SurveyQuestion', fields ['survey']
        db.create_unique(u'waitinglist_surveyquestion', ['survey_id'])

        # Adding model 'SurveyQuestionChoice'
        db.create_table(u'waitinglist_surveyquestionchoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='choices', to=orm['waitinglist.SurveyQuestion'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'waitinglist', ['SurveyQuestionChoice'])

        # Adding model 'SurveyAnswer'
        db.create_table(u'waitinglist_surveyanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['waitinglist.SurveyInstance'])),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('value', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('value_boolean', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'waitinglist', ['SurveyAnswer'])

        # Adding model 'Cohort'
        db.create_table(u'waitinglist_cohort', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'waitinglist', ['Cohort'])

        # Adding model 'SignupCodeCohort'
        db.create_table(u'waitinglist_signupcodecohort', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('signup_code', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['account.SignupCode'], unique=True)),
            ('cohort', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['waitinglist.Cohort'])),
        ))
        db.send_create_signal(u'waitinglist', ['SignupCodeCohort'])

        # Adding model 'UserCohort'
        db.create_table(u'waitinglist_usercohort', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('cohort', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['waitinglist.Cohort'])),
        ))
        db.send_create_signal(u'waitinglist', ['UserCohort'])


    def backwards(self, orm):
        # Removing unique constraint on 'SurveyQuestion', fields ['survey']
        db.delete_unique(u'waitinglist_surveyquestion', ['survey_id'])

        # Deleting model 'WaitingListEntry'
        db.delete_table(u'waitinglist_waitinglistentry')

        # Deleting model 'Survey'
        db.delete_table(u'waitinglist_survey')

        # Deleting model 'SurveyInstance'
        db.delete_table(u'waitinglist_surveyinstance')

        # Deleting model 'SurveyQuestion'
        db.delete_table(u'waitinglist_surveyquestion')

        # Deleting model 'SurveyQuestionChoice'
        db.delete_table(u'waitinglist_surveyquestionchoice')

        # Deleting model 'SurveyAnswer'
        db.delete_table(u'waitinglist_surveyanswer')

        # Deleting model 'Cohort'
        db.delete_table(u'waitinglist_cohort')

        # Deleting model 'SignupCodeCohort'
        db.delete_table(u'waitinglist_signupcodecohort')

        # Deleting model 'UserCohort'
        db.delete_table(u'waitinglist_usercohort')


    models = {
        u'account.signupcode': {
            'Meta': {'object_name': 'SignupCode'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'expiry': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inviter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'max_uses': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'use_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'waitinglist.cohort': {
            'Meta': {'object_name': 'Cohort'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '35'})
        },
        u'waitinglist.signupcodecohort': {
            'Meta': {'object_name': 'SignupCodeCohort'},
            'cohort': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['waitinglist.Cohort']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'signup_code': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['account.SignupCode']", 'unique': 'True'})
        },
        u'waitinglist.survey': {
            'Meta': {'object_name': 'Survey'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'waitinglist.surveyanswer': {
            'Meta': {'object_name': 'SurveyAnswer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['waitinglist.SurveyInstance']"}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'value_boolean': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        u'waitinglist.surveyinstance': {
            'Meta': {'object_name': 'SurveyInstance'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'entry': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['waitinglist.WaitingListEntry']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': u"orm['waitinglist.Survey']"})
        },
        u'waitinglist.surveyquestion': {
            'Meta': {'ordering': "['ordinal']", 'unique_together': "(['survey'],)", 'object_name': 'SurveyQuestion'},
            'help_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.IntegerField', [], {}),
            'ordinal': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': u"orm['waitinglist.Survey']"})
        },
        u'waitinglist.surveyquestionchoice': {
            'Meta': {'object_name': 'SurveyQuestionChoice'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'choices'", 'to': u"orm['waitinglist.SurveyQuestion']"})
        },
        u'waitinglist.usercohort': {
            'Meta': {'object_name': 'UserCohort'},
            'cohort': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['waitinglist.Cohort']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'waitinglist.waitinglistentry': {
            'Meta': {'object_name': 'WaitingListEntry'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['waitinglist']
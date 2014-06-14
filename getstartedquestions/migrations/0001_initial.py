# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'QuestionList'
        db.create_table(u'getstartedquestions_questionlist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('waitinglistemail', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('dob', self.gf('django.db.models.fields.DateField')()),
            ('funding_knowledge', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('income', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('funding_preference', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('industry_preference', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('site_rec', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'getstartedquestions', ['QuestionList'])


    def backwards(self, orm):
        # Deleting model 'QuestionList'
        db.delete_table(u'getstartedquestions_questionlist')


    models = {
        u'getstartedquestions.questionlist': {
            'Meta': {'object_name': 'QuestionList'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'funding_knowledge': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'funding_preference': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'income': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'industry_preference': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'site_rec': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'waitinglistemail': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        }
    }

    complete_apps = ['getstartedquestions']
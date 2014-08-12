# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'QuestionList.dob'
        db.alter_column(u'getstartedquestions_questionlist', 'dob', self.gf('django.db.models.fields.DateField')(null=True))

    def backwards(self, orm):

        # Changing field 'QuestionList.dob'
        db.alter_column(u'getstartedquestions_questionlist', 'dob', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 8, 12, 0, 0)))

    models = {
        u'getstartedquestions.questionlist': {
            'Meta': {'object_name': 'QuestionList'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
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
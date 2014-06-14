# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MediaUpdates'
        db.create_table(u'companyinfo_mediaupdates', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('signup_email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'companyinfo', ['MediaUpdates'])


    def backwards(self, orm):
        # Deleting model 'MediaUpdates'
        db.delete_table(u'companyinfo_mediaupdates')


    models = {
        u'companyinfo.mediaupdates': {
            'Meta': {'object_name': 'MediaUpdates'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'signup_email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'})
        }
    }

    complete_apps = ['companyinfo']
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PlatformStatistics'
        db.create_table(u'statistics_platformstatistics', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stat_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'statistics', ['PlatformStatistics'])


    def backwards(self, orm):
        # Deleting model 'PlatformStatistics'
        db.delete_table(u'statistics_platformstatistics')


    models = {
        u'statistics.platformstatistics': {
            'Meta': {'object_name': 'PlatformStatistics'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stat_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['statistics']
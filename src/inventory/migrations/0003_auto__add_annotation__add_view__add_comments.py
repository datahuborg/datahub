# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Annotation'
        db.create_table('annotations', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('url_path', self.gf('django.db.models.fields.CharField')(unique=True, max_length=500)),
            ('url_blurb', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('inventory', ['Annotation'])

        # Adding model 'View'
        db.create_table('views', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('url_path', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('repo_base', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('repo_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('view_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('inventory', ['View'])

        # Adding model 'Comments'
        db.create_table('comments', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('url_path', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('inventory', ['Comments'])


    def backwards(self, orm):
        # Deleting model 'Annotation'
        db.delete_table('annotations')

        # Deleting model 'View'
        db.delete_table('views')

        # Deleting model 'Comments'
        db.delete_table('comments')


    models = {
        'inventory.annotation': {
            'Meta': {'object_name': 'Annotation', 'db_table': "'annotations'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url_blurb': ('django.db.models.fields.TextField', [], {}),
            'url_path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500'})
        },
        'inventory.app': {
            'Meta': {'object_name': 'App', 'db_table': "'apps'"},
            'app_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'app_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'app_token': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.User']"})
        },
        'inventory.comments': {
            'Meta': {'object_name': 'Comments', 'db_table': "'comments'"},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url_path': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'inventory.permission': {
            'Meta': {'object_name': 'Permission', 'db_table': "'permissions'"},
            'access': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.App']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.User']"})
        },
        'inventory.user': {
            'Meta': {'object_name': 'User', 'db_table': "'users'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'f_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'inventory.view': {
            'Meta': {'object_name': 'View', 'db_table': "'views'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repo_base': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'repo_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url_path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'view_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['inventory']
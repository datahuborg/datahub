# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Card.url_path'
        db.delete_column('cards', 'url_path')

        # Adding field 'Card.query'
        db.add_column('cards', 'query',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Card.url_path'
        raise RuntimeError("Cannot reverse this migration. 'Card.url_path' and its values cannot be restored.")
        # Deleting field 'Card.query'
        db.delete_column('cards', 'query')


    models = {
        'inventory.annotation': {
            'Meta': {'object_name': 'Annotation', 'db_table': "'annotations'"},
            'annotation_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
        'inventory.card': {
            'Meta': {'object_name': 'Card', 'db_table': "'cards'"},
            'card_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'query': ('django.db.models.fields.TextField', [], {}),
            'repo_base': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'repo_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'inventory.comments': {
            'Meta': {'object_name': 'Comments', 'db_table': "'comments'"},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url_path': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'inventory.dashboard': {
            'Meta': {'object_name': 'Dashboard', 'db_table': "'dashboards'"},
            'dashboard_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repo_base': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'repo_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url_path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'inventory.dashboardcard': {
            'Meta': {'object_name': 'DashboardCard', 'db_table': "'dashboard_cards'"},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Card']"}),
            'dashboard': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Dashboard']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
        }
    }

    complete_apps = ['inventory']
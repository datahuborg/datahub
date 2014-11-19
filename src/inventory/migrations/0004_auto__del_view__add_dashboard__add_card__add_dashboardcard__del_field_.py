# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'View'
        db.delete_table('views')

        # Adding model 'Dashboard'
        db.create_table('dashboards', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('url_path', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('repo_base', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('repo_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('dashboard_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('inventory', ['Dashboard'])

        # Adding model 'Card'
        db.create_table('cards', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('url_path', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('repo_base', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('repo_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('card_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('inventory', ['Card'])

        # Adding model 'DashboardCard'
        db.create_table('dashboard_cards', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Card'])),
            ('dashboard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Dashboard'])),
        ))
        db.send_create_signal('inventory', ['DashboardCard'])

        # Deleting field 'Annotation.url_blurb'
        db.delete_column('annotations', 'url_blurb')

        # Adding field 'Annotation.annotation_text'
        db.add_column('annotations', 'annotation_text',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'View'
        db.create_table('views', (
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('view_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('repo_base', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('url_path', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('repo_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('inventory', ['View'])

        # Deleting model 'Dashboard'
        db.delete_table('dashboards')

        # Deleting model 'Card'
        db.delete_table('cards')

        # Deleting model 'DashboardCard'
        db.delete_table('dashboard_cards')


        # User chose to not deal with backwards NULL issues for 'Annotation.url_blurb'
        raise RuntimeError("Cannot reverse this migration. 'Annotation.url_blurb' and its values cannot be restored.")
        # Deleting field 'Annotation.annotation_text'
        db.delete_column('annotations', 'annotation_text')


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
            'repo_base': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'repo_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url_path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
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
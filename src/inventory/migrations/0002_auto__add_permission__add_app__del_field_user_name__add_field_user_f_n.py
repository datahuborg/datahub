# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Permission'
        db.create_table('permissions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.User'])),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.App'])),
            ('access', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('inventory', ['Permission'])

        # Adding model 'App'
        db.create_table('apps', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('app_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('app_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('app_token', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.User'])),
        ))
        db.send_create_signal('inventory', ['App'])

        # Deleting field 'User.name'
        db.delete_column('users', 'name')

        # Adding field 'User.f_name'
        db.add_column('users', 'f_name',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
                      keep_default=False)

        # Adding field 'User.l_name'
        db.add_column('users', 'l_name',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Permission'
        db.delete_table('permissions')

        # Deleting model 'App'
        db.delete_table('apps')


        # User chose to not deal with backwards NULL issues for 'User.name'
        raise RuntimeError("Cannot reverse this migration. 'User.name' and its values cannot be restored.")
        # Deleting field 'User.f_name'
        db.delete_column('users', 'f_name')

        # Deleting field 'User.l_name'
        db.delete_column('users', 'l_name')


    models = {
        'inventory.app': {
            'Meta': {'object_name': 'App', 'db_table': "'apps'"},
            'app_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'app_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'app_token': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.User']"})
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
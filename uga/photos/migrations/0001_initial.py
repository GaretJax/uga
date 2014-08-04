# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Album'
        db.create_table('photos_album', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gdata_id', self.gf('django.db.models.fields.CharField')(max_length=31)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('photos', ['Album'])

        # Adding model 'Photo'
        db.create_table('photos_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photos.Album'])),
            ('gdata_id', self.gf('django.db.models.fields.CharField')(max_length=31)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('photos', ['Photo'])


    def backwards(self, orm):
        # Deleting model 'Album'
        db.delete_table('photos_album')

        # Deleting model 'Photo'
        db.delete_table('photos_photo')


    models = {
        'photos.album': {
            'Meta': {'object_name': 'Album'},
            'gdata_id': ('django.db.models.fields.CharField', [], {'max_length': '31'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'photos.photo': {
            'Meta': {'object_name': 'Photo'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['photos.Album']"}),
            'gdata_id': ('django.db.models.fields.CharField', [], {'max_length': '31'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['photos']
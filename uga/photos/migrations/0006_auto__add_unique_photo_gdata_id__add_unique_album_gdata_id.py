# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Photo', fields ['gdata_id']
        db.create_unique('photos_photo', ['gdata_id'])

        # Adding unique constraint on 'Album', fields ['gdata_id']
        db.create_unique('photos_album', ['gdata_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Album', fields ['gdata_id']
        db.delete_unique('photos_album', ['gdata_id'])

        # Removing unique constraint on 'Photo', fields ['gdata_id']
        db.delete_unique('photos_photo', ['gdata_id'])


    models = {
        'photos.album': {
            'Meta': {'ordering': "('-published',)", 'object_name': 'Album'},
            'gdata_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '31'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        'photos.photo': {
            'Meta': {'ordering': "('published',)", 'object_name': 'Photo'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'to': "orm['photos.Album']"}),
            'gdata_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '31'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['photos']
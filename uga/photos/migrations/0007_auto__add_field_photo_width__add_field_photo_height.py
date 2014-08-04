# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Photo.width'
        db.add_column('photos_photo', 'width',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Photo.height'
        db.add_column('photos_photo', 'height',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Photo.width'
        db.delete_column('photos_photo', 'width')

        # Deleting field 'Photo.height'
        db.delete_column('photos_photo', 'height')


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
            'height': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['photos']
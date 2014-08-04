# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'Album.thumbnail' to match new field type.
        db.rename_column('photos_album', 'thumbnail_id', 'thumbnail')
        # Changing field 'Album.thumbnail'
        db.alter_column('photos_album', 'thumbnail', self.gf('django.db.models.fields.URLField')(default='http://example.com', max_length=200))
        # Removing index on 'Album', fields ['thumbnail']
        db.delete_index('photos_album', ['thumbnail_id'])


    def backwards(self, orm):
        # Adding index on 'Album', fields ['thumbnail']
        db.create_index('photos_album', ['thumbnail_id'])


        # Renaming column for 'Album.thumbnail' to match new field type.
        db.rename_column('photos_album', 'thumbnail', 'thumbnail_id')
        # Changing field 'Album.thumbnail'
        db.alter_column('photos_album', 'thumbnail_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['photos.Photo']))

    models = {
        'photos.album': {
            'Meta': {'object_name': 'Album'},
            'gdata_id': ('django.db.models.fields.CharField', [], {'max_length': '31'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        'photos.photo': {
            'Meta': {'object_name': 'Photo'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'to': "orm['photos.Album']"}),
            'gdata_id': ('django.db.models.fields.CharField', [], {'max_length': '31'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['photos']
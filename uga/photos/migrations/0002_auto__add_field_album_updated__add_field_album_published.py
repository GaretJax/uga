# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Album.updated'
        db.add_column('photos_album', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 8, 18, 0, 0)),
                      keep_default=False)

        # Adding field 'Album.published'
        db.add_column('photos_album', 'published',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 8, 18, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Album.updated'
        db.delete_column('photos_album', 'updated')

        # Deleting field 'Album.published'
        db.delete_column('photos_album', 'published')


    models = {
        'photos.album': {
            'Meta': {'object_name': 'Album'},
            'gdata_id': ('django.db.models.fields.CharField', [], {'max_length': '31'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
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
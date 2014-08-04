# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'CoverPhoto.id'
        db.delete_column('photos_coverphoto', 'id')


        # Changing field 'CoverPhoto.album'
        db.alter_column('photos_coverphoto', 'album_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, primary_key=True, to=orm['photos.Album']))
        # Adding field 'Photo.taken'
        db.add_column('photos_photo', 'taken',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'CoverPhoto.id'
        raise RuntimeError("Cannot reverse this migration. 'CoverPhoto.id' and its values cannot be restored.")

        # Changing field 'CoverPhoto.album'
        db.alter_column('photos_coverphoto', 'album_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['photos.Album'], unique=True))
        # Deleting field 'Photo.taken'
        db.delete_column('photos_photo', 'taken')


    models = {
        'photos.album': {
            'Meta': {'ordering': "('-published',)", 'object_name': 'Album'},
            'gdata_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '31'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        'photos.coverphoto': {
            'Meta': {'object_name': 'CoverPhoto'},
            'album': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'thumbnail'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['photos.Album']"}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'photos.photo': {
            'Meta': {'ordering': "('published',)", 'object_name': 'Photo'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'to': "orm['photos.Album']"}),
            'gdata_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '31'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {}),
            'taken': ('django.db.models.fields.DateTimeField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'photos.resizedphoto': {
            'Meta': {'ordering': "('published',)", 'object_name': 'ResizedPhoto', '_ormbases': ['photos.Photo']},
            'photo_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['photos.Photo']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['photos']

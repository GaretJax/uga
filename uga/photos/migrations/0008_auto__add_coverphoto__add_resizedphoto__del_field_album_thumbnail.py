# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CoverPhoto'
        db.create_table('photos_coverphoto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('width', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('height', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('album', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['photos.Album'], unique=True)),
        ))
        db.send_create_signal('photos', ['CoverPhoto'])

        # Adding model 'ResizedPhoto'
        db.create_table('photos_resizedphoto', (
            ('photo_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['photos.Photo'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('photos', ['ResizedPhoto'])

        # Deleting field 'Album.thumbnail'
        db.delete_column('photos_album', 'thumbnail')


    def backwards(self, orm):
        # Deleting model 'CoverPhoto'
        db.delete_table('photos_coverphoto')

        # Deleting model 'ResizedPhoto'
        db.delete_table('photos_resizedphoto')


        # User chose to not deal with backwards NULL issues for 'Album.thumbnail'
        raise RuntimeError("Cannot reverse this migration. 'Album.thumbnail' and its values cannot be restored.")

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
            'album': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['photos.Album']", 'unique': 'True'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
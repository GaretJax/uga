# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'List'
        db.create_table('inscriptions_list', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('rate', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('limit', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('deleting', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('inscriptions', ['List'])

        # Adding model 'Inscription'
        db.create_table('inscriptions_inscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('list', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inscriptions.List'])),
        ))
        db.send_create_signal('inscriptions', ['Inscription'])

        # Adding unique constraint on 'Inscription', fields ['contact', 'list']
        db.create_unique('inscriptions_inscription', ['contact', 'list_id'])

        # Adding model 'InscriptionEntry'
        db.create_table('inscriptions_inscriptionentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('inscription', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inscriptions.Inscription'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('inscriptions', ['InscriptionEntry'])


    def backwards(self, orm):
        # Removing unique constraint on 'Inscription', fields ['contact', 'list']
        db.delete_unique('inscriptions_inscription', ['contact', 'list_id'])

        # Deleting model 'List'
        db.delete_table('inscriptions_list')

        # Deleting model 'Inscription'
        db.delete_table('inscriptions_inscription')

        # Deleting model 'InscriptionEntry'
        db.delete_table('inscriptions_inscriptionentry')


    models = {
        'inscriptions.inscription': {
            'Meta': {'ordering': "('timestamp',)", 'unique_together': "(('contact', 'list'),)", 'object_name': 'Inscription'},
            'contact': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inscriptions.List']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'inscriptions.inscriptionentry': {
            'Meta': {'ordering': "('timestamp',)", 'object_name': 'InscriptionEntry'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inscriptions.Inscription']"}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'inscriptions.list': {
            'Meta': {'object_name': 'List'},
            'deleting': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rate': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        }
    }

    complete_apps = ['inscriptions']
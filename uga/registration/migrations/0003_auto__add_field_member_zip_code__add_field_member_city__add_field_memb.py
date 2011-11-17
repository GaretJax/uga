# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Member.zip_code'
        db.add_column('registration_member', 'zip_code', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True), keep_default=False)

        # Adding field 'Member.city'
        db.add_column('registration_member', 'city', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Member.street'
        db.add_column('registration_member', 'street', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Member.street_number'
        db.add_column('registration_member', 'street_number', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Member.zip_code'
        db.delete_column('registration_member', 'zip_code')

        # Deleting field 'Member.city'
        db.delete_column('registration_member', 'city')

        # Deleting field 'Member.street'
        db.delete_column('registration_member', 'street')

        # Deleting field 'Member.street_number'
        db.delete_column('registration_member', 'street_number')


    models = {
        'registration.member': {
            'Meta': {'object_name': 'Member'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'street_number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'zip_code': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['registration']

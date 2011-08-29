# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Member.first_name'
        db.alter_column('registration_member', 'first_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Member.last_name'
        db.alter_column('registration_member', 'last_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Adding unique constraint on 'Member', fields ['email']
        db.create_unique('registration_member', ['email'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Member', fields ['email']
        db.delete_unique('registration_member', ['email'])

        # Changing field 'Member.first_name'
        db.alter_column('registration_member', 'first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Member.last_name'
        db.alter_column('registration_member', 'last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255))


    models = {
        'registration.member': {
            'Meta': {'object_name': 'Member'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['registration']

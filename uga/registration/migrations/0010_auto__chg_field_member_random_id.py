# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Member.random_id'
        db.alter_column('registration_member', 'random_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64))

    def backwards(self, orm):

        # Changing field 'Member.random_id'
        db.alter_column('registration_member', 'random_id', self.gf('django.db.models.fields.CharField')(max_length=128, unique=True))

    models = {
        'registration.member': {
            'Meta': {'ordering': "('first_name', 'last_name')", 'object_name': 'Member'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'random_id': ('django.db.models.fields.CharField', [], {'default': "'07987971380248d14823f8333bc483a2187dc1d110fc800aa6973e2d579dad65'", 'unique': 'True', 'max_length': '64'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'street_number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'registration.membership': {
            'Meta': {'unique_together': "(('person', 'year'),)", 'object_name': 'Membership'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registration.Member']"}),
            'year': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registration.SubscriptionYear']"})
        },
        'registration.subscriptionyear': {
            'Meta': {'object_name': 'SubscriptionYear'},
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['registration.Member']", 'through': "orm['registration.Membership']", 'symmetrical': 'False'}),
            'start': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['registration']
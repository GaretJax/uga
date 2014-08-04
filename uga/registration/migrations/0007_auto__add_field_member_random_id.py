# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Member.random_id'
        db.add_column('registration_member', 'random_id',
                      self.gf('django.db.models.fields.CharField')(max_length=128, unique=True, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Member.random_id'
        db.delete_column('registration_member', 'random_id')


    models = {
        'registration.member': {
            'Meta': {'ordering': "('first_name', 'last_name')", 'object_name': 'Member'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'random_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True'}),
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
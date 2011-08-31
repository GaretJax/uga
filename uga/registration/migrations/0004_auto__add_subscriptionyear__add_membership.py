# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SubscriptionYear'
        db.create_table('registration_subscriptionyear', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('end', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('registration', ['SubscriptionYear'])

        # Adding model 'Membership'
        db.create_table('registration_membership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_joined', self.gf('django.db.models.fields.DateField')()),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.Member'])),
            ('year', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.SubscriptionYear'])),
        ))
        db.send_create_signal('registration', ['Membership'])


    def backwards(self, orm):
        
        # Deleting model 'SubscriptionYear'
        db.delete_table('registration_subscriptionyear')

        # Deleting model 'Membership'
        db.delete_table('registration_membership')


    models = {
        'registration.member': {
            'Meta': {'object_name': 'Member'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'street_number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'registration.membership': {
            'Meta': {'object_name': 'Membership'},
            'date_joined': ('django.db.models.fields.DateField', [], {}),
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

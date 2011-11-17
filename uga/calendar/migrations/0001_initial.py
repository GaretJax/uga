# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MonthCalendarPlugin'
        db.create_table('cmsplugin_monthcalendarplugin', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('display_details', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('calendar', ['MonthCalendarPlugin'])

        # Adding M2M table for field calendars_to_display on 'MonthCalendarPlugin'
        db.create_table('calendar_monthcalendarplugin_calendars_to_display', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('monthcalendarplugin', models.ForeignKey(orm['calendar.monthcalendarplugin'], null=False)),
            ('calendar', models.ForeignKey(orm['schedule.calendar'], null=False))
        ))
        db.create_unique('calendar_monthcalendarplugin_calendars_to_display', ['monthcalendarplugin_id', 'calendar_id'])


    def backwards(self, orm):
        
        # Deleting model 'MonthCalendarPlugin'
        db.delete_table('cmsplugin_monthcalendarplugin')

        # Removing M2M table for field calendars_to_display on 'MonthCalendarPlugin'
        db.delete_table('calendar_monthcalendarplugin_calendars_to_display')


    models = {
        'calendar.monthcalendarplugin': {
            'Meta': {'object_name': 'MonthCalendarPlugin', 'db_table': "'cmsplugin_monthcalendarplugin'", '_ormbases': ['cms.CMSPlugin']},
            'calendars_to_display': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['schedule.Calendar']", 'symmetrical': 'False'}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'display_details': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'publisher_is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'publisher_public': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'publisher_draft'", 'unique': 'True', 'null': 'True', 'to': "orm['cms.CMSPlugin']"}),
            'publisher_state': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'schedule.calendar': {
            'Meta': {'object_name': 'Calendar'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'db_index': 'True'})
        }
    }

    complete_apps = ['calendar']

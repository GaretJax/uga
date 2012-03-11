from django.contrib.admin.util import unquote
from django.contrib import admin
from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.http import Http404, HttpResponse
from django.template.defaultfilters import slugify

import csv
import models
import signals


class ListAdmin(admin.ModelAdmin):
    list_display = ('name', 'open', 'count', 'limit', 'rate')
    list_editable = ('limit', 'rate')
    
    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        
        info = self.model._meta.app_label, self.model._meta.module_name
        urls = super(ListAdmin, self).get_urls()
        
        my_urls = patterns('',
            url(r'^(.+)/export/$',
                self.admin_site.admin_view(self.export),
                name='%s_%s_export' % info)
        )
        
        return my_urls + urls
        
    def export(self, request, object_id):
        model = self.model
        opts = model._meta
        obj = self.get_object(request, unquote(object_id))
        
        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})
        
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=elenco-iscritti-%s.csv' % slugify(obj.name)
        
        writer = csv.writer(response)
        writer.writerow(['#', 'Nome', 'Cognome', 'Iscritto il', 'Iscritto alle', 'Iscritto da'])
        
        for entry in obj.entries().all():
            writer.writerow([
                entry.rank(),
                entry.first_name.encode('utf-8'),
                entry.last_name.encode('utf-8'),
                entry.timestamp.strftime("%d %B %Y"),
                entry.timestamp.strftime("%H:%M:%S") + ".%06d" % entry.timestamp.microsecond,
                entry.inscription.contact,
            ])
        
        return response

admin.site.register(models.List, ListAdmin)


class EntryInline(admin.TabularInline):
    model = models.InscriptionEntry

class InscriptionAdmin(admin.ModelAdmin):
    inlines = [
        EntryInline,
    ]
    
    list_filter = ('list',)
    list_display = ('list', 'names', 'timestamp')
    
admin.site.register(models.Inscription, InscriptionAdmin)

def event(obj):
    return obj.inscription.list
event.admin_order_field = 'inscription__list'

class InscriptionEntryAdmin(admin.ModelAdmin):
    list_display = ('rank', 'full_name', 'first_name', 'last_name', 'timestamp', event, 'enrolled',)
    list_display_links = ('rank', 'full_name',)
    list_editable = ('first_name', 'last_name')
    #list_filter = ('inscription__list',)
    
    def save_model(self, request, obj, form, change):
        print obj.full_name()
        print change
        obj.save()
    
admin.site.register(models.InscriptionEntry, InscriptionEntryAdmin)
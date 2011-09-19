from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from uga.registration import models

# Requires django 1.4
#class IncompleteListFilter(admin.SimpleListFilter):
#    title = _('completion')
#
#    parameter_name = 'status'
#
#    def lookups(self, request, model_admin):
#        return (
#            ('complete', _('Complete')),
#            ('incomplete', _('Incomplete')),
#        )
#
#    def queryset(self, request, queryset):
#        if self.value():
#            query = queryset.model.objects._get_completion_query()
#
#            if self.value() == 'incomplete':
#                query = ~query
#
#            queryset = queryset.filter(query)
#
#        return queryset
#


class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'street', 'street_number', 'is_complete')
#    list_filter = (IncompleteListFilter,)
admin.site.register(models.Member, MemberAdmin)



class SubscriptionYearAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.SubscriptionYear, SubscriptionYearAdmin)



class MembershipAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Membership, MembershipAdmin)
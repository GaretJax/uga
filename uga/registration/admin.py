from django.contrib import admin
from uga.registration import models

class MemberAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Member, MemberAdmin)
from django.contrib import admin
from . import models

class LocationAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Location, LocationAdmin)


class EventLocationAdmin(admin.ModelAdmin):
        pass
admin.site.register(models.EventLocation, EventLocationAdmin)

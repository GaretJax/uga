from django.contrib import admin

from . import models


class AlbumAdmin(admin.ModelAdmin):
    exclude = ('gdata_id',)
admin.site.register(models.Album, AlbumAdmin)


class PhotoAdmin(admin.ModelAdmin):
    exclude = ('gdata_id',)
admin.site.register(models.Photo, PhotoAdmin)


class CoverPhotoAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.CoverPhoto, CoverPhotoAdmin)

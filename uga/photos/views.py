from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from . import models


class Photo(object):
    def get_absolute_url(self):
        return reverse('photo', kwargs={'album_id': self.album_id, 'photo_id': self.id})


def albums(request):
    return render(request, 'uga/photos/albums.html', {
        'albums': models.Album.objects.all(),
    })


def album(request, album_id):
    return render(request, 'uga/photos/album.html', {
        'album': get_object_or_404(models.Album, pk=album_id),
    })


def photo(request, album_id, photo_id):
    return render(request, 'uga/photos/photo.html', {
        'photo': get_object_or_404(models.Photo, pk=photo_id),
    })

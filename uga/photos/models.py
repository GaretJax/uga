from django.db import models
from django.utils.timezone import utc
import re
from collections import namedtuple
from datetime import datetime

from dateutil.parser import parse


Image = namedtuple('Image', ['url', 'width', 'height', 'cropped'])


class Album(models.Model):
    gdata_id = models.CharField(max_length=31, unique=True)
    title = models.CharField(max_length=255)
    updated = models.DateTimeField()
    published = models.DateTimeField()

    @classmethod
    def from_gdata(cls, gdata, update=True):
        try:
            obj = cls.objects.get(gdata_id=gdata.gphoto_id.text)
            created = False
        except cls.DoesNotExist:
            obj = cls(gdata_id=gdata.gphoto_id.text)
            created = True

        if created or update:
            obj.title = gdata.title.text
            obj.updated = parse(gdata.updated.text)
            obj.published = parse(gdata.published.text)
            obj.save()

            try:
                cover = CoverPhoto.objects.get(album=obj)
            except CoverPhoto.DoesNotExist:
                cover = CoverPhoto(album=obj)

            cover.url = gdata.media.thumbnail[0].url
            cover.height=gdata.media.thumbnail[0].height
            cover.width=gdata.media.thumbnail[0].width

            cover.save()

        return obj, created

    @property
    def size(self):
        return self.photos.count()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-published',)


class PhotoBase(models.Model):
    url = models.URLField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    def __getattr__(self, name):
        if name.startswith('img_'):
            _, size = name.split('_')
            crop = size.endswith('c')
            size = int(size[:-1]) if crop else int(size)
            return self.resized(size, crop=crop)
        return super(PhotoBase, self).__getattr__(name)

    def resized(self, size, crop=False):
        kwargs = {f.name: getattr(self, f.name) for f in self._meta.fields}
        res = ResizedPhoto(**kwargs)

        if crop:
            crop = '-c'
            res.width = res.height = size
        else:
            crop = ''
            if res.width > res.height:
                res.width = size
                res.height = size * self.height/self.width
            else:
                res.height = size
                res.width = size * self.width/self.height

        res.url = re.sub(r'/s\d+(-c)?/', '/s{:d}{}/'.format(size, crop), self.url)

        return res

    class Meta:
        abstract = True


class Photo(PhotoBase):
    album = models.ForeignKey(Album, related_name='photos')
    gdata_id = models.CharField(max_length=31, unique=True)
    taken = models.DateTimeField()
    published = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        ordering = ('taken',)

    @property
    def next(self):
        try:
            return self.__class__.objects.filter(
                album=self.album
            ).filter(
                taken__gt=self.taken
            )[0]
        except IndexError:
            return None

    @property
    def prev(self):
        try:
            return self.__class__.objects.filter(
                album=self.album
            ).filter(
                taken__lt=self.taken
            ).reverse()[0]
        except IndexError:
            return None

    @property
    def index(self):
        return self.__class__.objects.filter(
            album=self.album
        ).filter(
            taken__lt=self.taken
        ).reverse().count() + 1

    @classmethod
    def from_gdata(cls, gdata, album=None, update=True):
        try:
            obj = cls.objects.get(gdata_id=gdata.gphoto_id.text)
            created = False
        except cls.DoesNotExist:
            obj = cls(gdata_id=gdata.gphoto_id.text)
            created = True
            if album:
                obj.album = album
            else:
                obj.album = Album.objects.get(gdata_id=gdata.albumid.text)

        if created or update:
            obj.url = gdata.media.thumbnail[0].url
            obj.updated = parse(gdata.updated.text)
            obj.published = parse(gdata.published.text)
            obj.taken = datetime.fromtimestamp(int(gdata.timestamp.text)/1000).replace(tzinfo=utc)
            obj.width = int(gdata.width.text)
            obj.height = int(gdata.height.text)

            obj.save()

        return obj, created


class CoverPhoto(PhotoBase):
    album = models.OneToOneField(Album, related_name='thumbnail', primary_key=True)


class ResizedPhoto(Photo):
    def save(self, *args, **kwargs):
        raise RuntimeError('Cannot save ResizedPhoto instances')

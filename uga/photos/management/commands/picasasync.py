from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option

from gdata.photos import service as picasa
from ... import models


ALBUM_URI = 'https://picasaweb.google.com/data/feed/api/user/{user}/albumid/{album}?kind=photo&thumbsize=100c'


class Command(BaseCommand):
    args = ''
    help = u'Syncs photos and albums from the Picasa account'

    option_list = BaseCommand.option_list + (
        make_option('--all',
            action='store_true',
            dest='update',
            default=False,
            help=u'Syncs all albums (even the ones which already exist in the DB)'),
        make_option('--only-new',
            action='store_false',
            dest='update',
            default=False,
            help=u'Only syncs albums which don\'t yet exist in the DB (default, use this to override a previous --only-new flag)'),
    )

    def handle(self, *args, **options):
        client = picasa.PhotosService()
        albums_data = client.GetUserFeed(user=settings.PICASA_USER)

        a_count = len(albums_data.entry)
        p_count = 0

        self.stdout.write(u'Preparing to import {} albums...\n'.format(a_count))

        try:
            for i, album_data in enumerate(albums_data.entry):
                album, created = models.Album.from_gdata(album_data, update=options['update'])

                self.stdout.write(u'\r' + ' ' * 80)
                #self.stdout.write(u'\rProcessing {}/{}: \'{}\'... '.format(
                #        i+1, a_count, album.title))
                self.stdout.flush()

                if not options['update'] and not created:
                    continue

                uri = ALBUM_URI.format(
                    user=album_data.user.text,
                    album=album_data.gphoto_id.text
                )

                photos_data = client.GetFeed(uri)
                ap_count = len(photos_data.entry)
                for j, photo_data in enumerate(photos_data.entry):
                    self.stdout.write(u'\r' + ' ' * 80)
                    #self.stdout.write(u'\rProcessing {}/{}: \'{}\' (photo {}/{})... '.format(
                    #        i+1, a_count, album.title, j, ap_count))
                    self.stdout.flush()
                    models.Photo.from_gdata(photo_data, album=album)
                    p_count += 1
        except KeyboardInterrupt:
            self.stdout.write(u'\nAborting...\n')

        # TODO: Remove removed photos and albums

        self.stdout.write(u'\r' + ' ' * 80)
        self.stdout.write(u'\rImported {} photos in {} albums\n'.format(p_count, i + 1))

        #import xml.dom.minidom
        #xml = xml.dom.minidom.parseString(str(photo_data))
        #print xml.toprettyxml()
        #print int(photo_data.timestamp.text)

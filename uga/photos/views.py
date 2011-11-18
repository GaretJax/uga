from django.shortcuts import render_to_response
from django.template import RequestContext

from gdata.photos import service as picasa


def albums(request):
    client = picasa.PhotosService()

    albums = client.GetUserFeed(user='ugawebmail@gmail.com')

    print dir(albums.entry[0])
    return render_to_response('uga/photos/albums.html', {
        'albums': albums,
    }, context_instance = RequestContext(request))



def ____():
    url = 'https://picasaweb.google.com/data/feed/api/user/ugawebmail@gmail.com'

    import urllib

    from xml.etree import ElementTree

    class Namespace(object):
        def __init__(self, uri):
            self.uri = uri

        def __call__(self, tag):
            return '{{{0}}}{1}'.format(self.uri, tag)


    q = Namespace('http://www.w3.org/2005/Atom')

    fu = urllib.urlopen(url)
    xml = fu.read()
    print xml
    albums = ElementTree.fromstring(xml)
    fu.close()



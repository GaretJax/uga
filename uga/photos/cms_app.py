from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class PhotosHook(CMSApp):
    name = _("Photo gallery")
    urls = ["uga.photos.urls"]

apphook_pool.register(PhotosHook)


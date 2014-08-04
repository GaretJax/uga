from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class InscriptionsHook(CMSApp):
    name = _("Ticketcorner")
    urls = ["uga.inscriptions.urls"]

apphook_pool.register(InscriptionsHook)

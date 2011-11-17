from cms import app_base
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from uga.registration import menu



class RegistrationAppHook(app_base.CMSApp):
    name = _("Registration manager")
    urls = ["uga.registration.urls"]
    menus = [menu.RegistrationMenu]

apphook_pool.register(RegistrationAppHook)
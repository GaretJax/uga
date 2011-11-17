from cms.menu_bases import CMSAttachMenu
from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class RegistrationMenu(CMSAttachMenu):
    name = _("Registration menu")

    def get_nodes(self, request):
        return [
            NavigationNode(_('Nuova iscrizione'), reverse('enroll'), 1),
            NavigationNode(_('Esporta indirizzi email'), reverse('export_emails'), 2),
        ]

menu_pool.register_menu(RegistrationMenu)

# -*- coding: UTF-8 -*-

from django.dispatch import Signal
from django.contrib.sites.models import Site

from uga.inscriptions.shortcuts import render_to_mail


enrollment_added = Signal(providing_args=["event", "enrollment"])

def send_confirmation_mail(sender, event, inscription, **kwargs):
    render_to_mail(
        u'[UGA] Iscrizione a “{}”'.format(event.event.title),
        'eventi@uga.ch',
        [inscription.contact,],
        'inscriptions/mails/confirmation.txt',
        'inscriptions/mails/confirmation.html',
        {
            'event': event,
            'inscription': inscription,
            'site': Site.objects.get_current(),
        }
    )

enrollment_added.connect(send_confirmation_mail)

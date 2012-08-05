# -*- coding: UTF-8 -*-

from django.dispatch import Signal
from uga.inscriptions.shortcuts import render_to_mail

enrollment_added = Signal(providing_args=["event", "enrollment"])
enrollment_name_deleted = Signal(providing_args=["event", "enrollment", "entry"])


def delete_enrollment_name(sender, instance, **kwargs):
    from .models import Inscription
    try:
        send_update_mail(sender, instance.inscription.list, instance.inscription, instance)
    except Inscription.DoesNotExist:
        pass


def send_update_mail(sender, event, enrollment, entry, **kwargs):
    from models import InscriptionEntry
    from django.contrib.sites.models import Site

    if entry.enrolled():
        try:
            newly_enrolled = InscriptionEntry.objects.filter(
                    inscription__list=event)[event.limit - 1]
        except IndexError:
            # Nobody is now enrolled
            pass
        else:
            render_to_mail(
                u'[UGA] Iscrizione a “%s”' % (event.name),
                'eventi@uga.ch',
                [newly_enrolled.inscription.contact,],
                'inscriptions/mails/enrolled.txt',
                'inscriptions/mails/enrolled.html',
                {
                    'event': event,
                    'inscription': newly_enrolled.inscription,
                    'enrolled': newly_enrolled,
                    'site': Site.objects.get_current(),
                }
            )

enrollment_name_deleted.connect(send_update_mail)


def send_confirmation_mail(sender, event, inscription, **kwargs):
    from django.contrib.sites.models import Site

    render_to_mail(
        u'[UGA] Iscrizione a “%s”' % (event.name),
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

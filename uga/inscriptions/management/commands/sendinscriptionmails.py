# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

from ...models import List, InscriptionEntry

from uga.inscriptions.shortcuts import render_to_mail
from django.core.mail import get_connection


#enrollment_name_deleted.connect(send_update_mail)


class Command(BaseCommand):
    help = 'Sends emails to update the status of the inscriptions to selected events'

    def handle(self, *args, **options):
        to_update = {}

        for l in List.objects.all():
            inscriptions = InscriptionEntry.objects.filter(inscription__list=l).all()
            self.stdout.write('Checking \'{}\':\n'.format(l))
            for count, i in enumerate(inscriptions):
                if count < l.limit:
                    if not i.confirmation_sent:
                        self.stdout.write(' * Confirming \'{}\'\n'.format(i))
                        i.confirmation_sent = True
                        i.save()
                        to_update.setdefault(i.inscription, []).append(i)
                else:
                    break

        if not to_update:
            self.stdout.write('No mails were sent\n')
        else:
            self.stdout.write('\nPreparing to send {} mails...\n'.format(len(to_update)))

            connection = get_connection()
            connection.open()

            for inscription, entries in to_update.iteritems():
                render_to_mail(
                    u'[UGA] Iscrizione a “%s”' % (inscription.list.event.title),
                    'eventi@uga.ch',
                    [inscription.contact,],
                    'inscriptions/mails/enrolled.txt',
                    'inscriptions/mails/enrolled.html',
                    {
                        'event': inscription.list,
                        'inscription': inscription,
                        'enrolled': entries,
                        'site': Site.objects.get_current(),
                    },
                    connection=connection
                )
                self.stdout.write('.')
            self.stdout.write('\n')
            connection.close()
            self.stdout.write('Done\n')

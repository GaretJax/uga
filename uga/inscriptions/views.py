# -*- coding: UTF-8 -*-

from django.shortcuts import get_object_or_404, render, redirect
from django.forms.util import ErrorList
from django.db import IntegrityError, transaction
from django.utils import timezone as tz

from models import List, Inscription, InscriptionEntry
from forms import InscriptionEntryFormSet, InscriptionForm, InscriptionEntryForm

from . import utils, signals
from django.contrib import messages


def remove(request, inscription_id, auth, name_id):
    ins = get_object_or_404(Inscription, pk=inscription_id, password=auth)
    entry = get_object_or_404(InscriptionEntry, pk=name_id, inscription=ins)

    if 'confirmed' in request.GET:
        entry.delete()

        #signals.enrollment_name_deleted.send(sender=InscriptionEntry, event=ins.list, enrollment=ins, entry=entry)

        if ins.inscriptionentry_set.count() == 0:
            ins.delete()
            messages.add_message(request, messages.INFO,
                    u"La tua iscrizione all'evento “{}” è stata correttamente rimossa dal sistema.".format(ins.list.event.title))
            return redirect('inscriptions.list')
        else:
            messages.add_message(request, messages.INFO,
                    u"Il nominativo “{}” é stato correttamente rimosso dalla tua iscrizione.".format(entry.full_name()))
            return redirect('inscriptions.manage', inscription_id=ins.pk, auth=ins.password)

    return render(request, 'inscriptions/confirm_remove.html', {
        'inscription': ins,
        'entry': entry,
    })


def manage(request, inscription_id, auth):
    ins = get_object_or_404(Inscription, pk=inscription_id, password=auth)
    error = ''

    if ins.list.open() and ins.inscriptionentry_set.count() < ins.list.rate:
        if request.method == 'POST':
            form = InscriptionEntryForm(request.POST)

            if form.is_valid():
                ins.add_name(form.cleaned_data['first_name'], form.cleaned_data['last_name'])
                messages.add_message(request, messages.INFO,
                    u"Il nominativo “{} {}” é stato correttamente aggiunto alla tua iscrizione.".format(form.cleaned_data['first_name'], form.cleaned_data['last_name']))
                return redirect('inscriptions.manage', inscription_id=ins.pk, auth=ins.password)
            else:
                if 'first_name' in form.errors:
                    error = form.errors['first_name']
                elif 'last_name' in form.errors:
                    error = form.errors['last_name']
        else:
            form = InscriptionEntryForm()
    else:
        form = None

    return render(request, 'inscriptions/manage.html', {
        'inscription': ins,
        'subscription': form,
        'error': error,
    })


def list_events(request):
    return render(request, 'inscriptions/list.html', {
        'events': List.objects.exclude(end__lte=tz.now()),
    })


def subscribe(request, list_id):
    e = get_object_or_404(List, pk=int(list_id))

    # Assert that list is open
    if e.start > tz.now():
        return render(request, 'inscriptions/subscription_not_yet_opened.html', {
            'event': e,
        })
    elif e.end and e.end < tz.now():
        return render(request, 'inscriptions/subscription_already_closed.html', {
            'event': e,
        })

    if request.method == 'POST':
        formset = InscriptionEntryFormSet(e.rate, request.POST)
        form = InscriptionForm(request.POST)

        if formset.is_valid() and form.is_valid():
            inscription = form.save(commit=False)
            inscription.list = e

            try:
                tid = transaction.savepoint()
                inscription.save()
            except IntegrityError:
                transaction.savepoint_rollback(tid)

                # Handle duplicate email addresses
                if 'contact' not in form._errors:
                    form._errors['contact'] = ErrorList()

                form._errors['contact'].append(u"Questo indirizzo email è già stato utilizzato per un'altra iscrizione.")
            else:
                transaction.savepoint_commit(tid)
                utils.save_entries(formset, inscription)
                signals.enrollment_added.send(sender=Inscription,
                        event=e, inscription=inscription)
                messages.add_message(request, messages.INFO,
                        u"Complimenti, la tua iscrizione all'evento “{}” é stata conclusa con successo, fra poco riceverai un'email all'indirizzo “{}” con il riassunto dell'iscrizione.".format(e.event.title, inscription.contact))

                return redirect('inscriptions.manage', inscription_id=inscription.pk, auth=inscription.password)
    else:
        formset = InscriptionEntryFormSet(e.rate)
        form = InscriptionForm()

    return render(request, 'inscriptions/subscription_form.html', {
        'subscription_formset': formset,
        'inscription_form': form,
        'event': e,
    })

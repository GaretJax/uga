# -*- coding: UTF-8 -*-

from datetime import datetime

from uga.inscriptions.shortcuts import render_to_response as render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.db import transaction, IntegrityError
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList

from models import List, Inscription, InscriptionEntry
from forms import InscriptionEntryFormSet, InscriptionForm, InscriptionEntryForm

import signals
import utils

def get_and_delete_message(request):
    if 'message' in request.session:
        message = request.session['message']
        del request.session['message']
        return message

    return ''

def remove(request, inscription_id, auth, name_id):
    ins = get_object_or_404(Inscription, pk=inscription_id, password=auth)
    entry = get_object_or_404(InscriptionEntry, pk=name_id, inscription=ins)

    if 'confirmed' in request.GET:
        entry.delete()

        #signals.enrollment_name_deleted.send(sender=InscriptionEntry, event=ins.list, enrollment=ins, entry=entry)

        if ins.inscriptionentry_set.count() == 0:
            ins.delete()
            request.session['message'] = u"La tua iscrizione all'evento “%s” è stata correttamente rimossa dal sistema." % (ins.list.name)
            return HttpResponseRedirect(reverse('inscriptions.list'))
        else:
            request.session['message'] = u"Il nominativo “%s” é stato correttamente rimosso dalla tua iscrizione." % (entry.full_name())

            return HttpResponseRedirect(reverse(
                'inscriptions.manage', kwargs={
                    'inscription_id': ins.pk,
                    'auth': ins.password,
                }))

    return render('inscriptions/confirm_remove.html', {
        'inscription': ins,
        'entry': entry,
    }, request)

def manage(request, inscription_id, auth):
    ins = get_object_or_404(Inscription, pk=inscription_id, password=auth)
    error = ''

    if ins.list.open() and ins.inscriptionentry_set.count() < ins.list.rate:
        if request.method == 'POST':
            form = InscriptionEntryForm(request.POST)

            if form.is_valid():
                ins.add_name(form.cleaned_data['first_name'], form.cleaned_data['last_name'])
                request.session['message'] = u"Il nominativo “%s %s” é stato correttamente aggiunto alla tua iscrizione." % (form.cleaned_data['first_name'], form.cleaned_data['last_name'])
                return HttpResponseRedirect(reverse(
                    'inscriptions.manage', kwargs={
                        'inscription_id': ins.pk,
                        'auth': ins.password,
                    }))
            else:
                if 'first_name' in form.errors:
                    error = form.errors['first_name']
                elif 'last_name' in form.errors:
                    error = form.errors['last_name']
        else:
            form = InscriptionEntryForm()
    else:
        form = None

    return render('inscriptions/manage.html', {
        'inscription': ins,
        'subscription': form,
        'error': error,
        'message': get_and_delete_message(request),
    }, request)

def list_events(request):
    return render('inscriptions/list.html', {
        'events': List.objects.exclude(end__lte=datetime.now()),
        'message': get_and_delete_message(request),
    }, request)

@transaction.commit_manually
def subscribe(request, list_id):
    print "Entering"
    e = get_object_or_404(List, pk=int(list_id))

    if e.start > datetime.now():
        transaction.rollback()
        ret = render('inscriptions/subscription_not_yet_opened.html', {
            'event': e,
        }, request)
        transaction.commit()
        return ret
    elif e.end and e.end < datetime.now():
        transaction.rollback()
        ret = render('inscriptions/subscription_already_closed.html', {
            'event': e,
        }, request)
        transaction.commit()
        return ret

    if request.method == 'POST':
        print "POSTING"
        formset = InscriptionEntryFormSet(e.rate, request.POST)
        form = InscriptionForm(request.POST)

        if formset.is_valid() and form.is_valid():
            inscription = form.save(commit=False)
            inscription.list = e

            try:
                inscription.save()
            except IntegrityError:
                # Handle duplicate email addresses
                if 'contact' not in form._errors:
                    form._errors['contact'] = ErrorList()

                form._errors['contact'].append(u"Questo indirizzo email è già stato utilizzato per un'altra iscrizione.")

                transaction.rollback()
            except Exception:
                transaction.rollback()
                raise
            else:
                try:
                    utils.save_entries(formset, inscription)
                except Exception:
                    print "EX"
                    transaction.rollback()
                    raise
                else:
                    transaction.commit()
                    try:
                        signals.enrollment_added.send(sender=Inscription, event=e, inscription=inscription)
                    except Exception:
                        print "Mail was not sent"

                    request.session['message'] = u"Complimenti, la tua iscrizione all'evento “%s” é stata conclusa con successo, fra poco riceverai un'email all'indirizzo “%s” con il riassunto dell'iscrizione." % (e.name, inscription.contact)

                    response = HttpResponseRedirect(reverse(
                        'inscriptions.manage', kwargs={
                            'inscription_id': inscription.pk,
                            'auth': inscription.password,
                        }))

                    transaction.commit()

                    return response

    else:
        transaction.rollback()
        formset = InscriptionEntryFormSet(e.rate)
        form = InscriptionForm()

    res = render('inscriptions/subscription_form.html', {
        'subscription_formset': formset,
        'inscription_form': form,
        'event': e,
    }, request)

    transaction.commit()

    return res

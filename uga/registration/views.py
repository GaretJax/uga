from datetime import date

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages

from mailchimp.chimpy import chimpy

from uga.decorators import require_cms_permissions
from uga.registration import forms, models



@require_cms_permissions
def list(request):
    return render_to_response('uga/registration/list.html', {
        'members': models.Member.objects.all(),
    }, context_instance=RequestContext(request))



@require_cms_permissions
def mailing_list(request, member_id):
    member = get_object_or_404(models.Member, pk=int(member_id))

    if request.method == 'POST':
        action = request.POST['action']

        connection = chimpy.Connection(settings.MAILCHIMP_API_KEY)

        if action == 'subscribe':
            connection.list_subscribe(settings.MAILING_LIST_ID, member.email,
                    {'FNAME': member.first_name, 'LNAME': member.last_name}, 'html',
                    double_optin=False)
        elif action == 'unsubscribe':
            connection.list_unsubscribe(settings.MAILING_LIST_ID, member.email,
                    delete_member=False, send_goodbye=True, send_notify=False)
        elif action == 'resubscribe':
            connection.list_subscribe(settings.MAILING_LIST_ID, member.email,
                    {'FNAME': member.first_name, 'LNAME': member.last_name}, 'html',
                    double_optin=True)

    return HttpResponseRedirect(reverse('edit_member',
            kwargs={'member_id': int(member_id)}))



@require_cms_permissions
def subscriptions(request, member_id):
    member = get_object_or_404(models.Member, pk=int(member_id))

    if request.method == 'POST':
        action = request.POST['action']

        if action == 'delete':
            deletion_form = forms.SubscriptionDeletionForm(member, request.POST)

            if deletion_form.is_valid():
                membership = deletion_form.cleaned_data['membership']
                membership.delete()

                messages.success(request, 'The member <strong>{0}</strong> was correctly ' \
                        'unenrolled from <strong>{1}</strong>.'.format(member, membership.year))
        elif action == 'enroll':
            subscription_form = forms.SubscriptionForm(member, request.POST)

            if subscription_form.is_valid():
                membership = models.Membership.objects.create(person=member,
                    year=subscription_form.cleaned_data['subscription'])

                # Create a new message
                messages.success(request, 'The member <strong>{0}</strong> was correctly ' \
                        'enrolled to <strong>{1}</strong>.'.format(member, membership.year))

    return HttpResponseRedirect(reverse('edit_member',
            kwargs={'member_id': int(member_id)}))



@require_cms_permissions
def edit(request, member_id):
    member = get_object_or_404(models.Member, pk=int(member_id))
    connection = chimpy.Connection(settings.MAILCHIMP_API_KEY)

    if request.method == 'POST':
        old_email = member.email
        old_full_name = member.get_full_name()

        # Handle data submission
        edit_form = forms.EditForm(request.POST, instance=member)

        if edit_form.is_valid():
            # Save changes to member
            member = edit_form.save()

            if member.email != old_email or member.get_full_name() != old_full_name:
                try:
                    connection.list_update_member(settings.MAILING_LIST_ID, old_email, {
                        'FNAME': member.first_name,
                        'LNAME': member.last_name,
                        'EMAIL': member.email,
                    })
                except chimpy.ChimpyException:
                    pass

            # Create a new message
            messages.success(request, 'The changes to <strong>{0}</strong> where correctly ' \
                    'saved to the database.'.format(member))

            # Redirect
            return HttpResponseRedirect(reverse('list'))
    else:
        edit_form = forms.EditForm(instance=member)

    subscription_form = forms.SubscriptionForm(member)

    try:
        mailing_list_membership = connection.list_member_info(
                settings.MAILING_LIST_ID, member.email)
    except chimpy.ChimpyException:
        mailing_list_membership = None

    return render_to_response('uga/registration/edit.html', {
        'page_title': u'Modifica "{0}"'.format(member.get_full_name()),
        'member': member,
        'edit_form': edit_form,
        'subscription_form': subscription_form,
        'mailing_list_membership': mailing_list_membership,
    }, context_instance=RequestContext(request))



@require_cms_permissions
def export_emails(request):
    return render_to_response('uga/registration/export_emails.html', {
        'page_title': 'Esporta indirizzi email',
        'members': models.Member.objects.all(),
    }, context_instance=RequestContext(request))



@require_cms_permissions
def remove(request, member_id):
    member = get_object_or_404(models.Member, pk=int(member_id))

    if request.method == 'POST':
        # Remove member
        if request.POST['action'] != 'remove':
            return HttpResponseRedirect(reverse('edit_member',
                    kwargs={'member_id': int(member_id)}))

        # Remove from mailing list
        connection = chimpy.Connection(settings.MAILCHIMP_API_KEY)
        try:
            connection.list_unsubscribe(settings.MAILING_LIST_ID, member.email,
                    delete_member=True, send_goodbye=False, send_notify=False)
        except chimpy.ChimpyException:
            pass

        member.delete()

        messages.success(request, 'The member <strong>{0}</strong> was correctly ' \
                    'removed from the system.'.format(member.get_full_name()))

        return HttpResponseRedirect(reverse('list'))


    return render_to_response('uga/registration/remove.html', {
        'page_title': 'Rimozione socio',
        'member': member,
    }, context_instance=RequestContext(request))



@require_cms_permissions
def enroll(request):
    today = date.today()
    default_subscribtion = models.SubscriptionYear.objects.filter(
            start__lt=today).filter(end__gt=today).order_by('-end')[0]
    initial = {
        'subscription': default_subscribtion,
        'zip_code': 1700,
        'city': 'Fribourg',
        'mailing_list': True,
    }

    if request.method == 'POST':
        enroll_form = forms.EnrollForm(request.POST, initial=initial)

        if enroll_form.is_valid():
            # Create the member and the membership
            member = enroll_form.save()
            membership = models.Membership.objects.create(person=member,
                    year=enroll_form.cleaned_data['subscription'])

            if enroll_form.cleaned_data['mailing_list']:
                connection = chimpy.Connection(settings.MAILCHIMP_API_KEY)
                connection.list_subscribe(settings.MAILING_LIST_ID, member.email, {
                    'FNAME': member.first_name,
                    'LNAME': member.last_name
                }, 'html', double_optin=False)

            # Create a new message
            messages.success(request, 'The new member <strong>{0}</strong> was correctly ' \
                    'enrolled to <strong>{1}</strong>.'.format(member, membership.year))

            # Send confirmation email (background)
            return HttpResponseRedirect(reverse('enroll'))
    else:
        enroll_form = forms.EnrollForm(initial=initial)

    return render_to_response('uga/registration/enroll.html', {
        'page_title': 'Nuova iscrizione',
        'enroll_form': enroll_form,
    }, context_instance=RequestContext(request))


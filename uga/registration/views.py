from datetime import date

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages


from uga.registration import forms, models


def list(request):
    return render_to_response('uga/registration/list.html', {
        'members': models.Member.objects.all(),
    }, context_instance=RequestContext(request))


def enroll(request):
    today = date.today()
    default_subscribtion = models.SubscriptionYear.objects.filter(
            start__lt=today).filter(end__gt=today).order_by('-end')[0]
    initial = {
        'subscription': default_subscribtion,
        'zip_code': 1700,
        'city': 'Fribourg'
    }

    if request.method == 'POST':
        enroll_form = forms.EnrollForm(request.POST, initial=initial)

        if enroll_form.is_valid():
            # Create the member and the membership
            member = enroll_form.save()
            membership = models.Membership.objects.create(person=member,
                    year=enroll_form.cleaned_data['subscription'])

            # Create a new message
            messages.success(request, 'The new member <strong>{0}</strong> was correctly ' \
                    'enrolled to <strong>{1}</strong>'.format(member, membership.year))

            # Send confirmation email (background)

            return HttpResponseRedirect(reverse('enroll'))
    else:
        enroll_form = forms.EnrollForm(initial=initial)

    return render_to_response('uga/registration/enroll.html', {
        'page_title': 'Nuova iscrizione',
        'enroll_form': enroll_form,
    }, context_instance=RequestContext(request))

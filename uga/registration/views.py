
from django.shortcuts import render_to_response
from django.template import RequestContext



def enroll(request):
    return render_to_response('uga/registration/enroll.html', {
        'page_title': 'Iscrizione nuovo socio',
    }, context_instance=RequestContext(request))
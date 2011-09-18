from django import forms
from uga.registration import models
from django.utils.translation import ugettext_lazy as _



class EnrollForm(forms.ModelForm):

    # Additional fields
    subscription = forms.ModelChoiceField(
            queryset=models.SubscriptionYear.objects.all())

    # Overrides to specify custom attributes
    street = forms.CharField(label=_('Name'), required=False)
    street_number = forms.IntegerField(label=_('#'), required=False)
    zip_code = forms.IntegerField(label=_('CAP'), required=False)

    class Meta:
        model = models.Member


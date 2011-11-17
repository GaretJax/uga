from django import forms
from uga.registration import models
from django.utils.translation import ugettext_lazy as _



class EditForm(forms.ModelForm):

    # Overrides to specify custom attributes
    street = forms.CharField(label=_('Name'), required=False)
    street_number = forms.IntegerField(label=_('#'), required=False)
    zip_code = forms.IntegerField(label=_('CAP'), required=False)

    class Meta:
        model = models.Member



class SubscriptionForm(forms.Form):

    def __init__(self, member, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)

        self.fields['subscription'].queryset = models.SubscriptionYear.objects.exclude(membership__person=member).order_by('-start')

    subscription = forms.ModelChoiceField(
            queryset=models.SubscriptionYear.objects.all())



class SubscriptionDeletionForm(forms.Form):

    def __init__(self, member, *args, **kwargs):
        super(SubscriptionDeletionForm, self).__init__(*args, **kwargs)

        self.fields['membership'].queryset = member.membership_set

    membership = forms.ModelChoiceField(
            queryset=models.Membership.objects.all())



class EnrollForm(EditForm):

    mailing_list = forms.BooleanField(required=False)

    # Additional fields
    subscription = forms.ModelChoiceField(
            queryset=models.SubscriptionYear.objects.all())


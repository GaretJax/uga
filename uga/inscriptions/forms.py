from django import forms
from django.forms.formsets import formset_factory
from django.forms.formsets import BaseFormSet

from models import Inscription

class BaseInscriptionEntryFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        
        if not self.filled_forms_count():
            raise forms.ValidationError("Devi inserire almeno un nominativo da iscrivere.")
    
    def filled_forms_count(self):
        return sum((1 for f in self.forms if len(f.cleaned_data)))
    

class InscriptionEntryForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

class InscriptionForm(forms.ModelForm):
    
    def clean_contact(self):
        return self.cleaned_data['contact'].lower()
    
    class Meta:
        model = Inscription
        fields = ('contact',)

def InscriptionEntryFormSet(num, *args, **kwargs):
    return formset_factory(InscriptionEntryForm, formset=BaseInscriptionEntryFormSet, extra=num, max_num=num)(*args, **kwargs)
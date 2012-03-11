from models import InscriptionEntry

def save_entries(formset, inscription):
    for f in formset.forms:
        if not f.cleaned_data:
            continue
        
        inscription.add_name(f.cleaned_data['first_name'], f.cleaned_data['last_name'])

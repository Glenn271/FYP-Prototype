from django import forms
from .models import Prop
CITIES = [
    ('Balbriggan', 'Balbriggan'),
    ('Clondalkin', 'Clondalkin'),
    ('Finglas', 'Finglas'),
    ('Tallaght', 'Tallaght'),
]

class PropertySearchForm(forms.Form):
    city = forms.CharField(label='City', widget= forms.Select(choices = CITIES))
    rent = forms.CharField(label = 'Ideal Rent Price p/m', required = False)

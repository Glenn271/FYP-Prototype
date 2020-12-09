from django import forms
from .models import Prop
CITIES = [
    ('balbriggan', 'Balbriggan'),
    ('clondalkin', 'Clondalkin'),
    ('finglas', 'Finglas'),
    ('tallaght', 'Tallaght'),
]

class PropertySearchForm(forms.Form):
    city = forms.CharField(label='City', widget= forms.Select(choices = CITIES))

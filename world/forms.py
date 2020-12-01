from django import forms

CITIES = [
    ('clondalkin', 'Clondalkin'),
    ('finglas', 'Finglas'),
    ('tallaght', 'Tallaght'),
]

class PropertySearchForm(forms.Form):
    city = forms.CharField(label='City', widget= forms.Select(choices = CITIES))
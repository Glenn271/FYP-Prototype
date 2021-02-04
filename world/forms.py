from django import forms

CITIES = [
    ('Balbriggan', 'Balbriggan'),
    ('Clondalkin', 'Clondalkin'),
    ('Finglas', 'Finglas'),
    ('Tallaght', 'Tallaght'),
]

HOUSE_TYPE = [
    ('', 'Any'),
    ('Apartment ', 'Apartment'),
    ('Terraced House ', 'Terraced House'),
    ('Semi-Detached ', 'Semi-Detached'),
    ('Detached ', 'Detached'),
    ('Bungalow ', 'Bungalow'),
    ('Country House ', 'Country House'),
    ('Studio ', 'Studio')
]

class PropertySearchForm(forms.Form):
    city = forms.CharField(label='City', widget= forms.Select(choices = CITIES))
    #rent = forms.CharField(label = 'Ideal Rent Price p/m', required = False)
    house_type = forms.MultipleChoiceField(label='House Type', required = False,
                                           widget=forms.CheckboxSelectMultiple, choices = HOUSE_TYPE)
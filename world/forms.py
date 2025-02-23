from django import forms


CITIES = [
    ('Adamstown', 'Adamstown'),
    ('arbour-hill', 'Arbour Hill'),
    ('Artane', 'Artane'), ('Ashtown', 'Ashtown'),
    ('Aylesbury', 'Aylesbury'), ('Ayrfield', 'Ayrfield'),
    ('Balbriggan', 'Balbriggan'),
    ('Baldonnel', 'Baldonnel'), ('Baldoyle', 'Baldoyle'),
    ('Balgriffin', 'Balgriffin'),
    ('Ballinteer', 'Ballinteer'), ('Ballsbridge', 'Ballsbridge'),
    ('Ballybough', 'Ballybough'),
    ('Ballyboughal', 'Ballyboughal'), ('Ballybrack', 'Ballybrack'),
    ('Ballycoolin', 'Ballycoolin'),('Ballycullen', 'Ballycullen'),
    ('Ballyfermot', 'Ballyfermot'), ('Ballymount', 'Ballymount'),
    ('Ballymun', 'Ballymun'), ('Balrothery', 'Balrothery'),
    ('Balscaddan', 'Balscaddan'), ('Bayside', 'Bayside'),
    ('Beaumont', 'Beaumont'), ('Blackrock', 'Blackrock'),
    ('Blanchardstown', 'Blanchardstown'), ('Bluebell', 'Bluebell'),
    ('Bohernabreena', 'Bohernabreena'), ('Booterstown', 'Booterstown'),
    ('Brittas', 'Brittas'),
    ('Cabinteely', 'Cabinteely'), ('Cabra', 'Cabra'),
    ('Carpenterstown', 'Carpenterstown'), ('Carrickmines', 'Carrickmines'),
    ('Castleknock', 'Castleknock'), ('Chapelizod', 'Chapelizod'),
    ('cherry-orchard', 'Cherry Orchard'),('Cherrywood', 'Cherrywood'),
    ('Christchurch', 'Christchurch'),('Churchtown', 'Churchtown'),
    ('Citywest', 'Citywest'),('Clarehall', 'Clarehall'),
    ('Clondalkin', 'Clondalkin'),
    ('Clongriffin', 'Clongriffin'),
    ('Clonshaugh', 'Clonshaugh'),('Clonsilla', 'Clonsilla'),
    ('Clonskeagh', 'Clonskeagh'),('Clontarf', 'Clontarf'),
    ('Coolmine', 'Coolmine'), ('Coolock', 'Coolock'),
    ('Crumlin', 'Crumlin'), ('Dalkey', 'Dalkey'),
    ('Darndale', 'Darndale'),
    ('Dartry', 'Dartry'), ('deans-grange', 'Deansgrange'),
    ('dolphin-s-barn', 'Dolphins Barn'),
    ('Donabate', 'Donabate'), ('Donaghmede', 'Donaghmede'),
    ('Donnybrook', 'Donnybrook'), ('Donnycarney', 'Donnycarney'),
    ('Drimnagh', 'Drimnagh'),
    ('Drumcondra', 'Drumcondra'), ('dun-laoghaire', 'Dun Laoghaire'),
    ('Dundrum', 'Dundrum'), ('east-wall', 'East Wall'),
    ('Fairview', 'Fairview'), ('Finglas', 'Finglas'),
    ('Firhouse', 'Firhouse'), ('Foxrock', 'Foxrock'),
    ('Garristown', 'Garristown'), ('Glasnevin', 'Glasnevin'),
    ('Glasthule', 'Glasthule'), ('Glenageary', 'Glenageary'),
    ('Goatstown', 'Goatstown'),
    ('grand-canal-dock', 'Grand Canal Dock'),
    ('harold-s-cross', 'Harolds Cross'),('Hollystown', 'Hollystown'),
    ('Howth', 'Howth'), ('IFSC', 'IFSC'),
    ('Inchicore', 'Inchicore'), ('Irishtown', 'Irishtown'),
    ('Islandbridge', 'Islandbridge'),('Kilbarrack', 'Kilbarrack'),
    ('Killester', 'Killester'), ('Killiney', 'Killiney'),
    ('Kilmacud', 'Kilmacud'), ('Kilmainham', 'Kilmainham'),
    ('Kilnamanagh', 'Kilnamanagh'), ('Kilternan', 'Kilternan'),
    ('Kiltipper', 'Kiltipper'), ('Kimmage', 'Kimmage'),
    ('Kingswood', 'Kingswood'), ('Kinsealy', 'Kinsealy'),
    ('Knocklyon', 'Knocklyon'), ('Leopardstown', 'Leopardstown'),
    ('Loughlinstown', 'Loughlinstown'), ('Loughshinny', 'Loughshinny'),
    ('Lucan', 'Lucan'), ('Lusk', 'Lusk'),
    ('Malahide', 'Malahide'),('Marino', 'Marino'),
    ('Merrion', 'Merrion'),
    ('Milltown', 'Milltown'), ('Monkstown', 'Monkstown'),
    ('Mount-Merrion', 'Mount Merrion'),
    ('Mulhuddart', 'Mulhuddart'),
    ('Naul', 'Naul'), ('Navan-Road-d7', 'Navan Road'),
    ('Newcastle', 'Newcastle'), ('North-Circular-Road', 'North Circular Road'),
    ('North-Strand', 'North Strand'),
    ('North-Wall', 'North Wall'),
    ('Oldbawn', 'Oldbawn'), ('Ongar', 'Ongar'),
    ('Palmerstown', 'Palmerstown'), ('Park-West', 'Park West'),
    ('Perrystown', 'Perrystown'), ('Phibsborough', 'Phibsborough'), ('Poppintree', 'Poppintree'),
    ('Portmarnock', 'Portmarnock'), ('Portobello', 'Portobello'), ('Raheny', 'Raheny'),
    ('Ranelagh', 'Ranelagh'), ('Rathcoole', 'Rathcoole'), ('Rathfarnham', 'Rathfarnham'),
    ('Rathgar', 'Rathgar'), ('Rathmichael', 'Rathmichael'), ('Rathmines', 'Rathmines'),
    ('Rialto', 'Rialto'),
    ('Ringsend', 'Ringsend'), ('Rolestown', 'Rolestown'),
    ('Rush', 'Rush'), ('Saggart', 'Saggart'), ('Sallynoggin', 'Sallynoggin'),
    ('Sandycove', 'Sandycove'), ('Sandyford', 'Sandyford'), ('Sandymount', 'Sandymount'),
    ('Santry', 'Santry'), ('Shankill', 'Shankill'), ('Skerries', 'Skerries'),
    ('Smithfield', 'Smithfield'), ('South-Circular-Road', 'South-Circular-Road'),
    ('St-Margaret-s', 'St Margarets'),
    ('Stepaside', 'Stepaside'), ('Stillorgan', 'Stillorgan'), ('Stoneybatter', 'Stoneybatter'),
    ('Strawberry-Beds', 'Strawberry Beds'), ('Sutton', 'Sutton'),
    ('Swords', 'Swords'),
    ('Tallaght', 'Tallaght'), ('Temple-Bar', 'Temple Bar'),
    ('Templeogue', 'Templeogue'), ('Terenure', 'Terenure'),
    ('The-Coombe', 'The Coombe'), ('The-Ward', 'The Ward'),
    ('Ticknock', 'Ticknock'), ('Tyrrelstown', 'Tyrrelstown'),
    ('Walkinstown', 'Walkinstown'), ('Whitehall', 'Whitehall'),
    ('Windy-Arbour', 'Windy Arbour')
]

HOUSE_TYPE = [
    ('Any', 'Any'),
    ('Apartment', 'Apartment'),
    ('House', 'House'),
    ('Studio', 'Studio')
]

class PropertySearchForm(forms.Form):
    city = forms.CharField(label='Area', widget= forms.Select(choices = CITIES))
    house_type = forms.MultipleChoiceField(label='Property Type', required = False,
                                           widget=forms.CheckboxSelectMultiple, choices = HOUSE_TYPE)

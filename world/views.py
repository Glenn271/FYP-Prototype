from django.shortcuts import render, redirect
from .forms import PropertySearchForm
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import spacy


locations = [
    {
        'author': 'CoreyMS',
        'title': 'location 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'location 2',
        'content': 'Second post content',
        'date_posted': 'August 28, 2018'
    }
]


def home(request):
    context = {
        'locations': locations
    }
    return render(request, 'world/home.html', context)


def about(request):
    return render(request, 'world/about.html', {'title': 'About'})

#property search form
def search(request):
    context = {}
    prop_list = []

    if request.method == 'POST':
        form = PropertySearchForm(request.POST)

        if form.is_valid():
            city = form.cleaned_data['city']
            maxRent = form.cleaned_data['rent']

            #get housing data from myHome
            page = requests.get("https://www.myhome.ie/rentals/dublin/house-to-rent-in-{0}".format(city))
            soup = BeautifulSoup(page.content, 'html.parser')
            noProp = soup.find_all(class_="NoResultsCard py-5")
            propertyCard = soup.find_all(class_="PropertyListingCard")

            print(noProp)

            if noProp:
                context['noProp'] = True
                return render(request, 'world/search.html', context)

            else:
                #parsing content and assigning to variables
                for prop in propertyCard:
                    propList = prop
                    propAddress = propList.find(class_="PropertyListingCard__Address").get_text()
                    rentPrice = propList.find(class_="PropertyListingCard__Price").get_text()

                    try:
                        rentNumeric = re.search('€(.+?) ',rentPrice).group(1)
                    except AttributeError:
                        rentNumeric = ''

                    #using Nominatim for lat/lon info of property
                    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(propAddress) + '?format=json'
                    response = requests.get(url).json()

                    try:
                        lat = response[0]["lat"]
                        lon = response[0]["lon"]

                    #change this to have defaults
                    except:
                        lat = '53.350140'
                        lon = '-6.266155'

                    print(propAddress)
                    print(lat + " " + lon)

                    if maxRent != '' and rentNumeric != '':
                        rentNumeric = rentNumeric.replace(',','')
                        nlp = spacy.load("en_core_web_sm")

                        ideal_rent = int(maxRent)
                        actual_rent = int(rentNumeric)

                        diff = actual_rent - ideal_rent

                        if(diff <= 0 or diff <= (ideal_rent * 0.33)):
                            rent_sim = "High"
                        elif(diff > (ideal_rent * 0.33) and diff <= (ideal_rent * 0.67)):
                            rent_sim = "Medium"
                        elif(diff > (ideal_rent * 0.67)):
                            rent_sim = "Low"
                        else:
                            rent_sim = "Unknown"

                        # making JSON object for property data
                        property = {
                            'address': propAddress,
                            'city': city,
                            'lat': lat,
                            'lon': lon,
                            'rent': rentPrice,
                            'rent_sim' : rent_sim
                        }

                        prop_list.append(property)
                    else:
                        property = {
                            'address': propAddress,
                            'city': city,
                            'lat': lat,
                            'lon': lon,
                            'rent': rentPrice,
                            'rent_sim': "Unknown"
                        }
                        prop_list.append(property)

            #sort based on rent similarity
            prop_list.sort(key = lambda k : k['rent_sim'], reverse=True)

            print(prop_list[0])

            #context
            context['prop_list'] = prop_list
            context['form'] = form

            #search results if form is valid
            return render(request, 'world/results.html', context)

    else:
        form = PropertySearchForm()
    return render(request, 'world/search.html', {'form' : form})


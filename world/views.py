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
            houseType = form.cleaned_data['house_type']
            nlp = spacy.load("en_core_web_sm")

            #get housing data from myHome
            page = requests.get("https://www.myhome.ie/rentals/dublin/property-to-rent-in-{0}".format(city))
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

                    #property info
                    infoSpans = propList.find_all('span', {'class' : 'PropertyInfoStrip__Detail ng-star-inserted'})
                    infoLines = [span.get_text() for span in infoSpans]

                    print(infoLines)

                    beds = baths = house = 'N/A'
                    houseTypes = ['Apartment ', 'Terraced House ', 'Semi-Detached ',
                                  'Detached ', 'Bungalow ', 'Country House ', 'Studio ']

                    #assign values for prop info
                    for line in infoLines:
                        if ('bed' in line):
                            beds = line
                        if('bath' in line):
                            baths = line
                        if(line in houseTypes):
                            house = line

                    print(beds, baths, house)

                    #extract number from rent price p/m
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

                    #find default coords of city if difficulties finding address
                    except:
                        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(
                            city) + '?format=json'
                        response = requests.get(url).json()
                        lat = response[0]["lat"]
                        lon = response[0]["lon"]

                    print(propAddress)
                    print(lat + " " + lon)

                    if maxRent != '' and rentNumeric != '':
                        rentNumeric = rentNumeric.replace(',','')

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
                    else:
                        rent_sim = "Unknown"

                    house_sim = 0
                    #ideal vs actual house type
                    if houseType != '':
                        ideal_house = nlp(houseType)
                        actual_house = nlp(house)

                        house_sim = int(ideal_house.similarity(actual_house))
                        print(house_sim)


                    # making JSON object for property data
                    property = {
                        'address': propAddress,
                        'city': city,
                        'lat': lat,
                        'lon': lon,
                        'rent': rentPrice,
                        'rent_sim' : rent_sim,
                        'beds': beds,
                        'baths': baths,
                        'house': house,
                        'house_sim': house_sim
                    }

                    prop_list.append(property)


            #sort based on rent similarity
            prop_list.sort(key = lambda k : k['rent_sim'], reverse=True)

            #context
            context['prop_list'] = prop_list
            context['form'] = form

            #search results if form is valid
            return render(request, 'world/results.html', context)

    else:
        form = PropertySearchForm()
    return render(request, 'world/search.html', {'form' : form})


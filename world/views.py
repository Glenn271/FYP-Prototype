from django.shortcuts import render, redirect
from django.views.generic import ListView,DetailView
from .forms import PropertySearchForm
from .models import TestProperty
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import spacy


def home(request):
    return render(request, 'world/home.html')


def about(request):
    return render(request, 'world/about.html', {'title': 'About'})


class PropListView(ListView):
    model = TestProperty
    template_name = 'world/results.html'
    context_object_name = 'prop_list'


class PropDetailView(DetailView):
    model = TestProperty
    context_object_name = 'prop'


# #property search form
# def search(request):
#     context = {}
#     prop_list = []
#
#     if request.method == 'POST':
#         form = PropertySearchForm(request.POST)
#
#         if form.is_valid():
#             city = form.cleaned_data['city']
#             #maxRent = form.cleaned_data['rent']
#             maxRent = request.POST['rent']
#             houseType = form.cleaned_data['house_type']
#             nlp = spacy.load("en_core_web_sm")
#
#             #get housing data from myHome
#             page = requests.get("https://www.myhome.ie/rentals/dublin/property-to-rent-in-{0}".format(city))
#             soup = BeautifulSoup(page.content, 'html.parser')
#             noProp = soup.find_all(class_="NoResultsCard py-5")
#             propertyCard = soup.find_all(class_="PropertyListingCard")
#
#             print(noProp)
#
#             if noProp:
#                 context['noProp'] = True
#                 return render(request, 'world/search.html', context)
#
#             else:
#                 #parsing content and assigning to variables
#                 for prop in propertyCard:
#                     propList = prop
#                     propAddress = propList.find(class_="PropertyListingCard__Address").get_text()
#                     rentPrice = propList.find(class_="PropertyListingCard__Price").get_text()
#
#                     #property info
#                     infoSpans = propList.find_all('span', {'class' : 'PropertyInfoStrip__Detail ng-star-inserted'})
#                     infoLines = [span.get_text() for span in infoSpans]
#
#                     print(infoLines)
#
#                     beds = baths = house = 'N/A'
#                     houseTypes = ['Apartment ', 'Terraced House ', 'Semi-Detached ',
#                                   'Detached ', 'Bungalow ', 'Country House ', 'Studio ']
#
#                     #assign values for prop info
#                     for line in infoLines:
#                         if ('bed' in line):
#                             beds = line
#                         if('bath' in line):
#                             baths = line
#                         if(line in houseTypes):
#                             house = line
#
#                     house_sim = 0
#                     # ideal vs actual house type
#                     if houseType:
#                         for ideal_house in houseType:
#                             if ideal_house in house:
#                                 house_sim = 1
#                         print(house_sim)
#
#                     print(beds, baths, house)
#
#                     #extract number from rent price p/m
#                     try:
#                         rentNumeric = re.search('€(.+?) ',rentPrice).group(1)
#                     except AttributeError:
#                         rentNumeric = ''
#
#                     #using Nominatim for lat/lon info of property
#                     url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(propAddress) + '?format=json'
#                     response = requests.get(url).json()
#
#                     try:
#                         lat = response[0]["lat"]
#                         lon = response[0]["lon"]
#
#                     #find default coords of city if difficulties finding address
#                     except:
#                         url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(
#                             city) + '?format=json'
#                         response = requests.get(url).json()
#                         lat = response[0]["lat"]
#                         lon = response[0]["lon"]
#
#                     print(propAddress)
#                     print(lat + " " + lon)
#
#                     if maxRent != '' and rentNumeric != '':
#                         rentNumeric = rentNumeric.replace(',','')
#
#                         ideal_rent = int(maxRent)
#                         actual_rent = int(rentNumeric)
#
#                         diff = actual_rent - ideal_rent
#
#                         if(diff <= 0 or diff <= (ideal_rent * 0.33)):
#                             rent_sim = "High"
#                         elif(diff > (ideal_rent * 0.33) and diff <= (ideal_rent * 0.67)):
#                             rent_sim = "Medium"
#                         elif(diff > (ideal_rent * 0.67)):
#                             rent_sim = "Low"
#                         else:
#                             rent_sim = "Unknown"
#                     else:
#                         rent_sim = "Unknown"
#
#                     # making JSON object for property data
#                     property = {
#                         'address': propAddress,
#                         'city': city,
#                         'lat': lat,
#                         'lon': lon,
#                         'rent': rentPrice,
#                         'rent_sim' : rent_sim,
#                         'beds': beds,
#                         'baths': baths,
#                         'house': house,
#                         'house_sim': house_sim
#                     }
#
#                     prop_list.append(property)
#
#
#             #sort based on rent similarity
#             prop_list.sort(key = lambda k : k['rent_sim'], reverse=True)
#
#             #context
#             context['prop_list'] = prop_list
#             context['form'] = form
#
#             #search results if form is valid
#             return render(request, 'world/results.html', context)
#
#     else:
#         form = PropertySearchForm()
#     return render(request, 'world/search.html', {'form' : form})

def find_latest_info(city):
    search_props = []

    page = requests.get("https://www.myhome.ie/rentals/dublin/property-to-rent-in-{0}".format(city))
    soup = BeautifulSoup(page.content, 'html.parser')
    propertyCard = soup.find_all(class_="PropertyListingCard")

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

        # #extract number from rent price p/m
        # try:
        #     rentNumeric = int(re.search('€(.+?) ',rentPrice).group(1))
        # except AttributeError:
        #     rentNumeric = 0

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

        listing = TestProperty(address=propAddress, city = city, lat=lat,
                               lon = lon, rent=rentPrice, propertyType = house)

        listing.save()
        search_props.append(listing)

    return search_props


def search(request):
    context = {}
    prop_list = []

    if request.method == 'POST':
        form = PropertySearchForm(request.POST)

        if form.is_valid():
            city = form.cleaned_data['city']
            maxRent = request.POST['rent']
            houseType = form.cleaned_data['house_type']
            nlp = spacy.load("en_core_web_sm")

            search_props = TestProperty.objects.filter(city=city)

            if not search_props:
                search_props = find_latest_info(city)

            for prop in search_props:
                # making JSON object for property data
                property = {
                    'address': prop.address,
                    'city': prop.city,
                    'date_posted':prop.date_posted,
                    'lat': prop.lat,
                    'lon': prop.lon,
                    'rent': prop.rent,
                    'rent_sim' : 0,
                    'beds': 0,
                    'baths': 0,
                    'house': prop.propertyType,
                    'house_sim': 0
                }
                prop_list.append(property)

            #context
            context['prop_list'] = prop_list
            context['form'] = form

            #search results if form is valid
            return render(request, 'world/results.html', context)

    else:
        form = PropertySearchForm()
    return render(request, 'world/search.html', {'form' : form})
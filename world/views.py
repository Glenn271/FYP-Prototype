from django.shortcuts import render
from .forms import PropertySearchForm
import requests
from bs4 import BeautifulSoup
import urllib.parse
from django.views import generic
import json
from django.http import JsonResponse

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

def search(request):
    prop_list = []
    if request.method == 'POST':
        form = PropertySearchForm(request.POST)

        if form.is_valid():
            city = form.cleaned_data['city']

            #get city data from myHome
            page = requests.get("https://www.myhome.ie/rentals/dublin/house-to-rent-in-{0}".format(city))
            soup = BeautifulSoup(page.content, 'html.parser')
            propertyCard = soup.find_all(class_="PropertyListingCard")

            for prop in propertyCard:
                propList = prop
                propAddress = propList.find(class_="PropertyListingCard__Address").get_text()
                #print(propAddress)

                url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(propAddress) + '?format=json'
                response = requests.get(url).json()

                lat = response[0]["lat"]
                lon = response[0]["lon"]

                property = {
                    'address' : propAddress,
                    'city' : city,
                    'lat' : lat,
                    'lon' : lon
                }

                prop_list.append(property)
            # json_res = json.dumps(prop_list)
            # print(json_res)
            #
            # return render(request, 'world/results.html', {'json_res' : json_res})
            return JsonResponse({'prop_list':prop_list})

    else:
        form = PropertySearchForm()
    return render(request, 'world/search.html', {'form' : form})






from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from .forms import PropertySearchForm
from .models import Housing, UserFaves, Profile
from django.contrib.auth.models import User
import requests
from datetime import datetime
from django.utils import timezone
from bs4 import BeautifulSoup
import urllib.parse
import re
import overpy
import numpy as np
import json


def home(request):
    return render(request, 'world/home.html')


def about(request):
    return render(request, 'world/about.html', {'title': 'About'})


class PropDetailView(DetailView):
    model = Housing
    context_object_name = 'prop'


def addfave(request, pk):
    context = {}
    u = User.objects.get(username=request.user.username)
    p = Profile.objects.get(user=u)
    h = Housing.objects.get(id=pk)

    if not UserFaves.objects.filter(user=p, house=h).exists():
        uf = UserFaves(user=p, house=h)
        uf.save()

    context['user_faves'] = UserFaves.objects.filter(user = p)
    return render(request, 'users/profile.html', context)


def removefave(request, pk):
    context = {}
    u = User.objects.get(username=request.user.username)
    p = Profile.objects.get(user=u)
    h = Housing.objects.get(id=pk)
    uf = UserFaves.objects.filter(user=p, house=h)
    uf.delete()

    context['user_faves'] = UserFaves.objects.filter(user = p)
    return render(request, 'users/profile.html', context)


def find_latest_info(city):
    search_props = []

    page = requests.get("https://www.daft.ie/property-for-rent/{0}-dublin".format(city.lower()))
    soup = BeautifulSoup(page.content, 'html.parser')

    noProp = soup.find_all(class_="ZeroResults__Container-sc-193ko9u-2 UZhCx")
    print("noProp = " + str(noProp))

    # if no properties match search
    if noProp:
        return []

    #if properties are found
    else:
        propertyCard = soup.find_all(class_="SearchPage__Result-gg133s-2 itNYNv")

        for prop in propertyCard:
            try:
                propList = prop
                propAddress = propList.find(class_="TitleBlock__Address-sc-1avkvav-7 knPImU").get_text()
                rentPrice = propList.find(class_="TitleBlock__Price-sc-1avkvav-3 pJtsY").p.text

                # property info
                beds = propList.find("p", {"data-testid": "beds"}).get_text()
                baths = propList.find("p", {"data-testid": "baths"}).get_text()
                daftHouse = propList.find("p", {"data-testid": "property-type"}).get_text()

                osm_address = propAddress + " Ireland"
                osm_city = city + " Dublin Ireland"

                #using Nominatim for lat/lon info of property
                url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(osm_address) + '?format=json'
                response = requests.get(url).json()

                try:
                    lat = response[0]["lat"]
                    lon = response[0]["lon"]

                #find default coords of city if difficulties finding address
                except:
                    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(
                        osm_city) + '?format=json'
                    response = requests.get(url).json()
                    lat = response[0]["lat"]
                    lon = response[0]["lon"]

                print(propAddress)
                print(lat + " " + lon)

                bingSearch = "{0} site:daft.ie".format(propAddress)

                bingURL = "http://www.bing.com/images/search?q=" + bingSearch + "&FORM=HDRSC2"

                bingPage = requests.get(bingURL)

                b_soup = BeautifulSoup(bingPage.content, 'html.parser')

                try:
                    raw_image = b_soup.find("a", {"class": "iusc"})
                    m = json.loads(raw_image["m"])
                    turl = m["turl"]  # mobile image, desktop image
                except:
                    turl = "https://dummyimage.com/600x400/ffffff/000.png&text=Image+Coming+Soon"
                print(prop.address, turl)

                listing = Housing(address=propAddress, city = city, lat=lat,
                                       lon = lon, rent=rentPrice, beds = beds, baths = baths,
                                       propertyType = daftHouse, url=turl)

                listing.save()
                search_props.append(listing)
            except:
                print("Incompatible property")

    return search_props


def search(request):
    context = {}
    prop_list = []
    houseTypes = ['Apartment', 'House', 'Studio']

    if request.method == 'POST':
        form = PropertySearchForm(request.POST)

        context['form'] = form

        if form.is_valid():
            city = form.cleaned_data['city']
            maxRent = request.POST['rent']
            rentPriority = request.POST['rent_priority']
            housePriority = request.POST['house_priority']
            houseType = form.cleaned_data['house_type']

            if not houseType or 'Any' in houseType:
                housePriority = 0

            print(city)
            print(rentPriority, housePriority, houseType)

            weights = np.array([rentPriority, housePriority]).astype(np.float)
            weight_sum = np.sum(weights)
            print(weights, weight_sum)

            balanced = weights/weight_sum
            print(balanced)

            #check if balanced to 1
            total_balanced = np.sum(balanced)
            print(total_balanced)

            rent_weight = balanced[0]
            house_weight = balanced[1]


            search_props = Housing.objects.filter(city=city)

            if not search_props:
                search_props = find_latest_info(city)
                # print(search_props)

            # else:
            #     last_updated = datetime.strftime(search_props[0].date_posted, '%d-%m-%Y')
            #     time_now = datetime.strftime(timezone.now(), '%d-%m-%Y')
            #
            #     print(last_updated, time_now)
            #
            #     if last_updated != time_now:
            #         TestProperty.objects.filter(city=city).delete()
            #         search_props = find_latest_info(city)

            if not search_props:
                context['noProp'] = True
                return render(request, 'world/search.html', context)

            else:
                for prop in search_props:
                    #extract number from rent price p/m
                    try:
                        rentNumeric = re.search('€(.+?) ',prop.rent).group(1)
                        rentNumeric = rentNumeric.replace(',', '')
                    except AttributeError:
                        rentNumeric = 0

                    ideal_rent = int(maxRent)
                    actual_rent = int(rentNumeric)

                    print ("Ideal vs Actual " + str(ideal_rent) + " " + str(actual_rent))
                    rent_sim = 0
                    house_sim = 0

                    if actual_rent != 0:
                        # score based on proportion of ideal to actual rent
                        # this takes every property price into account, as opposed to manual classing
                        diff = float(ideal_rent/actual_rent)
                        rent_sim = diff

                        # diff = actual_rent - ideal_rent
                        #
                        # if (diff <= 0):
                        #     rent_sim = 1 *
                        # elif (diff > 0 and diff <= (ideal_rent * 0.33)):
                        #     rent_sim = 0.8
                        # elif(diff > (ideal_rent * 0.33) and diff <= (ideal_rent * 0.67)):
                        #     rent_sim = 0.5
                        # else:
                        #     rent_sim = 0

                    # ideal vs actual house type
                    for house in houseType:
                        if house in houseTypes or house == "Any":
                            house_sim = 1

                    rent_weighted = float(rent_sim * float(rent_weight))
                    house_weighted = float(house_sim * float(house_weight))

                    total_sim = rent_weighted + house_weighted

                    #check if property already in favourites
                    u = User.objects.get(username=request.user.username)
                    p = Profile.objects.get(user=u)
                    h = Housing.objects.get(id=prop.id)

                    if UserFaves.objects.filter(user=p, house=h).exists():
                        in_favourites = True
                    else:
                        in_favourites = False

                    # making JSON object for property data
                    property = {
                        'id' : prop.id,
                        'address': prop.address,
                        'city': prop.city,
                        'date_posted':prop.date_posted,
                        'lat': prop.lat,
                        'lon': prop.lon,
                        'rent': prop.rent,
                        'rent_sim' : rent_sim,
                        'rent_eur' : actual_rent,
                        'beds': prop.beds,
                        'baths': prop.baths,
                        'house': prop.propertyType,
                        'house_sim': house_sim,
                        'total_sim' : total_sim,
                        'in_favourites': in_favourites,
                        'url': prop.url
                    }

                    prop_list.append(property)

                if housePriority == 0:
                    prop_list.sort(key=lambda k: k['rent_eur'], reverse=False)
                else:
                    prop_list.sort(key=lambda k: k['total_sim'], reverse=True)


                #context
                context['prop_list'] = prop_list
                context['form'] = form

                #search results if form is valid
                return render(request, 'world/search.html', context)

    else:
        form = PropertySearchForm()
    return render(request, 'world/search.html', {'form' : form})


def overpass_test(request):
    context = {}

    radius = float(request.POST['radius'])
    radius *= 1000
    lat = request.POST['lat']
    lon = request.POST['lon']

    print(radius,lat, lon)

    amenity_list = get_amenities(radius, lat, lon)

    source = {
        'lat' : lat,
        'lon' : lon,
        'radius' : radius
    }

    context['amenity_list'] = amenity_list
    context['source'] = source
    return render(request, 'world/amenities.html', context)


def get_amenities(radius, lat, lon):
    amenity_list = []
    api = overpy.Overpass()

    #get overpass amenities
    query = ("""
                (
                  node["amenity"](around:{0},{1}, {2});
                  way["amenity"](around:{0},{1}, {2});
                  node["shop"](around:{0},{1}, {2});
                  way["shop"](around:{0},{1}, {2});
                );
                out center;
                >;
            """).format(radius, lat, lon)
    result = api.query(query)

    for node in result.nodes:
        amenity = node.tags.get("amenity", "n/a")
        shop = node.tags.get("shop", "n/a")
        name = node.tags.get("name", "n/a")

        amenity_or_shop = " "

        if amenity == "n/a" and shop != "n/a":
            amenity_or_shop = shop
            amenity_display_name = shop.replace("_", " ")
            amenity_display_name = amenity_display_name.title()

        else:
            amenity_or_shop = amenity
            amenity_display_name = amenity.replace("_", " ")
            amenity_display_name = amenity_display_name.title()

        print(amenity_or_shop, name, node.lat, node.lon)

        area_amenity = {
            'amenity' : amenity_or_shop,
            'amenity_display_name' : amenity_display_name,
            'name' : name,
            'lat' : node.lat,
            'lon' : node.lon
        }

        amenity_list.append(area_amenity)

    for way in result.ways:
        amenity = way.tags.get("amenity", "n/a")
        shop = way.tags.get("shop", "n/a")
        name = way.tags.get("name", "n/a")

        amenity_or_shop = " "

        if amenity == "n/a" and shop != "n/a":
            amenity_or_shop = shop
            amenity_display_name = shop.replace("_", " ")
            amenity_display_name = amenity_display_name.title()

        else:
            amenity_or_shop = amenity
            amenity_display_name = amenity.replace("_", " ")
            amenity_display_name = amenity_display_name.title()

        print(amenity_or_shop, name, node.lat, node.lon)

        area_amenity = {
            'amenity': amenity_or_shop,
            'amenity_display_name': amenity_display_name,
            'name': name,
            'lat': node.lat,
            'lon': node.lon
        }

        amenity_list.append(area_amenity)

    return amenity_list
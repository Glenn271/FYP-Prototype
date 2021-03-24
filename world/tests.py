from django.test import TestCase
from world.models import Housing
from world.forms import PropertySearchForm

# Creating tests for World app
class HousingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Housing.objects.create(address="2 Kilcarberry Close", city = "Clondalkin", lat=53.3182422,
                                       lon = -6.4167325, rent="€2,000 p/m", beds = "3 bed", baths = "2 bath",
                                       propertyType = "House", url="https://dummyimage.com/600x400/ffffff/000.png&text=Image+Coming+Soon")

    # check if house object _str_ method returns address
    def test_object_name(self):
        house = Housing.objects.get(address="2 Kilcarberry Close")
        expected_name = house.address
        self.assertEqual(expected_name, str(house))

   # checking configuration for get_absolute_url method is correct
    def test_get_absolute_url(self):
        house = Housing.objects.get(address="2 Kilcarberry Close")
        self.assertEqual(house.get_absolute_url(), '/results/{}/'.format(house.id))


    # check if url field max length is 300, so it's large enough to store URLs for house images
    def test_url_max_length(self):
        house = Housing.objects.get(address="2 Kilcarberry Close")
        max_length = house._meta.get_field('url').max_length
        self.assertEqual(max_length, 300)


# testing property search form
class PropertySearchFormTest(TestCase):

    #test if label for area field is correct
    def test_area_label(self):
        form = PropertySearchForm()
        self.assertTrue(form.fields['city'].label == "Area")

    # test if label for property type field is correct
    def test_property_label(self):
        form = PropertySearchForm()
        self.assertTrue(form.fields['house_type'].label == "Property Type")

    # as city is a required field, it should return false if nothing is entered
    def test_area_filled(self):
        form = PropertySearchForm(data={'city':None})
        self.assertFalse(form.is_valid())

    # check that only house types available are entered for property type
    def test_property_options(self):
        house_types = ['Any', 'Apartment', 'House', 'Studio']
        entry = 'Palace'
        form = PropertySearchForm(data={'house_type': entry})

        if entry not in house_types:
            self.assertFalse(form.is_valid())

        else:
            self.assertTrue(form.is_valid())


# testing the view for loading templates
class WorldViewTesting(TestCase):
    @classmethod
    def setUpTestData(cls):
        Housing.objects.create(address="1 Kilcarberry Close", city="Clondalkin", lat=53.3182422,
                               lon=-6.4167325, rent="€2,000 p/m", beds="3 bed", baths="2 bath",
                               propertyType="House",
                               url="https://dummyimage.com/600x400/ffffff/000.png&text=Image+Coming+Soon")

    # check the home page loads with configured url
    def test_home_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    # check that about page loads with configured url
    def test_about_page(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    # check that search page loads with configured url
    def test_search_page(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)

    # check if created property has a detail view created successfully
    def test_PropDetailView(self):
        house = Housing.objects.get(address="1 Kilcarberry Close")
        response = self.client.get('/results/{}/'.format(house.id))
        self.assertEqual(response.status_code, 200)

























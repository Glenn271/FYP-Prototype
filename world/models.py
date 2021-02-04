from django.contrib.gis.db import models
from django.utils import timezone

class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2, null=True)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name

#storing property information
class TestProperty(models.Model):
    address = models.CharField(max_length=100) #address of property
    city = models.CharField(max_length=100) #city
    lon = models.FloatField()
    lat = models.FloatField()
    date_posted = models.DateTimeField(default=timezone.now) #date the listing was added to db
    rent = models.IntegerField() #rent price
    propertyType = models.CharField(max_length=100) #type of house (apartment, bungalow etc)

    def __str__(self):
        return self.address




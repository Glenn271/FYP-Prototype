from django.contrib.gis import admin
from .models import WorldBorder, Property

admin.site.register(WorldBorder, admin.GeoModelAdmin)
admin.site.register(Property, admin.OSMGeoAdmin)



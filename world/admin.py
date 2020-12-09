from django.contrib.gis import admin
from .models import WorldBorder, Prop

admin.site.register(WorldBorder, admin.GeoModelAdmin)
admin.site.register(Prop, admin.OSMGeoAdmin)



from django.contrib.gis import admin
from .models import WorldBorder, TestProperty

admin.site.register(WorldBorder, admin.GeoModelAdmin)
admin.site.register(TestProperty)



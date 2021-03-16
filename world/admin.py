from django.contrib.gis import admin
from .models import WorldBorder, TestProperty, Housing

admin.site.register(WorldBorder, admin.GeoModelAdmin)
admin.site.register(TestProperty)
admin.site.register(Housing)



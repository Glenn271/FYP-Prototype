from django.contrib.gis import admin
from .models import WorldBorder, TestProperty, Housing, UserFaves

admin.site.register(WorldBorder, admin.GeoModelAdmin)
admin.site.register(TestProperty)
admin.site.register(Housing)
admin.site.register(UserFaves)



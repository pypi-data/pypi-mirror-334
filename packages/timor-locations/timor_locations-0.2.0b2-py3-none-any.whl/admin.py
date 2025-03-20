from django.contrib.gis import admin

from timor_locations import models


@admin.register(models.Municipality, models.AdministrativePost, models.Suco)
class AreaAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TopoJson)
class TopoJSONAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin
from sky import models

class SkyObjectAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'direction')

class DirectionAdmin(admin.ModelAdmin):
    ordering = ('ra','dec',)

admin.site.register(models.SkyObject, SkyObjectAdmin)
admin.site.register(models.Direction, DirectionAdmin)
#admin.site.register(models.Cluster)

from django.contrib import admin

from . import models


admin.site.register(models.WorkType)
admin.site.register(models.ArtType)
admin.site.register(models.Iguala)
admin.site.register(models.ArtIguala)
admin.site.register(models.Status)
admin.site.register(models.Work)
admin.site.register(models.ArtWork)
admin.site.register(models.File)
admin.site.register(models.WorkDesigner)
admin.site.register(models.StatusChange)

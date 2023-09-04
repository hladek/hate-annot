from django.contrib import admin
from . import models

admin.site.register(models.Batch)
admin.site.register(models.Question)
admin.site.register(models.Annotation)

# Register your models here.

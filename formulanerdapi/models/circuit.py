from django.db import models
from .nation import Nation
class Circuit(models.Model):
  name = models.CharField(max_length=75)
  nation = models.ForeignKey(Nation, on_delete=models.CASCADE, null=True, blank=True)
  length = models.CharField(max_length=50)
  circuit_type = models.CharField(max_length=50)
  designer = models.CharField(max_length=50)
  year_built = models.IntegerField(null=True, blank=True)
  circuit_image_url = models.URLField(max_length=255)

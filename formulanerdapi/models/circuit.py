from django.db import models

class Nation(models.Model):
    name = models.CharField(max_length=100)
class Circuit(models.Model):
  name = models.CharField(max_length=75)
  nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
  length = models.CharField(max_length=50)
  circuit_type = models.CharField(max_length=50)
  designer = models.CharField(max_length=50)
  year_built = models.IntegerField()
  circuit_image_url = models.URLField(max_length=255)

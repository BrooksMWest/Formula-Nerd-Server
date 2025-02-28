from django.db import models

class Nation(models.Model):
    name = models.CharField(max_length=100)
class Constructor(models.Model):
  name = models.CharField(max_length=75)
  location = models.CharField(max_length=50)
  nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
  is_engine_manufacturer = models.BooleanField()
  about = models.CharField(max_length=255)
  constructor_image_url = models.URLField()

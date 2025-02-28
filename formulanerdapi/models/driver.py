from django.db import models

class Nation(models.Model):
    name = models.CharField(max_length=100)

class Constructor(models.Model):
    name = models.Charfield(max_length=100)
class Driver(models.Model):
  name = models.CharField(max_length=75)
  age = models.IntField(max_length=3)
  gender = models.CharField(max_length=50)
  nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
  current_constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE)
  about = models.TextField()
  driver_image_url = models.URLField()

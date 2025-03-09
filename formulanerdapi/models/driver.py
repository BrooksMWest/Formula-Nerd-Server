from django.db import models
from .nation import Nation
from .constructor import Constructor
class Driver(models.Model):
  name = models.CharField(max_length=75)
  age = models.IntegerField(null=True)
  gender = models.CharField(max_length=50)
  nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
  current_constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE)
  about = models.TextField()
  driver_image_url = models.URLField()

from django.db import models
from .driver import Driver
from .constructor import Constructor

class DriverConstructorHistory(models.Model):
  
  driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
  constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE)
  start_year = models.IntegerField(max_length=4)
  end_year = models.IntegerField(max_length=4)

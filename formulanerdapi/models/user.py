from django.db import models
from .nation import Nation
from .driver import Driver
from .circuit import Circuit

class User(models.Model):

  uid = models.CharField(max_length=125, unique=True)  
  name = models.CharField(max_length=75)
  nation = models.ForeignKey(Nation, on_delete=models.SET_NULL, null=True, blank=True)
  favorite_driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
  favorite_circuit = models.ForeignKey(Circuit, on_delete=models.SET_NULL, null=True, blank=True)

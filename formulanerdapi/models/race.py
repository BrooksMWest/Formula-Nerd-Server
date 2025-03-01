from django.db import models
from .nation import Nation
from .driver import Driver
from .circuit import Circuit
class Race(models.Model):
  name = models.CharField(max_length=75)
  circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
  date = models.DateField()
  nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
  distance = models.CharField(max_length=25)
  laps = models.IntegerField()
  winner_driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
  p2_driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
  p3_driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

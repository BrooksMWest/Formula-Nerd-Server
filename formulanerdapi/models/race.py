from django.db import models

class Nation(models.Model):
    name = models.CharField(max_length=100)

class Driver(models.Model):
    name = models.CharField(max_length=75)

class Race(models.Model):
  name = models.CharField(max_length=75)
  circuit = models.CharField(max_length=50)
  date = models.DateField()
  nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
  distance = models.CharField(max_length=25)
  laps = models.IntegerField()
  winner_driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
  p2_driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
  p3_driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

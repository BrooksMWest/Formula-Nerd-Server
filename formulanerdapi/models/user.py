from django.db import models

class Nation(models.Model):
    name = models.CharField(max_length=100)

class Driver(models.Model):
    name = models.CharField(max_length=75)

class User(models.Model):

  uid = models.CharField(max_length=125)  
  name = models.CharField(max_length=75)
  nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
  favorite_driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
  favorite_circuit = models.ForeignKey(Driver, on_delete=models.CASCADE)

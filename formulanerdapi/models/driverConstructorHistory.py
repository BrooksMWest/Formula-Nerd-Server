from django.db import models

class Driver(models.Model):
    name = models.CharField(max_length=100)

class Constructor(models.Model):
    name = models.Charfield(max_length=100)

class DriverConstructorHistory(models.Model):
  
  driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
  constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE)
  start_year = models.IntField(max_length=4)
  end_year = models.IntField(max_length=4)

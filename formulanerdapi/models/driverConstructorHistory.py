from django.db import models
from .driver import Driver
from .constructor import Constructor
from django.core.exceptions import ValidationError


class DriverConstructorHistory(models.Model):
  
  driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
  constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE)
  start_year = models.IntegerField()
  end_year = models.IntegerField(null=True, blank=True)

  def clean(self):
        if self.end_year and self.end_year < self.start_year:
            raise ValidationError("End year cannot be before start year.")

  def save(self, *args, **kwargs):
      self.clean()
      super().save(*args, **kwargs)

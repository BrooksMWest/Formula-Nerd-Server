from django.db import models

class Nation(models.Model):
    
  name = models.CharField(max_length=75)
  flag_image_url = models.URLFieldField()

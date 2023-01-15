from django.db import models

# Create your models here.
class Tag(models.Model):
  name = models.CharField(max_length=32, primary_key=True)

  def __str__(self):
    return self.name

class Photo(models.Model):
  image = models.ImageField(null=False, blank=False, upload_to="uploads/")
  description = models.TextField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  tags = models.ManyToManyField(Tag, blank=True)
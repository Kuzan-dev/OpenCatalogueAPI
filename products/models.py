from django.db import models
import uuid

def product_image_path(instance, filename):
    # Usa una ruta predeterminada temporal
    return f"product/temp/{filename}"

# Create your models here.
class Image(models.Model):
    file = models.ImageField(upload_to=product_image_path)

    def __str__(self):
      return self.file.name
  

class Product(models.Model):
  identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  name = models.CharField(max_length=255)
  link = models.URLField()
  description = models.TextField(("Description"), blank=True)
  images = models.ManyToManyField('Image', related_name='product')
  
  def __str__(self):
    return self.name

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
  rating = models.FloatField(default=0)
  delivery = models.TextField(("Delivery"), blank=True)
  stock = models.IntegerField(default=0)
  available = models.BooleanField(default=True)
  description = models.TextField(("Description"), blank=True)
  images = models.ManyToManyField('Image', related_name='product')
  tags = models.ManyToManyField('Tag', related_name='product')
  prices = models.ManyToManyField('Price', related_name='product')
  
  def __str__(self):
    return self.name

class Material(models.Model):
  name = models.CharField(max_length=255)
  def __str__(self):
    return self.name

class Price(models.Model):
  description = models.TextField(("Description"), blank=True)
  price = models.FloatField()
  material = models.ForeignKey(Material, related_name='prices', on_delete=models.CASCADE)
  def __str__(self):
    return self.description
   
class Tag(models.Model):
  name = models.CharField(max_length=255)
  def __str__(self):
    return self.name
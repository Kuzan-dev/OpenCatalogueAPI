from django.db import models
from django.utils.translation import gettext_lazy as _
from uuid import uuid4

def product_image_path(instance, filename):
  return f"product/{instance.product.name}/{filename}"

def get_unique_filename(filename):
    extension = filename.split('.')[-1]
    unique_filename = f"{uuid4().hex}.{extension}"
    return unique_filename

# Create your models here.
class Image (models.Model):
  file = models.ImageField(upload_to=product_image_path)
  product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE)

  def __str__(self):
    return self.file.name
  
  def save(self, *args, **kwargs):
    if self.file:
      self.file.name = get_unique_filename(self.file.name)
    super().save(*args, **kwargs)
  

class Material(models.Model):
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name

class Price(models.Model):
  description = models.TextField()
  price = models.FloatField()
  material = models.ForeignKey(Material, on_delete=models.CASCADE)

  def __str__(self):
    return self.description

class Tag(models.Model):
  name = models.CharField(max_length=255)
  
  def __str__(self):
    return self.name


class Product(models.Model):
  name = models.CharField(max_length=255)
  description = models.TextField(_("Description"), blank=True)
  link = models.URLField()
  rating = models.FloatField()
  delivery = models.TextField()
  stock = models.IntegerField(default=0)
  available = models.BooleanField(default=True)
  tags = models.ManyToManyField('Tag', related_name='products')
  prices = models.ManyToManyField('Price', related_name='products')

  def __str__(self):
    return self.title

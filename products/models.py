from django.db import models
from django.core.files.base import ContentFile
from PIL import Image as PILImage, Image
from io import BytesIO
import uuid

def product_image_path(instance, filename):
    # Usa una ruta predeterminada temporal
    return f"product/temp/{filename}"

def compress_image(image_file, max_size=(900,900), quality=85):
  #Crea yba instancia de Pillow Image
  image = PILImage.open(image_file)

  # Redimensiona la imagen
  image.thumbnail(max_size, PILImage.Resampling.LANCZOS)
  
  # Guarda la imagen comprimida en un buffer
  buffer = BytesIO() # Crea un buffer de memoria
  image.save(buffer, format=image.format, quality=quality, optimize=True) # Guarda la imagen en el buffer
  buffer.seek(0)# Mueve el cursor al inicio del buffer

  return buffer

# Create your models here.
class Image(models.Model):
    file = models.ImageField(upload_to=product_image_path)
    is_ready = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.is_ready and self.file:
            compressed_image = compress_image(self.file)
            self.file = ContentFile(compressed_image.read(), name=self.file.name)
            # Guardar el objeto con una versión comprimida y establecer el estado en is_ready
            super().save(*args, **kwargs)
            self.is_ready = True
            # Actualizar el estado en is_ready sin guardar nuevamente
            kwargs['force_update'] = True
        else:
            super().save(*args, **kwargs)

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
  material = models.ForeignKey(Material, related_name='prices', on_delete=models.CASCADE, default= 1)
  def __str__(self):
    return self.description
   
class Tag(models.Model):
  name = models.CharField(max_length=255)
  def __str__(self):
    return self.name
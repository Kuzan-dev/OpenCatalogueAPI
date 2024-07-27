from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.conf import settings
import os
from .models import Product, Image
import logging
import time

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Image)
def update_image_status(sender, instance, created, **kwargs):
  if created:
    instance.is_ready = True
    instance.save()

def move_image(file, new_path, max_retries=5, wait_time=0.5):
    old_path = file.name
    old_full_path = default_storage.path(old_path)
    new_full_path = default_storage.path(new_path)
    
    # Verificar si el archivo ya ha sido movido
    if default_storage.exists(new_full_path):
        logger.info(f"El archivo ya ha sido movido a: {new_path}")
        return
    
    logger.info(f"Ruta completa del archivo: {old_full_path}")
    logger.info(f"Moviendo archivo: {old_full_path} a {new_full_path}")

    attempt = 0
    while attempt < max_retries:
        if default_storage.exists(old_path):
            try:
                with default_storage.open(old_path, 'rb') as src:
                    file_content = src.read()
                
                os.makedirs(os.path.dirname(new_full_path), exist_ok=True)

                with default_storage.open(new_path, 'wb') as dst:
                    dst.write(file_content)

                default_storage.delete(old_path)
                logger.info(f"Imagen movida a: {new_path}")
                return  # Éxito, salir de la función
            except Exception as e:
                logger.error(f"Error moviendo el archivo en el intento {attempt + 1}: {e}")
                # Intenta nuevamente si ocurre una excepción durante el movimiento
        else:
            logger.error(f"Archivo no encontrado en el intento {attempt + 1}: {old_path}")
            time.sleep(wait_time)  # Espera antes de volver a intentar
        attempt += 1

    logger.error(f"Error moviendo el archivo después de {max_retries} intentos: {old_path}")

def move_product_images(instance):

  images = instance.images.filter(is_ready=True)# Obtiene todas las imágenes asociadas al producto

  logger.info(f"Imágenes asociadas con el producto {instance.name} : {[image.file.name for image in images]}") # Registra las imágenes asociadas
  
  for image in images:
    #Define la nueva ruta de la imagen
    new_path = f"product/{instance.identifier}/images/{image.id}{os.path.splitext(image.file.name)[1]}"
    move_image(image.file, new_path)

@receiver(post_save, sender=Product)
def move_product_images_on_save(sender, instance, created, **kwargs):
  if created:
    try:
      move_product_images(instance)
    except Exception as e:
      logger.error(f"Error moviendo las imágenes del producto {instance.name}: {e}")


@receiver(m2m_changed, sender=Product.images.through)
def move_product_images_on_change(sender, instance, action, **kwargs):

  if action in ['post_add', 'post_remove']:
    try:
      move_product_images(instance)
    except Exception as e:
      logger.error(f"Error moviendo las imágenes del producto {instance.name}: {e}")
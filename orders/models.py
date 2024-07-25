from django.db import models

# Create your models here.
class Order(models.Model):
  
  completed = models.BooleanField(default=False)

  def __str__(self):
    return f"Order {self.id}"

  
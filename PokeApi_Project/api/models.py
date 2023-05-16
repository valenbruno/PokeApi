from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Pokemon(models.Model):
    nombre=models.CharField(max_length=50)
    tipo=models.CharField(max_length=50)
    naturaleza=models.CharField(max_length=50)
    peso=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    ataque=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(100)])

    class Meta:
        verbose_name="Pokemon"
        ordering = ["nombre"]
        verbose_name_plural ="Pokemones"
    def __str__(self):
        return self.nombre

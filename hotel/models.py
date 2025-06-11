
from django.db import models
from django.contrib.auth.models import User

class Quarto(models.Model):
    NUM_TIPO = [
        ('Solteiro', 'Solteiro'),
        ('Duplo', 'Duplo'),
        ('Luxo', 'Luxo'),
    ]
    STATUS_CHOICES = [
        ('Disponível', 'Disponível'),
        ('Reservado', 'Reservado'),
    ]

    numero = models.PositiveIntegerField(unique=True)
    tipo = models.CharField(max_length=20, choices=NUM_TIPO)
    capacidade = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Disponível')

    def __str__(self):
        return f"Quarto {self.numero} - {self.tipo} - {self.status}"

class Reserva(models.Model):
    quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE)
    hospede_nome = models.CharField(max_length=100)
    data_reserva = models.DateTimeField(auto_now_add=True)
    reservado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Reserva: {self.hospede_nome} no quarto {self.quarto.numero}"

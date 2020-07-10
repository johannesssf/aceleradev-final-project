from django.core.validators import MinLengthValidator
from django.db import models


class User(models.Model):
    email = models.EmailField('e-mail')
    password = models.CharField(
        'password',
        max_length=50,
        validators=[MinLengthValidator(8)]
    )

    def __str__(self):
        return self.email

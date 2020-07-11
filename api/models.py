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


class Record(models.Model):
    REC_CHOICES = (
        ('error', 'ERROR'),
        ('info', 'INFO'),
        ('debug', 'DEBUG'),
        ('warning', 'WARNING'),
        ('critical', 'CRITICAL'),
    )
    environment = models.CharField('Environment', max_length=30)
    level = models.CharField('Level', max_length=10, choices=REC_CHOICES)
    message = models.CharField('Message', max_length=200)
    origin = models.GenericIPAddressField('Origin', protocol='IPv4')
    date = models.DateTimeField('Date')
    is_archived = models.BooleanField('Is archived')
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return "{} [{}][{}] {}: {}".format(
            self.date.strftime('%Y-%m-%d %H:%M:%S'),
            self.level,
            self.origin,
            self.environment,
            self.message
        )

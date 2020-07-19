from django.contrib.auth.models import User
from django.db import models


class Record(models.Model):
    """Represents the model of how the error information is recorded into
    the system.
    """

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
    events = models.IntegerField('Events')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{} [{}][{}][{}] {}: {}".format(
            self.date.strftime('%Y-%m-%d %H:%M:%S'),
            self.level,
            self.origin,
            self.environment,
            self.events,
            self.message
        )

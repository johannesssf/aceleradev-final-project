from hashlib import sha256

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator
from django.db import models


class UserManager(BaseUserManager):
    """Mandatory class when using a custom user.
    """
    list_display = ('email', 'password')

    def create_user(self, email, password):
        User.objects.create(email=email, password=password)

    def create_superuser(self, email, password):
        self.create_user(email, password)

    def get_by_natural_key(self, email):
        return User.objects.get(email=email)


class User(AbstractBaseUser):
    """Represents the API users and substitutes the default Django User.

    The email field is used to authenticate users into the system and
    the password field is encrypted before being saved using sha256 hash
    algorithm.
    """
    email = models.EmailField('e-mail', unique=True)
    password = models.CharField(
        'password',
        max_length=100,
        validators=[MinLengthValidator(8)]
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('password',)
    objects = UserManager()

    def save(self, *args, **kwargs):
        """Overrides super's method to add password cryptography.
        """
        self.password = sha256(self.password.encode()).hexdigest()
        super().save(*args, **kwargs)

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

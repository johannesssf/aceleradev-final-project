from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MinLengthValidator
from django.db import models


class UserManager(BaseUserManager):
    """Mandatory class when using a custom user.
    """
    def _create_user(self, email, password, is_staff, is_superuser):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password):
        return self._create_user(email, password, False, False)

    def create_superuser(self, email, password):
        return self._create_user(email, password, True, True)

    def get_by_natural_key(self, email):
        return User.objects.get(email=email)


class User(AbstractBaseUser, PermissionsMixin):
    """Represents the API users and substitutes the default Django User.
    """
    email = models.EmailField('e-mail', unique=True)
    password = models.CharField(
        'password',
        max_length=100,
        validators=[MinLengthValidator(8)]
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('password',)
    objects = UserManager()

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

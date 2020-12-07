from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, screen_name, twitter_id, is_protected, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not screen_name:
            raise ValueError('The given username must be set')
        user = self.model(screen_name=screen_name, **extra_fields)
        user.password = make_password(password)
        user.twitter_id = twitter_id
        user.is_protected = is_protected
        user.save(using=self._db)
        return user

    def create_user(self, screen_name, twitter_id=0, is_protected=False, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(screen_name, twitter_id, is_protected, password, **extra_fields)

    def create_superuser(self, screen_name, twitter_id=0, is_protected=False, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(screen_name, twitter_id, is_protected, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    screen_name = models.CharField(
        'screen name',
        unique=True,
        max_length=50,
    )
    twitter_id = models.BigIntegerField(
        'Twitter id',
        unique=True,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_protected = models.BooleanField(
        default=False
    )
    access_token = models.CharField(
        'Access token',
        max_length=100
    )
    access_token_secret = models.CharField(
        'Access token secret',
        max_length=100
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'screen_name'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()

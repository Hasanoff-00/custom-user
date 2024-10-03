from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "admin"
        MANAGER = "manager"
        SHOP_OWNER = "shop_owner"
        CUSTOMER = "customer"

    guid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        null=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    phone = models.CharField(
        max_length=12,
        unique=True,
        null=True,
    )
    full_name = models.CharField(max_length=255, null=True)
    image = models.ImageField(
        upload_to="users/",
        null=True,
        blank=True,
    )
    address = models.TextField()
    role = models.CharField(
        choices=Role.choices,
        max_length=10,
        default=Role.CUSTOMER,
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        if self.username is not None:
            return self.username
        if self.full_name is not None:
            return self.full_name
        if self.phone is not None:
            return self.phone

    class Meta:
        db_table = "users"
        verbose_name = _("user")
        verbose_name_plural = _("users")

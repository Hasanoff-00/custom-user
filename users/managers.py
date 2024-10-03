from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def _create_user(self, password, phone=None, username=None, **extra_fields):
        # Telefon yoki username bo'lmasa xatolik chiqariladi
        if phone is None and username is None:
            raise ValidationError("The given phone or username must be set")

        # Agar username bo'lmasa, telefon orqali foydalanuvchi yaratadi
        if username is None:
            user = self.model(phone=phone, **extra_fields)
        else:
            # Agar username bo'lsa, username orqali foydalanuvchi yaratadi
            user = self.model(username=username, **extra_fields)

        # Parolni o'rnatadi va foydalanuvchini saqlaydi
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, **extra_fields):
        # Foydalanuvchi odatda staff va superuser bo'lmaydi
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        # Telefon va username ni extra_fields dan olib tashlaydi
        phone = extra_fields.pop("phone", None)
        username = extra_fields.pop("username", None)
        password = extra_fields.pop("password")

        # `_create_user` yordamida foydalanuvchi yaratadi
        return self._create_user(phone=phone, username=username, password=password, **extra_fields)

    def create_superuser(self, password, phone=None, username=None, **extra_fields):
        # Superuser bo'lishi uchun staff va superuser statuslarini true qilib o'rnatadi
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", self.model.Role.ADMIN)

        # Agar superuserda is_staff yoki is_superuser false bo'lsa, xatolik chiqariladi
        if extra_fields.get("is_staff") is not True:
            raise ValidationError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValidationError("Superuser must have is_superuser=True.")

        # Superuser yaratish uchun `_create_user` dan foydalanadi
        return self._create_user(phone=phone, username=username, password=password, **extra_fields)
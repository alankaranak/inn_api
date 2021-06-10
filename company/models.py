from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class Company(models.Model):
    """Представляет модель компании."""

    inn = models.CharField(verbose_name="ИНН", unique=True, max_length=13)
    name = models.CharField(verbose_name="Наименование компании", max_length=150)
    address = models.CharField(verbose_name="Адрес", max_length=150)
    nol = models.PositiveIntegerField(verbose_name="Количество лицензий", default=0)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def checkout_inn(cls, inn: str) -> bool:
        """Проверка существования записи по ИНН."""
        if not inn:
            return None
        return cls.objects.filter(inn=inn).exists()

    @classmethod
    def checkout_address(cls, address: str) -> bool:
        """Проверка существования записи по адресу."""
        if not address:
            return None
        return cls.objects.filter(address__icontains=address).exists()

class User(AbstractUser):
    """Представляет модель пользователя."""

    fio = models.CharField(verbose_name="ФИО", max_length=150)
    uid = models.UUIDField(verbose_name="ИД пользователя", default=uuid.uuid4, unique=True)
    inn = models.ForeignKey(
        Company, 
        on_delete=models.SET_NULL,
        verbose_name="ИНН компании",
        related_name="users",
        null=True,
    )

    @classmethod
    def checkout_uid(cls, uid: str) -> bool:
        """Проверка существования записи в базе по uid."""
        if not uid:
            return None

        return cls.objects.filter(uid=uid).exists()

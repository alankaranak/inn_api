from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from company.managers import CustomUserManager


class Company(models.Model):
    """Представляет модель компании."""

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    inn = models.CharField(verbose_name="ИНН", unique=True, max_length=13)
    name = models.CharField(verbose_name="Наименование компании", max_length=150)
    address = models.CharField(verbose_name="Адрес", max_length=150)
    nol = models.PositiveIntegerField(verbose_name="Количество лицензий", default=0)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def get_company(cls, inn):
        """Получить экземпляр компании.
        
        Если компания не найдена по ИНН, будет создан новый экземпляр,
        у которого на поля `Address`, `Name` будет выставлено пришедшее значение ИНН
        """
        try:
            return cls.objects.get(inn=inn)
        except cls.DoesNotExist:
            company = cls.objects.create(inn=inn, name=inn, address=inn)
            return company


class Person(models.Model):
    """Представляет модель человека."""

    class Meta:
        verbose_name = 'Лицензия'
        verbose_name_plural = 'Лицензии'

    fio = models.CharField(verbose_name="ФИО", max_length=150)
    uid = models.UUIDField(verbose_name="ИД пользователя", default=uuid.uuid4, unique=True)
    company = models.ForeignKey(
        Company, 
        on_delete=models.SET_NULL,
        verbose_name="ИНН компании",
        related_name="persons",
        null=True,
    )

    def __str__(self) -> str:
        return self.fio

    @classmethod
    def get_person(cls, uid: str):
        """Получить экземпляр персоны.
        
        Если объект по УИД не найден, будет возвращен экземпляр,
        у которого еще не вызывался `save`
        """
        try:
            return cls.objects.get(uid=uid)
        except cls.DoesNotExist:
            return cls(uid=uid)

    @classmethod
    def checkout_data(cls, uid: uuid.UUID, inn: str, address: str) -> int:
        """Последовательная проверка существования записи.

        Параметры:
        `uid`, `inn`, `address` - str
        
        Возвращает: `0` / `1`

        `0` - Совпадений не найдено
        `1` - Совпадение найдено
        """
        if not uid:
            raise ValueError('Поле uid обязательно')
        if not inn or inn == "":
            raise ValueError('Поле inn обязательно')
        if not address or address == "":
            raise ValueError('Поле address обязательно')

        if not isinstance(uid, uuid.UUID):
            raise TypeError(f"Параметр {uid} не является объектом типа UUID")

        qs = cls.objects.filter(uid=uid, company__inn=inn, company__address__icontains=address)
        if qs.exists():
            return 1

        return 0


class User(AbstractUser):
    """Представляет модель пользователя."""

    fio = models.CharField(verbose_name="ФИО", max_length=150)
    uid = models.UUIDField(verbose_name="ИД пользователя", default=uuid.uuid4, unique=True)
    company = models.ForeignKey(
        Company, 
        on_delete=models.SET_NULL,
        verbose_name="ИНН компании",
        related_name="users",
        null=True,
    )

    USERNAME_FIELD = 'username'
    objects = CustomUserManager()

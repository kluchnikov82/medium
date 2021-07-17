import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractUser
from guess.models import Medium

# Create your models here.


class AppUser(AbstractUser):
    """
        Пользователь
    """

    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          verbose_name='ID пользователя')

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин')

    session = models.CharField(default='',
                               blank=True,
                               max_length=40,
                               verbose_name='Сессия')

    number = ArrayField(models.CharField(max_length=200), blank=True, default=list)

    medium = models.ManyToManyField(Medium)


    is_active = models.BooleanField(verbose_name='Активный', default=True)
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Дата последнего изменения')
    deleted = models.DateTimeField(default=None,
                                   null=True,
                                   verbose_name='Дата удаления')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'account_users'

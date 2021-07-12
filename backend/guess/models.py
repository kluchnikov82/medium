from django.db import models

# Create your models here.
from django.db.models import Model


class Medium(Model):
    """
    Модель экстрасенсы
    """
    name = models.CharField(max_length=250,
                            verbose_name='Имя экстрасенса')

    guess1 = models.IntegerField(default=0, verbose_name='Догадка1')
    guess2 = models.IntegerField(default=0, verbose_name='Догадка2')
    level = models.IntegerField(default=0, verbose_name='Уровень доверенности')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Догадка'
        verbose_name_plural = 'Догадки'
        db_table = 'medium'

    def __str__(self):
        return self.name


class History(Model):
    """
    Модель история
    """
    number = models.IntegerField(default=0, verbose_name='Пользовательское значение')

    class Meta:
        verbose_name = 'История'
        db_table = 'history'

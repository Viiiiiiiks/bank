from django.db import models
from django.views.generic.base import TemplateView


class Post(models.Model):
    """

    Цель: Создание внутренней БД на основе класса Post
    """
    Number = models.CharField(max_length=200, default='1')
    REGN = models.CharField(max_length=200, default='1')
    NAME_B = models.CharField(max_length=200, default='1')
    ROOT = models.CharField(max_length=200, default='1')
    SIM_R = models.FloatField(default=1.0)
    SIM_V = models.FloatField(default=1.0)
    SIM_ITOGO = models.FloatField(default=1.0)
    DT = models.DateField(default=2019 / 10 / 12)

    def str(self):
        return self.NAME_B

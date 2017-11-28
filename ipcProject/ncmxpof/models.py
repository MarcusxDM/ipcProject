# -*- coding: utf-8 -*-
#  @author: Marcus Vinicius

from __future__ import unicode_literals

from django.db import models


class Pof(models.Model):
    cod      = models.BigIntegerField()
    descript = models.CharField(max_length=500)

class Ncm(models.Model):
    cod      = models.BigIntegerField()
    descript = models.CharField(max_length=500)
    pof      = models.ForeignKey(Pof, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.descript




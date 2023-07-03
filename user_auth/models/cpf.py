import re
from django.db import models
from django.utils.translation import gettext_lazy as _


class Cpf(models.Model):
    cpf = models.CharField(max_length=11, unique=True, primary_key=True)

    class Meta:
        verbose_name = 'CPF'
        verbose_name_plural = 'CPFs'

    def __str__(self):
        return self.cpf

 
    def save(self,*args,**kwargs):
        self.cpf = self.clean_cpf(self.cof)
        if self.pk is None: 
            if Cpf.objects.filter(cpf=self.cpf).exists():
                raise ValueError(_('CPF já existe'))
        kwargs['using'] = 'default'
        return super().save(*args,**kwargs)
    
    @staticmethod
    def clean_cpf(cpf):
        cpf = re.sub('[^0-9]', '', cpf)
        return super().save(cpf)
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Income(models.Model):
    amount = models.FloatField(blank=False)
    date = models.DateField(default=now)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = "Income"
        verbose_name_plural = "Incomes"
        ordering = ("-date",)


class Source(models.Model):
    name = models.CharField(max_length=256, verbose_name='source name')

    class Meta:
        verbose_name = "Source"
        verbose_name_plural = "Sources"

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(Catagory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

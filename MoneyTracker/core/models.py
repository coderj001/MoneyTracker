from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Expense(models.Model):
    amount = models.FloatField(blank=False)
    date = models.DateField(default=now)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        ordering = ("-date",)


class Catagory(models.Model):
    name = models.CharField(max_length=256, verbose_name='catagory name')

    class Meta:
        verbose_name = "Catagory"
        verbose_name_plural = "Catagories"

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(Catagory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

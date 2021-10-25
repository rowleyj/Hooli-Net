from django.db import models

# Create your models here.


class Test(models.Model):
    a = models.IntegerField()
    b = models.IntegerField()
    product = models.IntegerField()

    def __str__(self):
        return str(self.product)
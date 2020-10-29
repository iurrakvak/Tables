from django.db import models


class Account(models.Model):
    number = models.PositiveBigIntegerField(unique=True,
                                            editable=False)
    name = models.TextField()
    date = models.DateTimeField(auto_now_add=True,
                                editable=False)


class Operation(models.Model):
    account = models.ForeignKey(to=Account,
                                editable=False,
                                on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20,
                                 decimal_places=2,
                                 editable=False)

    PUT = 'PUT'
    WDL = 'WITHDRAW'
    TYPE_CHOICES = [
        (PUT, 'PUT'),
        (WDL, 'WITHDRAW'),
    ]
    type = models.TextField(choices=TYPE_CHOICES,
                            editable=False,
                            blank=False)
    date = models.DateTimeField(auto_now_add=True,
                                editable=False)


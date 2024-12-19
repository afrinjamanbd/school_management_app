from django.db import models


# Create your models here.
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    email = models.CharField(max_length=150)
    joining_date = models.DateField(null=False)
    educational_background = models.JSONField(default={"Bachelors": "BBA"}, blank=True)
    salary = models.FloatField(null=False, blank=False)

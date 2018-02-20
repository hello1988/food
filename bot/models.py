from django.db import models

# Create your models here.

class Basis(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Member(Basis):
    line_id = models.CharField(max_length=64)
    name = models.CharField(max_length=32, null=True, blank=True)
    photo = models.CharField(max_length=512, null=True, blank=True)
    email = models.CharField(max_length=512, null=True, blank=True)
    active = models.BooleanField(default=True)
    last_action = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return self.name

class FoodLog(Basis):
    member = models.ForeignKey(Member, models.CASCADE)
    image_url = models.CharField(max_length=512)
    starch = models.FloatField(default=0.0, verbose_name='主食')
    protein = models.FloatField(default=0.0, verbose_name='蛋白質')
    fruit = models.FloatField(default=0.0, verbose_name='水果')
    vegetables = models.FloatField(default=0.0, verbose_name='蔬菜')


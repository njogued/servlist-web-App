from django.db import models
# from users.models import User
from django.contrib.auth.models import User as Uzer

# Create your models here.


class Business(models.Model):
    business_id = models.AutoField(primary_key=True)
    business_name = models.CharField(max_length=100)
    business_type = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    location = models.CharField(max_length=50)
    email_contact = models.EmailField(max_length=100)
    phone_contact = models.CharField(max_length=20)
    status = models.IntegerField(choices=((0, "inactive"), (1, "active")))
    date_created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(Uzer, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'businesses'
        verbose_name_plural = 'Businesses'

    def __str__(self):
        return self.business_name

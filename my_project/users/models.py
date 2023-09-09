from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.TextField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = True
        db_table = 'users'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"User: {self.first_name} {self.last_name}, Date Created: {self.date_created}"
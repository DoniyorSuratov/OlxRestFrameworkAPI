from django.db import models


# Create your models here.
class SellMessages(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.TextField()
    sent_time = models.DateTimeField(auto_now_add=True)


class BuyMessage(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.TextField()
    sent_time = models.DateTimeField(auto_now_add=True)


class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return  self.name


class UserRole(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    role = models.ForeignKey('accounts.Role', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username





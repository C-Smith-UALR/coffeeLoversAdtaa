from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from invitations.utils import get_invitation_model
from invitations.models import Invitation

class AdtaaUser(AbstractUser):
    ACCESS_CHOICES=(
        ('RU', 'Root User'),
        ('AU', 'Admin User'),
        ('SU', 'Scheduler User'),
        ('', '--------'),
    )

    accessRequested = models.CharField(
        max_length=2,
        choices=ACCESS_CHOICES,
        default='',
        blank=True,
    )

    # is_active = models.BooleanField(
    #     default=False,
    # )

    def returnUserRequested(self):
        for choice in self.ACCESS_CHOICES:
            if choice[0] == self.accessRequested:
                return choice[1]

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'pk':self.pk})

    def userActiveYesNo(self):
        if self.is_active:
            return 'Yes'
        else:
            return 'No'

    def userAdminYesNo(self):
        if self.is_staff:
            return 'Yes'
        else:
            return 'No'


class Profile(models.Model):
    user = models.OneToOneField(AdtaaUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

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

    is_active = models.BooleanField("scheduler user", help_text='A scheduler user will be able to log in to this application and generate/export schedules using predefined course and instructor information.', default=False)
    is_staff = models.BooleanField("admin user", help_text='An admin user will have all capabilities of a scheduler user along with the ability to edit course and instructor information. <font color="red"><b>This user must also be a scheduler user.</b></font>', default=False)
    is_superuser = models.BooleanField("root user", help_text='A root user will have all capabilities of an admin user along with the abilitiy to approve/deny registration requests and invite new root users. <font color="red"><b>This user must also be a scheduler and admin user.</b></font>', default=False)

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

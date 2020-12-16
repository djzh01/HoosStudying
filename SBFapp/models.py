from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.urls import reverse


class Recurrence(models.Model):  # class to define recurrence in events
    DAY_CHOICES = (
        ('Monday', '1'),
        ('Tuesday', '2'),
        ('Wednesday', '3'),
        ('Thursday', '4'),
        ('Friday', '5'),
        ('Saturday', '6'),
        ('Sunday', '7'),
    )
    choice = models.CharField(max_length=10, choices=DAY_CHOICES, unique=True)

    def __str__(self):
        return self.choice


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=60)
    event_description = models.TextField(blank=True)
    event_start_time = models.TimeField('Start Time', default=None)
    event_end_time = models.TimeField('End Time', default=None)
    event_date = models.DateField('Date', default=None)
    days = models.ManyToManyField(Recurrence, verbose_name='Repeat')

    def get_absolute_url(self):
        return reverse('SBFapp:schedule')

    def get_detail_url(self):
        return reverse('SBFapp:event_detail', args=(self.id,))

    def clean(self):
        if self.event_end_time <= self.event_start_time:
            raise ValidationError('Ending times must be after starting times')

    def __str__(self):
        return self.event_name


GROUP_SIZE_CHOICES = [
         ('Max Two People', '2'),
         ('Max Three People', '3'),
         ('Max Four People', '4'),
         ('Max Five or More People', '5 >'),
     ]


class Profile(models.Model):
    user = models.OneToOneField(User, related_name = "profile", on_delete = models.CASCADE) # Direc relation of
    major = models.CharField(max_length = 40, blank = True, default = "Enter Major") #Would like to make database of the different majors like I did for the years beloew
    YEAR_IN_SCHOOL_CHOICES = [
        ('First Year', '1st'),
        ('Second Year', '2nd'),
        ('Third Year', '3rd'),
        ('Fourth Year', '4th'),
    ]
    year = models.CharField(
        max_length = 20,
        choices= YEAR_IN_SCHOOL_CHOICES,
        blank = True,
        default = 'First',
     )
    
    max_group_size = models.CharField(
        max_length = 30,
        choices = GROUP_SIZE_CHOICES,
        blank = True,
        default = 'Two',
    )
    room = models.CharField(max_length = 100, blank = True)
    # picture = models.ImageField(upload_to='profile_images', blank=True)
    # Place the schedule here
    # Profile Image

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # if created:
    #     Profile.objects.create(user=instance)
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


POST_TYPE= [('help','Help Request'),('find','Buddy Finder'),]


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=100)
    post_type = models.CharField(max_length=20,choices=POST_TYPE, default="")
    post_content = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.post_title

    def get_absolute_url(self):
        return reverse('SBFapp:community')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('SBFapp:post', args=(self.post.id,))


class Group(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='owner')
    group_name = models.CharField(max_length=100)
    group_descr = models.TextField()
    list_users = models.ManyToManyField(User,related_name='group_set')
    private = models.BooleanField()

    def __str__(self):
        return self.group_name

    def get_absolute_url(self):
        return reverse('SBFapp:group', args=(self.id, ))

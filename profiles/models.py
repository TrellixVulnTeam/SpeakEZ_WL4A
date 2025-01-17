from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from django.utils.crypto import get_random_string

# Create your models here.





class Profile(models.Model):
    Languages=[
     ('EN','English'),
     ('ZH','Chinese'),
     ('HI','Hindi'),
     ('ES','Spanish'),
     ('FR','French'),
     ('AR','Arabic'),
     ('RU','Russian'),
     ('BN','Bengali'),
     ('PT','Portuguese'),
     ('ID','Indonesian'),
      ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    Lang_Pref = models.CharField(max_length=2, choices=Languages,default='EN')


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()





class Relationship(models.Model):
    type = models.TextField(max_length=50,blank=True)
    profile = models.ForeignKey(Profile,related_name='relationships', on_delete=models.CASCADE)
    #





class People(models.Model):
    friend_id=models.PositiveIntegerField(null=True, blank=True)
    rel_id= models.ForeignKey(Relationship,related_name='people',on_delete=models.CASCADE)

class requests(models.Model):
    receiver=models.ForeignKey(User,related_name='requests',on_delete=models.CASCADE)
    sender=models.PositiveIntegerField(null=False,blank=False)
    accepted=models.BooleanField(null=False,default=False,blank=False)


@receiver(post_save,sender=requests)
def create_user_relationships(sender, instance, **kwargs):
    #if the instance of request is accepted
    if instance.accepted==True:
        #set the current user
        current_user=User.objects.get(id=instance.receiver.id)
        #set the sender
        oth_user=User.objects.get(id=instance.sender)

        #create the relationships
        user_rel= Relationship.objects.create(type='friend',profile=current_user.profile)
        user_rel.save()
        oth_rel=Relationship.objects.create(type='friend',profile=oth_user.profile)
        oth_rel.save()
        #create the people

        user_peep= People.objects.create(friend_id=oth_user.id,rel_id=user_rel)
        user_peep.save()
        oth_peep=People.objects.create(friend_id=current_user.id,rel_id=oth_rel)
        oth_peep.save()




"""Chat models for the user"""

class Room(models.Model):
    room_name = models.UUIDField(default=uuid.uuid4,editable=False,unique=True,null=False,blank=False)
    user_1 = models.PositiveIntegerField(null=False,blank=False)
    user_2 = models.PositiveIntegerField(null=False,blank=False)


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages',on_delete=models.CASCADE)
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)


# @receiver(post_save,sender=Room)
# def create_user_room(sender, instance, **kwargs):
#     if instance.user_1 and instance.user_2:
#         instance.room_name = get_random_string(length=32)
#         instance.save()

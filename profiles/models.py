from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from itertools import chain
from django.shortcuts import reverse
import random
from django.db.models import Q

class ProfileManager(models.Manager):

    def get_all_profiles_to_invites(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver= profile))

        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)

        available = [profile for profile in profiles if profile not in accepted]
        return available


    def get_all_profiles(self, me):
        profile = Profile.objects.all().exclude(user=me)
        return profile



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', default='avatar.png')
    background= models.ImageField(upload_to='backgrounds', default='background.jpg')
    following = models.ManyToManyField(User, related_name='following', blank=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    bio = models.TextField(default="no bio...")
    slug = models.SlugField(unique=True,blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        ex= False
        if self.user:
            to_slug = slugify(str(self.user))
            ex = Profile.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                ex = Profile.objects.filter(slug= to_slug).exists()
            else:
                to_slug = str(self.user)
            self.slug = to_slug
            super().save(*args, **kwargs)

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def get_posts_no(self):
        return self.posts.all().count()

    def get_all_authors_posts(self):
        return self.posts.all()

    def get_like_give_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value == 'Like':
                total_liked += 1
        return total_liked

    def get_likes_received_no(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked

    def get_my_posts(self):
        return self.post_set.all()

    @property
    def num_posts(self):
        return self.post_set.all().count()

    def get_following(self):
        return self.following.all()

    def get_following_users(self):
        following_list = [p for p in self.get_following()]
        return following_list

    def get_my_and_following_posts(self):
        users = [user for user in self.get_following()]
        posts = []
        qs = None
        for u in users:
            p = Profile.objects.get(user=u)
            p_posts = p.post_set.all()
            posts.append(p_posts)
        my_posts = self.post_set.all()
        posts.append(my_posts)
        if len(posts) > 0:
            qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.created)
        return qs

    def get_proposals_for_following(self):
        profiles = Profile.objects.all().exclude(user=self.user)
        followers_list = [p for p in self.get_following()]
        available = [p.user for p in profiles if p.user not in followers_list]
        random.shuffle(available)
        return available[:3]

    @property
    def following_count(self):
        return self.get_following().count()

    def get_followers(self):
        qs = Profile.objects.all()
        followers_list = []
        for profile in qs:
            if self.user in profile.get_following():
                followers_list.append(profile)
        return followers_list

    @property
    def followers_count(self):
        return len(self.get_followers())

STATUS_CHOICES = (
    ('send','send'),
    ('accepted','accepted')
)

class RelationshipManager(models.Manager):
    def invatations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs 


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8,choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
    

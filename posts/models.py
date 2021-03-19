from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile

class Post(models.Model):
    picture = models.ImageField(upload_to='images', blank=True)
    body = models.TextField()
    liked = models.ManyToManyField(Profile, default=None, blank=True,related_name='likes')
    author = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True,related_name='posts')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}-{self.body}"

    def get_liked(self):
        return self.liked.all()

    @property
    def like_count(self):
        return self.liked.all().count()

    def num_comments(self):
        return self.comment_set.all().count() 

    def get_user_liked(self, user):
        pass

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.pk)


LIKE_CHOICES = (
    ('Like','Like'),
    ('Unlike','Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"
    
    

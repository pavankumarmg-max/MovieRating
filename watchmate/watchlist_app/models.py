from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.
class StreamPlatform(models.Model):
    name= models.CharField(max_length=30)
    about= models.CharField(max_length=150)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name

        
class WatchList(models.Model):
    title=models.CharField(max_length=50,blank=True,null=True)
    description=models.CharField(max_length=500,null=True,blank=True)
    platform = models.ForeignKey(StreamPlatform,on_delete=models.CASCADE,related_name='watchlist')
    active= models.BooleanField(default=True)
    avg_rating=models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    user_review=models.ForeignKey(User, on_delete=models.CASCADE)
    rating=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    describe=models.CharField(max_length=200,null=True, blank=True)
    active=models.BooleanField(default=True)
    watchlist = models.ForeignKey(WatchList,on_delete=models.CASCADE,related_name='reviews')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating)+" | "+str(self.watchlist.title)

# print('appmodel 24')
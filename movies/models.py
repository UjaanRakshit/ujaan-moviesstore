from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')

    def __str__(self):
        return str(self.id) + ' - ' + self.name

    def get_average_rating(self):
        """Calculate and return the average rating for this movie"""
        avg = self.rating_set.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0

    def get_rating_count(self):
        """Return the number of ratings for this movie"""
        return self.rating_set.count()

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    rating = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('movie', 'user')

    def __str__(self):
        return f'{self.user.username} - {self.movie.name} - {self.rating} stars'

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name
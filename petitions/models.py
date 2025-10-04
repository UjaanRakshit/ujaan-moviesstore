from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Petition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    movie_title = models.CharField(max_length=200)
    movie_director = models.CharField(max_length=100, blank=True)
    movie_year = models.IntegerField(blank=True, null=True)
    movie_genre = models.CharField(max_length=100, blank=True)
    movie_description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_petitions')
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Petition for '{self.movie_title}' by {self.created_by.username}"
    
    def get_yes_votes(self):
        return self.votes.filter(vote_type='yes').count()
    
    def get_no_votes(self):
        return self.votes.filter(vote_type='no').count()
    
    def get_total_votes(self):
        return self.votes.count()
    
    def has_user_voted(self, user):
        if not user.is_authenticated:
            return False
        return self.votes.filter(user=user).exists()
    
    def get_user_vote(self, user):
        if not user.is_authenticated:
            return None
        try:
            vote = self.votes.get(user=user)
            return vote.vote_type
        except Vote.DoesNotExist:
            return None
    
    class Meta:
        ordering = ['-created_at']


class Vote(models.Model):
    VOTE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=3, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('petition', 'user')  # One vote per user per petition
    
    def __str__(self):
        return f"{self.user.username} voted '{self.vote_type}' on '{self.petition.movie_title}'"
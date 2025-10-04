from django.contrib import admin
from .models import Petition, Vote


@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ['movie_title', 'created_by', 'created_at', 'get_yes_votes', 'get_no_votes', 'is_active']
    list_filter = ['is_active', 'created_at', 'movie_genre']
    search_fields = ['movie_title', 'created_by__username', 'description']
    readonly_fields = ['created_at']
    
    def get_yes_votes(self, obj):
        return obj.get_yes_votes()
    get_yes_votes.short_description = 'Yes Votes'
    
    def get_no_votes(self, obj):
        return obj.get_no_votes()
    get_no_votes.short_description = 'No Votes'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['petition', 'user', 'vote_type', 'created_at']
    list_filter = ['vote_type', 'created_at']
    search_fields = ['petition__movie_title', 'user__username']
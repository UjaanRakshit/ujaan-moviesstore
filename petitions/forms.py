from django import forms
from .models import Petition


class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ['title', 'description', 'movie_title', 'movie_director', 'movie_year', 'movie_genre', 'movie_description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a title for your petition'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Explain why this movie should be added to the catalog'
            }),
            'movie_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the movie title'
            }),
            'movie_director': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the director name (optional)'
            }),
            'movie_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the release year (optional)',
                'min': 1900,
                'max': 2030
            }),
            'movie_genre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the genre (optional)'
            }),
            'movie_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of the movie (optional)'
            }),
        }
        labels = {
            'title': 'Petition Title',
            'description': 'Why should this movie be added?',
            'movie_title': 'Movie Title',
            'movie_director': 'Director',
            'movie_year': 'Release Year',
            'movie_genre': 'Genre',
            'movie_description': 'Movie Description',
        }
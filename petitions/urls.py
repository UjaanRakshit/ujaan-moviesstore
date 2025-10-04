from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='petitions.index'),
    path('create/', views.create_petition, name='petitions.create'),
    path('my-petitions/', views.my_petitions, name='petitions.my_petitions'),
    path('<int:petition_id>/', views.petition_detail, name='petitions.detail'),
    path('<int:petition_id>/vote/', views.vote_petition, name='petitions.vote'),
]
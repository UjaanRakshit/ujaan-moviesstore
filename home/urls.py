from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home.index'),
    path('about', views.about, name='home.about'),
    path('local-popularity-map', views.local_popularity_map, name='home.local_popularity_map'),
    # APIs for regional popularity and session region
    path('api/region-popularity', views.api_region_popularity, name='api.region_popularity'),
    path('api/region/<str:region_code>/top', views.api_region_top, name='api.region_top'),
    path('api/set-region', views.api_set_region, name='api.set_region'),
]
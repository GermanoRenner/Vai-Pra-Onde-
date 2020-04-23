from django.urls import path
from . import routesCalculateView

urlpatterns = [
    path('', routesCalculateView.createCity, name='post_cities'),
    path('insertWithRoad', routesCalculateView.createCityWithRoad, name='post_cities_rel'),
    path('buscarNos', routesCalculateView.getCity, name='get_cities'),

]
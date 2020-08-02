from django.urls import path
from . import routesCalculateView

urlpatterns = [
    path('', routesCalculateView.createCity, name='post_cities'),
    path('insertRoad', routesCalculateView.createRoad, name='post_cities_rel'),
    path('buscarNos', routesCalculateView.getCity, name='get_cities'),
    path('getDistance', routesCalculateView.getDistance, name='get_distance'),
    path('getShortestDistance', routesCalculateView.calcularShortestRoute, name='get_shortest_distance'),
    path('getAllCitiesWithRoads', routesCalculateView.getAllCitysWithRoads, name='get_all_cities_roads')



]
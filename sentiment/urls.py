from django.urls import path 
from . import views
from background_task import background


urlpatterns = [
    path('', views.index, name='dashboard-index'),
    path('search/', views.search, name='search_results')
]



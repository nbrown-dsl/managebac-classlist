from django.urls import path
from . import views

urlpatterns = [
    path('home',views.home,name='home'),
    path('',views.home,name='home'),
    path('about',views.about,name='about'),
    path('search',views.search,name='search'),
    path('student',views.student,name='student'),
 
]

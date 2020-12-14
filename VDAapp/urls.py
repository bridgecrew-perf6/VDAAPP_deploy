from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('api/vinEcu', Isupdate_for_Vehicle.as_view()),
    path('api/onlyvin', Isupdate_for_Vehicle1.as_view()),
    path('', views.IndexView, name="index"),

]

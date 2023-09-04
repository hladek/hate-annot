from django.urls import path,include
from . import views

urlpatterns = [
    path("users/",views.users),
    path("question/",views.question),
    path("start/",views.start),
    path("",views.index),
]

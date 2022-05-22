from django.urls import path
from .views import *

urlpatterns = [
    path('entity/', EntityView.as_view()),
    path('main/', main.as_view()),
]

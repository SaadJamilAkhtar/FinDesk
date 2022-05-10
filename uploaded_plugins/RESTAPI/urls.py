from django.urls import path
from .views import *

urlpatterns = [
    path('entity/', EntityView.as_view()),
]

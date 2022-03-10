from django.urls import path

from ledger import views

urlpatterns = [
    path('my-dashboard/', views.DasboardView.as_view(), name='home'),
]

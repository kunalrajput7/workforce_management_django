from django.urls import path

from . import views

urlpatterns = [
    path('', views.onboard, name="onboard"),
    path('bulk_upload/', views.bulk_upload, name="bulk_upload"),
    path('details/', views.details, name="details")
]
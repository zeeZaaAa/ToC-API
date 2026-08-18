from django.urls import path

from . import views

urlpatterns = [path('', views.MaskingDataView.as_view(), name='masking-data-detail')]

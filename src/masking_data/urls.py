from django.urls import path

from . import views

urlpatterns = [
    path('', views.MaskingDataListView.as_view(), name='masking-data-list'),
    path('<uuid:id>', views.MaskingDataView.as_view(), name='masking-data-detail'),
]
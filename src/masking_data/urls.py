from django.urls import path

from . import views

urlpatterns = [
    path('', views.MaskingDataListView.as_view(), name='masking-data-list'),
    path('guest', views.GuestMaskingDataView.as_view(), name='guest-route'),
    path('<uuid:id>', views.MaskingDataView.as_view(), name='masking-data-detail'),
]
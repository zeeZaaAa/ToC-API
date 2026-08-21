from django.urls import path
from .views import MaskingDataListView, MaskingDataView
from . import views

urlpatterns = [
	path('', views.MaskingDataListView.as_view(), name='masking-data-list'),
	path('<int:id>/', views.MaskingDataView.as_view(), name='masking-data-detail'),
]


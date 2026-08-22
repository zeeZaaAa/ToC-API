from django.urls import path
from . import views
from .views import MaskingDataListView, MaskingDataDetailView

urlpatterns = [
                path('', views.MaskingDataListView.as_view(), name='masking-data-list'),
                path('<int:id>/', views.MaskingDataView.as_view(), name='masking-data-detail'),
                path('<int:id>/', views.MaskingDataView.as_view(), name='masking-data-update'),
]
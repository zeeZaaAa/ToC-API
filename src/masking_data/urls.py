from django.urls import path

from . import views

urlpatterns = [
    path('', views.MaskingDataView.as_view(), name='masking-data-list'),
    path('<int:id>/', views.MaskingDataView.as_view(), name='masking-data-detail'),
]

# urlpatterns = [
# 	path('', views.MaskingDataView.as_view(), name='masking-data-detail'),
# 	path('<int:id>/', views.MaskingDataView.as_view(), name='masking-data-update'),
# ]

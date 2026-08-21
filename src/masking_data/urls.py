from django.urls import path
from .views import MaskingDataListView, MaskingDataDetailView

urlpatterns = [
                path('', MaskingDataListView.as_view(), name='masking-data-list'),
                path('<int:id>/', MaskingDataDetailView.as_view(), name='masking-data-detail'),
]

# urlpatterns = [
# 	path('', views.MaskingDataView.as_view(), name='masking-data-detail'),
# 	path('<int:id>/', views.MaskingDataView.as_view(), name='masking-data-update'),
# ]

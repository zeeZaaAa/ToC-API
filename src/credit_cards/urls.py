from django.urls import path
from . import views


urlpatterns = [
    path('get_masked_credit_card_number_by_id/', views.get_masked_credit_card_number_by_id, name='get_masked_card_number'),
]
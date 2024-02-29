from django.urls import path
from . import views

urlpatterns = [
    path('recommendation/<str:type>/<str:value>', views.recommendation, name='recommendation'),
    path('data/', views.data, name='data'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('default/<str:type>/<str:value>', views.default, name='default'),
    path('artificial/<str:type>/<str:value>', views.artificial, name='artificial'),
    path('externalSystem/<str:type>/<str:value>', views.externalSystem, name='externalSystem'),
    path('data/', views.data, name='data'),
]

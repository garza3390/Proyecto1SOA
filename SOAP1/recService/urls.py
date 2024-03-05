from django.urls import path
from . import views

urlpatterns = [
    path('default/<str:type>/<str:value>', views.default, name='default'),
    path('default/complete/<str:value1>/<str:value2>', views.defaultComplete, name='defaultComplete'),
    path('artificial/<str:_type>/<str:value>', views.artificial, name='artificial'),
    path('artificial/complete/<str:value1>/<str:value2>', views.artificialComplete, name='artificialComplete'),
    path('externalSystem/<str:type>/<str:value>', views.externalSystem, name='externalSystem'),
    path('externalSystem/<str:value1>/<str:value2>', views.externalSystem2, name='externalSystem2'),
    path('data/', views.data, name='data'),
]

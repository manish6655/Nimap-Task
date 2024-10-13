from django.urls import path
from .views import ClientListCreate, ClientRetrieveUpdateDestroy, ProjectCreate, UserProjectsList

urlpatterns = [
    path('clients/', ClientListCreate.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientRetrieveUpdateDestroy.as_view(), name='client-detail'),
    path('clients/<int:client_id>/projects/', ProjectCreate.as_view(), name='project-create'),
    path('projects/', UserProjectsList.as_view(), name='projects-list'),
]

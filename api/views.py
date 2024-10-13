from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from .models import Client, Project
from .serializers import ClientListSerializer, ClientDetailSerializer, ProjectListSerializer, ProjectSerializer
from rest_framework.permissions import IsAuthenticated

class ClientListCreate(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ClientRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return super().get_object()
        except Client.DoesNotExist:
            raise NotFound(detail="Client not found.", code=404)

class ProjectCreate(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        client_id = self.kwargs['client_id']
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            raise NotFound(detail="Client not found.", code=404)
        serializer.save(client=client, created_by=self.request.user)

class UserProjectsList(generics.ListAPIView):
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        return Project.objects.filter(users=self.request.user)

class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all() 
    serializer_class = ProjectListSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        return Project.objects.all() 
from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='username')

    class Meta:
        model = User
        fields = ['id', 'name']

class ProjectListSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'created_at', 'created_by'] 

class ProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    users = UserSerializer(many=True, read_only=True)
    client_name = serializers.CharField(source='client.client_name', read_only=True)

    user_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client_name', 'users', 'user_ids', 'created_at', 'created_by']
        read_only_fields = ['client_name', 'created_at', 'created_by']

    def create(self, validated_data):
        user_ids = validated_data.pop('user_ids')
        project = Project.objects.create(**validated_data)
        project.users.set(user_ids)
        return project

class ClientListSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by']

class ClientProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project_name'] 

class ClientDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    projects = ClientProjectListSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by','updated_at']

from rest_framework import serializers
from .models import Subject, StudySession


class StudySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySession
        fields = ['id', 'started_at', 'ended_at', 'duration_seconds', 'notes']
        read_only_fields = ['started_at', 'ended_at', 'duration_seconds']


class SubjectSerializer(serializers.ModelSerializer):
    total_study_seconds = serializers.ReadOnlyField()
    sessions = StudySessionSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'color', 'icon', 'created_at', 'total_study_seconds', 'sessions']
        read_only_fields = ['created_at']
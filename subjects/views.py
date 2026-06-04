from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subject, StudySession
from .serializers import SubjectSerializer, StudySessionSerializer


class SubjectListCreateView(generics.ListCreateAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subject.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subject.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_session(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)

    active = subject.sessions.filter(ended_at__isnull=True).first()
    if active:
        return Response(
            {'error': 'Ya hay una sesión activa para esta asignatura.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    session = StudySession.objects.create(subject=subject)
    return Response(StudySessionSerializer(session).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def end_session(request, subject_id, session_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    session = get_object_or_404(StudySession, id=session_id, subject=subject)

    if session.ended_at is not None:
        return Response(
            {'error': 'Esta sesión ya ha finalizado.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    notes = request.data.get('notes', '')
    session.notes = notes
    session.end_session()
    return Response(StudySessionSerializer(session).data)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.SubjectListCreateView.as_view(), name='subject-list-create'),
    path('<int:pk>/', views.SubjectDetailView.as_view(), name='subject-detail'),

    path('<int:subject_id>/sessions/start/', views.start_session, name='session-start'),
    path('<int:subject_id>/sessions/<int:session_id>/end/', views.end_session, name='session-end'),
]
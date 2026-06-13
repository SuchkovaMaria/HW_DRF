from django.core.serializers import get_serializer
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import generics
from course.models import Course, Lesson
from course.serializers import CourseSerializer, LessonSerializer, DetailSerializer
from users.permissions import IsModers, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """Класс вывода списка курсов, создания/редактирования/удаления курса"""

    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        # Автоматически сохраняем текущего пользователя как автора
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModers,)
        elif self.action == 'destroy':
            self.permission_classes = (~IsModers | IsOwner,)
        elif self.action == 'retrieve':
            self.permission_classes = (IsModers | IsOwner,)
        return super().get_permissions()



class LessonList(generics.ListCreateAPIView):
    """Вывод списка уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDetail(generics.RetrieveAPIView):
    """Вывод одного урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModers | IsOwner)

class LessonCreate(generics.CreateAPIView):
    """Создание урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModers)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonUpdate(generics.UpdateAPIView):
    """Изменение урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModers | IsOwner, IsAuthenticated)

class LessonDelete(generics.DestroyAPIView):
    """Удаление урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwner, IsAuthenticated)

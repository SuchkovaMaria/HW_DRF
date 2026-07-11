from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import generics
from course.models import Course, Lesson, Subscriptions
from course.pagination import CustomPagination
from course.serializers import CourseSerializer, LessonSerializer, DetailSerializer, SubscriptionsSerializer
from course.tasks import mail_about_update_course
from users.permissions import IsModers, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """Класс вывода списка курсов, создания/редактирования/удаления курса"""

    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        # Автоматически сохраняем текущего пользователя как автора
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
        course_id = serializer.data.get("id")
        subscriptions_in_course = Subscriptions.objects.filter(course=course_id)
        email_list = []
        for subscription in subscriptions_in_course:
            email_list.append(subscription.owner.email)
        mail_about_update_course.delay(email_list, course_id)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModers,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModers | IsOwner,)
        elif self.action == "retrieve":
            self.permission_classes = (IsModers | IsOwner,)
            # для проверки вывода, что информация о подписке будет отображаться
            # (потому что я сомневаюсь что автор курса будет подписываться на
            # свой курс как было указано требование в прошлом дз)
            # self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()


class LessonList(generics.ListCreateAPIView):
    """Вывод списка уроков"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


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
        course_id = serializer.data.get("course")
        subscriptions_in_course = Subscriptions.objects.filter(course=course_id)
        email_list = []
        for subscription in subscriptions_in_course:
            email_list.append(subscription.owner.email)
        mail_about_update_course.delay(email_list, course_id)


class LessonUpdate(generics.UpdateAPIView):
    """Изменение урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModers | IsOwner, IsAuthenticated)

    def perform_update(self, serializer):
        serializer.save()
        course_id = serializer.data.get("course")
        subscriptions_in_course = Subscriptions.objects.filter(course=course_id)
        email_list = []
        for subscription in subscriptions_in_course:
            email_list.append(subscription.owner.email)
        mail_about_update_course.delay(email_list, course_id)


class LessonDelete(generics.DestroyAPIView):
    """Удаление урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwner, IsAuthenticated)


class SubscriptionsCreate(generics.CreateAPIView):
    """Создание подписки"""

    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer
    permission_classes = (IsAuthenticated, ~IsModers)

    def post(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        owner = request.user
        subscription, created = Subscriptions.objects.get_or_create(owner=owner, course=course)
        serializer = self.get_serializer(subscription)
        if not created:
            return Response({"detail": "Вы уже подписаны на этот курс."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubscriptionsDelete(generics.DestroyAPIView):
    """Удаление подписки"""

    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer
    permission_classes = (IsOwner | IsModers, IsAuthenticated)

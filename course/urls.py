from django.urls import path

from course.apps import DepartmentConfig
from course.views import CourseViewSet, LessonList, LessonDetail, LessonCreate, LessonUpdate, LessonDelete, \
    SubscriptionsCreate, SubscriptionsDelete
from rest_framework.routers import DefaultRouter

app_name = DepartmentConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path("lesson/", LessonList.as_view(), name='lesson-list'),
    path("lesson/<int:pk>/", LessonDetail.as_view(), name='lesson-detail'),
    path("lesson/create", LessonCreate.as_view(), name='lesson-create'),
    path("lesson/<int:pk>/update", LessonUpdate.as_view(), name='lesson-update'),
    path("lesson/<int:pk>/delete", LessonDelete.as_view(), name='lesson-delete'),
    path("subscriptions/<int:course_id>/create", SubscriptionsCreate.as_view(), name='subscriptions-create'),
    path("subscriptions/<int:pk>/delete", SubscriptionsDelete.as_view(), name='subscriptions-delete'),
] + router.urls


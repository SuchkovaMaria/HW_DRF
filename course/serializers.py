from rest_framework import serializers

from course.models import Course, Lesson, Subscriptions
from course.validators import validete_expression_test


class LessonSerializer(serializers.ModelSerializer):

    video_path = serializers.CharField(validators=[validete_expression_test])

    class Meta:
        model = Lesson
        fields = ["id", "name", "description", "image", "course", "video_path", "owner"]
        read_only_fields = ("owner",)


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ["id", "name", "description", "image", "owner"]
        read_only_fields = ("owner",)


class DetailSerializer(serializers.ModelSerializer):

    count_lessons = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()

    def get_count_lessons(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_lessons(self, obj):
        list_lesson = []
        for lesson in Lesson.objects.filter(course=obj):
            list_lesson.append(lesson)
        list_lesson = LessonSerializer(list_lesson, many=True).data
        return list_lesson

    def get_subscription(self, obj):
        status = "Вы не подписаны на курс"
        request = self.context.get("request")
        if request:
            subscriptions = Subscriptions.objects.filter(owner=request.user)
            for subscription in subscriptions:
                if subscription.course == obj:
                    status = "Вы подписаны курс"
        return status

    class Meta:
        model = Course
        fields = ["name", "description", "image", "count_lessons", "lessons", "subscription"]
        read_only_fields = ("owner", "count_lessons", "lessons")


class SubscriptionsSerializer(serializers.ModelSerializer):

    course = CourseSerializer(read_only=True)

    class Meta:
        model = Subscriptions
        fields = ["id", "owner", "course"]
        read_only_fields = (
            "owner",
            "course",
        )

from rest_framework import serializers

from course.models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'image', 'course', 'video_path']


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'image']

class DetailSerializer(serializers.ModelSerializer):

    count_lessons = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

    def get_count_lessons(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_lessons(self, obj):
        list_lesson = []
        for lesson in Lesson.objects.filter(course=obj):
            list_lesson.append(lesson)
        list_lesson = LessonSerializer(list_lesson, many=True).data
        return list_lesson

    class Meta:
        model = Course
        fields = ['name', 'description', 'image', 'count_lessons', 'lessons']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'image', 'course', 'video_path']
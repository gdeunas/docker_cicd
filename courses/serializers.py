from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from courses.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    count_course_with_lesson = SerializerMethodField()

    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            "title",
            "preview",
            "description",
            "count_course_with_lesson",
            "lessons",
        )

    def get_count_course_with_lesson(self, courses):
        return Course.objects.filter(lesson=courses.lesson).count()

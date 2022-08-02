from rest_framework import serializers

from product.models import Lesson, UserLesson, Product


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('topic',)


class UserLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLesson
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)
    num_views = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ('name', 'num_views', 'lessons')

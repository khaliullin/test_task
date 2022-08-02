from django.db.models import Count, Q
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from product.models import UserLesson, Product
from product.serializers import UserLessonSerializer, ProductSerializer


class UserLessonViewSet(GenericViewSet, RetrieveModelMixin, CreateModelMixin):
    serializer_class = UserLessonSerializer
    queryset = UserLesson.objects.all()


class ProductView(GenericViewSet, ListModelMixin):
    permission_classes = [IsAuthenticated]

    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        return Product.objects.annotate(
            num_views=Count('lessons', filter=Q(lessons__userlesson__user=self.request.user))
        )

from rest_framework import routers

from product.views import UserLessonViewSet, ProductView

router = routers.DefaultRouter()
router.register('userlesson', UserLessonViewSet)
router.register('product', ProductView)


from django.contrib import admin
from django.db.models import Count, Max

from product.models import Product, Lesson, UserLesson


class NumViewsFilter(admin.SimpleListFilter):
    title = 'Number of views'
    parameter_name = 'num_views'

    def lookups(self, request, model_admin):
        max_value = UserLesson.objects.all().values('lesson').annotate(
            count_views=Count('lesson')
        ).aggregate(
            max_value=Max('count_views')
        )['max_value']
        if max_value:
            return [(i, i) for i in range(max_value + 1)]
        else:
            return []

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        else:
            return queryset.annotate(
                num_views=Count('userlesson__lesson')
            ).filter(
                num_views=self.value()
            )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('topic', 'product', 'viewed')
    list_filter = (NumViewsFilter,)

    def viewed(self, obj):
        return UserLesson.objects.filter(lesson=obj).count()


@admin.register(UserLesson)
class UserLessonAdmin(admin.ModelAdmin):
    pass
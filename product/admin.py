import json

import numpy as np
from django.contrib import admin
from django.db.models import Count

from product.models import Product, Lesson, UserLesson


class NumViewsFilter(admin.SimpleListFilter):
    title = 'Number of views'
    parameter_name = 'num_views'

    def get_quantiles(self, lst: list):
        if len(lst) <= 2:
            return None
        result = []
        quantiles = np.quantile(lst, q=np.arange(0.25, 1, 0.25))
        for i in range(len(quantiles)):
            if i == 0:
                result.append(([0, quantiles[i]], f'0 – {quantiles[i]}'))
            else:
                result.append(([quantiles[i - 1], quantiles[i]], f'{quantiles[i - 1]} – {quantiles[i]}'))
        result.append(([quantiles[-1], lst[-1]], f'{quantiles[-1]} – {lst[-1]}'))

        return result

    def lookups(self, request, model_admin):
        views_count = Lesson.objects.annotate(
            num_views=Count('userlesson__lesson')
        ).order_by('num_views').values_list('num_views', flat=True)

        return self.get_quantiles(lst=list(views_count))

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        else:
            value = json.loads(self.value())
            return queryset.annotate(
                num_views=Count('userlesson__lesson')
            ).filter(
                num_views__gte=value[0],
                num_views__lte=value[1]
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
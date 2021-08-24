from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^lists$', TaskListView.as_view(), name='task lists'),
    url(r'^multiple_choice_test/create$', MultipleChoiceTestCreateView.as_view(),
        name='create multiple choice test'),
    url(r'^multiple_choice_test/update=(?P<pk>\d+)$', MultipleChoiceTestUpdateView.as_view(),
        name='update multiple choice test'),
]

from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^multiply_choice_test/create$', MultiplyChoiceTestCreateView.as_view(),
        name='create multiply choice test'),
    url(r'^multiply_choice_test/update=(?P<pk>\d+)$', MultiplyChoiceTestUpdateView.as_view(),
        name='update multiply choice test'),
]

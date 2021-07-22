from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^start$', TestingSessionCreateView.as_view(),
        name='create testing session'),
]

from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^start$', TestingSessionCreateView.as_view(), name='create testing session'),
    url(r'^session=(?P<pk>\d+)$', TestingView.as_view(), name='testing'),
    url(r'^result/session=(?P<pk>\d+)$', TestingResultView.as_view(), name='testing result'),
    url(r'^sessions$', ActiveTestingSessions.as_view(), name='active testing sessions'),
]

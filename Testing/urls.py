from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^start(?:=(?P<test_pk>\d+))?$', TestingSessionCreateView.as_view(), name='create testing session'),
    url(r'^session=(?P<pk>\d+)$', TestingView.as_view(), name='testing'),
    url(r'^session=(?P<pk>\d+)/result$', TestingResultView.as_view(), name='testing result'),
    url(r'^sessions$', ActiveTestingSessions.as_view(), name='active testing sessions'),
    url(r'^results$', ResultsDispatcherView.as_view(), name='results dispatcher'),
    url(r'^results/test=(?P<test_pk>\d+)&dates=(?P<from>[0-9]{2}.[0-9]{2}.[0-9]{4})-'
        r'(?P<to>[0-9]{2}.[0-9]{2}.[0-9]{4})$', ResultsView.as_view(), name='testing results')
]

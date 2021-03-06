from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^list$', TestListView.as_view(), name='test list'),
    url(r'^create$', TestCreateView.as_view(), name='create test'),
    url(r'^update=(?P<pk>\d+)$', TestUpdateView.as_view(), name='update test'),
]

from django.urls import path
from tests import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tests', views.TestsView.as_view(), name='tests'),
    path('test/<int:test_id>', views.TestView.as_view(), name='test'),
]
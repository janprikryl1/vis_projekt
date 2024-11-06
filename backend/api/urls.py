from django.urls import path
from api import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('is-authenticated', views.IsAuthenticatedView.as_view(), name='is-authenticated'),
    path('latest-tests', views.LatestTestsView.as_view(), name='latest-tests'),


    path('tests', views.TestsView.as_view(), name='tests'),
    path('test/<int:test_id>', views.TestView.as_view(), name='test'),
    path('new-tests', views.NewTests.as_view(), name='new-tests'),
    path('user', views.UserView.as_view(), name='user')
]
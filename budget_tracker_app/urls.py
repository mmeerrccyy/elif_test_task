from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='hello_world'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('login/', views.LoginView.as_view(), name='login')
]

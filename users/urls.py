from django.urls import path
from users.views import SignUpView, LoginView

urlpatterns = [
    path('/register', SignUpView.as_view()),
    path('/signin', LoginView.as_view()),
]

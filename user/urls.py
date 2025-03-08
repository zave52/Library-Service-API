from django.urls import path

from user.views import CreateUserView, ManageUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register_user"),
    path("me/", ManageUserView.as_view(), name="manage_user"),
]

app_name = "user"

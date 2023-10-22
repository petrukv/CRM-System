from django.urls import path
from .import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("register/", views.register, name = "register"),
    path("login/", views.login_page, name = "login"),
    path("logout/", views.logout_user, name="logout"),
    path("update/<int:pk>/", views.update_info, name = "update"),
    path("delete/<int:pk>/", views.delete, name = "delete"),
    path("add_record/", views.add_record, name="add_record")
]

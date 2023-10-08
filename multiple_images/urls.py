from django.urls import path


from . import views

app_name = "multiple_images"


urlpatterns = [
    path("images/", views.MultipleImages.as_view(), name="list_add_image"),
    path("images/list/", views.ListAllDetails.as_view(), name="list_add_image"),
]

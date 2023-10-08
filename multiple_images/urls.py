from django.urls import path


from . import views

app_name = "multiple_images"


urlpatterns = [
    path("create_image/", views.CreateImage.as_view(), name="add_image"),
    path("images/", views.ListImages.as_view(), name="list_images"),
    path("images/<int:pk>/", views.SpecificImage.as_view(), name="specific_image"),
    path("images/update/<int:pk>/", views.UpdateImage.as_view(), name="update_image"),
]

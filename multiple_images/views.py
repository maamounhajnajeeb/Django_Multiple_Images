from rest_framework import generics, permissions
from rest_framework import response, status

from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest

from . import serializers, models, mixins


class CreateImage(generics.CreateAPIView):
    
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.CreateMultipleImages
    queryset = models.MultipleImage.objects
    
    def create(self, request: HttpRequest, *args, **kwargs):
        images_names = self.manage_uploaded_images(request)
        
        new_request_data = request.data.copy()
        new_request_data["images"] = images_names
        
        serializer = self.serializer_class(data=new_request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return response.Response({
            "status": 1
            , "data": serializer.data}
            , status=status.HTTP_201_CREATED
            , headers=self.get_success_headers(serializer.data))

    def manage_uploaded_images(self, request):
        uploaded_images = request.FILES.getlist("images")
        images_names = ""
        fs = FileSystemStorage()
        for image in uploaded_images:
            files_names = fs.listdir(fs.location)[1]
            unique_name = self.check_redundent(image.name, files_names)
            images_names += f" {fs.base_url}{unique_name}"
            fs.save(unique_name, image)
            
        return images_names[1:]
    
    def check_redundent(self, image_name, files_names, counter=-1):
        new_name, new_extension = image_name.split(".")
        for image in files_names:
            old_name, old_extenstion = image.split(".")
            if old_extenstion == new_extension and old_name == new_name:
                counter += 1
                image_name = f"{new_name}{counter}.{new_extension}"
                return self.check_redundent(image_name, files_names, counter)
        
        return image_name


class ListImages(generics.ListAPIView):
    queryset = models.MultipleImage.objects
    serializer_class = serializers.GetImages
    permission_classes = ()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().all()
        serializer = self.get_serializer(queryset, many=True)
        
        return response.Response({
            "data": serializer.data,
        }, status=status.HTTP_200_OK)


class SpecificImage(generics.RetrieveDestroyAPIView, mixins.DeleteFilesMixin):
    queryset = models.MultipleImage.objects
    serializer_class = serializers.GetImages
    permission_classes = ()
    
    def get_object(self):
        obj = super().get_object()
        if self.request.method != "GET":
            self.delete_files(obj)
        return obj
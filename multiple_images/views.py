from rest_framework import generics, permissions
from rest_framework import response, status

from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest

from uuid import uuid4

from . import serializers, models, mixins


class CreateImage(generics.CreateAPIView, mixins.DeleteFilesMixin):
    
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.CreateMultipleImages
    queryset = models.MultipleImage.objects
    
    def create(self, request: HttpRequest, *args, **kwargs):
        images_names = self.manage_uploaded_images()
        # images_names = self.manage_uploaded_images(request)
        
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

    # def manage_uploaded_images(self, request: HttpRequest):
    #     fs = FileSystemStorage()
    #     images_names = ""
        
    #     uploaded_images = self.uploaded_images(request)
    #     for image_obj in uploaded_images:
    #         files_names = self.get_files_names(fs)
    #         unique_name = self.check_redundent(image_obj.name, files_names)
    #         images_names += f" {fs.base_url}{unique_name}"
    #         fs.save(unique_name, image_obj)
            
    #     return images_names[1:]
    
    # def check_redundent(self, image_name, files_names):
    #     new_name, new_extension = uuid4().hex, image_name.split(".")[1]
    #     new_image_name = f"{new_name}.{new_extension}"
    #     if new_image_name in files_names:
    #         return self.check_redundent(image_name, files_names)
    #     return new_image_name
    
    # def get_files_names(self, fs: FileSystemStorage):
    #     return fs.listdir(fs.location)[1]
    
    # def uploaded_images(self, request: HttpRequest):
    #     return request.FILES.getlist("images")


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


class UpdateImage(generics.UpdateAPIView, mixins.DeleteFilesMixin):
    queryset = models.MultipleImage.objects
    serializer_class = serializers.GetImages
    permission_classes = ()
    
    def get_object(self):
        obj = super().get_object()
        if self.request.method != "GET":
            self.delete_files(obj)
            self.manage_uploaded_images()
        return obj


class SpecificImage(generics.RetrieveDestroyAPIView, mixins.DeleteFilesMixin):
    queryset = models.MultipleImage.objects
    serializer_class = serializers.GetImages
    permission_classes = ()
    
    def get_object(self):
        obj = super().get_object()
        if self.request.method != "GET":
            self.delete_files(obj)
        return obj
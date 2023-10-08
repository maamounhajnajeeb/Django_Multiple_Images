from rest_framework import generics, permissions
from rest_framework import response, status

from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest

from uuid import uuid4

from . import serializers, models, mixins


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


class CreateImage(generics.CreateAPIView, mixins.DeleteFilesMixin):
    
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.CreateMultipleImages
    queryset = models.MultipleImage.objects
    
    def create(self, request: HttpRequest, *args, **kwargs):
        images_names = self.manage_uploaded_images()
        request.data["images"] = images_names
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return response.Response({
            "status": 1
            , "data": serializer.data}
            , status=status.HTTP_201_CREATED
            , headers=self.get_success_headers(serializer.data))


class UpdateImage(generics.UpdateAPIView, mixins.DeleteFilesMixin):
    queryset = models.MultipleImage.objects
    serializer_class = serializers.GetImages
    permission_classes = ()
    
    def get_object(self):
        obj = super().get_object()
        if self.request.method != "GET":
            self.delete_files(obj)
        return obj
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        new_request_data = self.edit_request_data()
        serializer = self.get_serializer(instance, data=new_request_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return response.Response(serializer.data)
    
    def edit_request_data(self):
        images_names = self.manage_uploaded_images()
        self.request.data["images"] = images_names
        
        return self.request.data


class SpecificImage(generics.RetrieveDestroyAPIView, mixins.DeleteFilesMixin):
    queryset = models.MultipleImage.objects
    serializer_class = serializers.GetImages
    permission_classes = ()
    
    def get_object(self):
        obj = super().get_object()
        if self.request.method != "GET":
            self.delete_files(obj)
        return obj
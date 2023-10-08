from rest_framework import serializers

from . import models

class CreateMultipleImages(serializers.ModelSerializer):

    class Meta:
        model = models.MultipleImage
        fields = "__all__"


class GetImages(CreateMultipleImages):
    images = serializers.SerializerMethodField()
    
    def get_images(self, obj):
        images_str = obj.images
        images_str = images_str.split(" ")
        return images_str
from .models import MultipleImage
from django.core.files.storage import FileSystemStorage

import os

class DeleteFilesMixin:
    
    def delete_files(self, obj: MultipleImage):
        fs = FileSystemStorage()
        location = fs.location
        
        images_names = obj.images.split(" ")
        
        for image in images_names:
            os.remove(location+"\\"+image[6:])
from django import forms
from django.core.exceptions import ValidationError  
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'location', 'catagory', 'subject', 'image', 'text')

    def clean_image(self):

        IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

        uploaded_image= self.cleaned_data.get('image', False )

        extension = str(uploaded_image).split('.')[-1]

        file_type = extension.lower()


        if file_type not in IMAGE_FILE_TYPES:
            raise ValidationError('This is not an image file.')

        return uploaded_image
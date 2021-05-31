from .models import Video
from django import forms


class VideoFrom(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'url', 'youtube_id']
        labels ={'title':'Title','url':'Url','youtube_id':'YouTube Id'}

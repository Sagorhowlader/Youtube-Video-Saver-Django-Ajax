from .models import Video
from django import forms


class VideoFrom(forms.ModelForm):
    class Meta:
        model = Video
        fields = [ 'url']
        labels = {'title': 'Title', 'url': 'Url', 'youtube_id': 'YouTube Id'}


class SearchFrom(forms.Form):
    search_term = forms.CharField(max_length=255, label='Search for Video')

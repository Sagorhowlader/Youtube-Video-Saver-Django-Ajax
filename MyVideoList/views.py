from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.shortcuts import render, redirect
from .models import *
# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login
from .forms import VideoFrom,SearchFrom

from django.forms.utils import ErrorList
import urllib
import requests
YOUTUBE_API_key = 'AIzaSyDxWFYPA3FMztGFkCp32GrVsuZtP7YB6i4'


def homepage(request):
    return render(request, 'home.html')


class SingUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/SingUp.html'

    def form_valid(self, form):
        view = super(SingUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


class Create_Playlist(generic.CreateView):
    model = PlayList
    fields = ['title']
    template_name = 'playlist/createplaylist.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(Create_Playlist, self).form_valid(form)
        return redirect('home')


def dashboard(request):
    all_playlist = PlayList.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'playlist': all_playlist})


class DetailsPlaylist(generic.DetailView):
    model = PlayList
    template_name = 'playlist/detailsplaylist.html'


class UpdatePlaylist(generic.UpdateView):
    model = PlayList
    template_name = 'playlist/updateplaylist.html'
    fields = ['title']
    success_url = reverse_lazy('home')


class DeletedPlaylist(generic.DeleteView):
    model = PlayList
    template_name = 'playlist/deletedplaylist.html'
    success_url = reverse_lazy('dashboard')


def AddVideo(request, pk):
    forms = VideoFrom()
    searchform = SearchFrom()
    playlist = PlayList.objects.get(pk=pk)
    print(playlist.user)
    print(playlist.user)
    if playlist.user != request.user:
        raise Http404
    form = VideoFrom(request.POST)
    if form.is_valid():
        video = Video()

        video.url = form.cleaned_data['url']
        video.playlist = playlist
        parse_url = urllib.parse.urlparse(video.url)
        video_id = urllib.parse.parse_qs(parse_url.query).get('v')
        if video_id:
            video.youtube_id = video_id[0]
            response=requests.get('https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={}&key={}'.format(video_id[0],YOUTUBE_API_key))
            response=response.json()
            title= response['items'][0]['snippet']['title']
            video.title = title
            video.save()
            return redirect('detailsplaylist',pk)
        else:
            errors = form._errors.setdefault("url", ErrorList())
            errors.append(u'Needs to be a YouTube URL')
            print(form)
    return render(request, 'addvideo.html', {'form': forms,'searchform':searchform,'playlist':playlist})

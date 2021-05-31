from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import *
# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login
from .forms import VideoFrom


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
    return render(request, 'addvideo.html', {'form': forms})

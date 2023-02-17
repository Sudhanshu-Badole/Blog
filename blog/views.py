from django.shortcuts import render, redirect
from . models import Post
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView, CreateView,
    UpdateView,
    DeleteView
)
# Create your views here.
'''def home(request):
    data ={
        'posts':Post.objects.all()
    }
    return render(request,'home.html',data)'''
class PostListView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html' # <app>/<model>_<viewtype>.html


class PostCreateView(CreateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'login'

    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f'Your Post has been updated!')
        return super().form_valid(form)          
  
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    login_url = '/login/'
    redirect_field_name = 'login'

    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostSearchView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('q')
        if Post.objects.filter(title__icontains=query):
            messages.success(self.request, f'Your Search result are here...')
            query_set =  Post.objects.filter(title__icontains=query)
        elif Post.objects.filter(content__icontains=query):
            messages.success(self.request, f'Your Search result are here...')
            query_set = Post.objects.filter(content__icontains=query)
        else:
            messages.success(self.request, f'Search result not found...')
            query_set = []
        return query_set
        
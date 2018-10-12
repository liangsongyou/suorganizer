from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    View, CreateView, ListView, YearArchiveView,
    MonthArchiveView, ArchiveIndexView, DeleteView,
    DetailView)
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse_lazy

from .models import Post
from .forms import PostForm
from .utils import (
    PostGetMixin, DateObjectMixin, AllowFuturePermissionMixin, 
    PostFormValidMixin)
from user.decorators import require_authenticated_permission


from core.utils import UpdateView


class PostDetail(DateObjectMixin, DetailView):
    
    date_field = 'pub_date'
    model = Post

class PostArchiveYear(YearArchiveView):
    model = Post
    date_field = 'pub_date'
    make_object_list = True


class PostArchiveMonth(MonthArchiveView):
    model = Post
    date_field = 'pub_date'
    month_format = '%m'


class PostList(
        AllowFuturePermissionMixin,
        ArchiveIndexView):
    allow_empty = True
    context_object_name = 'post_list'
    date_field = 'pub_date'
    make_object_list = True
    model = Post
    paginate_by = 5
    template_name = 'blog/post_list.html'


@require_authenticated_permission('blog.add_post')
class PostCreate(PostFormValidMixin, CreateView):
    form_class = PostForm
    model = Post


class PostUpdate(PostFormValidMixin, DateObjectMixin, UpdateView):
    date_field = 'pub_date'
    form_class = PostForm
    model = Post

class PostDelete(DateObjectMixin, DeleteView):
    date_field = 'pub_date'
    model = Post
    success_url = reverse_lazy('blog_post_list')
































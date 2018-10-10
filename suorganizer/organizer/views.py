from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import (
    View, DetailView, CreateView, 
    DeleteView, ListView, DateDetailView)
from django.core.paginator import (
    EmptyPage, PageNotAnInteger, Paginator)
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import (
    login_required, 
    user_passes_test,
    permission_required)
from django.utils.decorators import method_decorator
from django.contrib.auth import PermissionDenied



from .models import Tag, Startup, NewsLink
from .forms import (
    TagForm, StartupForm, NewsLinkForm)
from .utils import (
    CreateView, ObjectUpdateMixin, ObjectDeleteMixin,
    PageLinksMixin,NewsLinkGetObjectMixin, StartupContextMixin)
from user.decorators import require_authenticated_permission, class_login_required

from core.utils import UpdateView


class TagList(PageLinksMixin, ListView):
    paginate_by = 5
    model = Tag


class StartupList(PageLinksMixin, ListView):
    model = Startup
    paginate_by = 5


class NewsLinkCreate(
                     NewsLinkGetObjectMixin,
                     StartupContextMixin,
                     CreateView):
    form_class = NewsLinkForm
    model = NewsLink

    def get_initial(self):
        startup_slug = self.kwargs.get(
            self.startup_slug_url_kwarg)
        self.startup = get_object_or_404(
            Startup, slug__iexact=startup_slug)
        initial = {
            self.startup_context_object_name:
                self.startup,
        }
        initial.update(self.initial)
        return initial


class StartupCreate(CreateView):
    form_class = StartupForm
    model = Startup
    template_name = 'organizer/startup_form.html'


def in_contrib_group(user):
    if user.groups.filter(name='contributors'):
        return True
    else:
        raise PermissionDenied


@require_authenticated_permission('organizer.add_tag')
class TagCreate(CreateView):
    form_class = TagForm
    model = Tag
    template_name = 'organizer/tag_form.html'

    


class NewsLinkUpdate(
        NewsLinkGetObjectMixin,
        StartupContextMixin,
        UpdateView):
    form_class = NewsLinkForm
    model = NewsLink
    slug_url_kwarg = 'newslink_slug'


@require_authenticated_permission('organizer.change_tag')
class TagUpdate(UpdateView):
    form_class = TagForm
    model = Tag


@require_authenticated_permission('organizer.change_startup')
class StartupUpdate(UpdateView):
    form_class = StartupForm
    model = Startup


class NewsLinkDelete(StartupContextMixin,DeleteView):
    model = NewsLink
    slug_url_kwarg = 'newslink_slug'


class TagDelete(DeleteView):
    model = Tag
    success_url = reverse_lazy('organizer_tag_list')


class StartupDelete(DeleteView):
    model = Startup
    success_url = reverse_lazy('organizer_startup_list')
    


class TagPageList(View):
    paginate_by = 5
    template_name = 'organizer/tag_list.html'

    def get(self, request, page_number):
        tags = Tag.objects.all()
        paginator = Paginator(
            tags, self.paginate_by)
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(
                paginator.num_pages)

        if page.has_previous():
            prev_url = reverse(
                'organizer_tag_page',
                args=(
                    page.previous_page_number(),
                ))
        else:
            prev_url = None
        if page.has_next():
            next_url = reverse(
                'organizer_tag_page',
                args=(
                    page.next_page_number(),
                ))
        else:
            next_url = None

        context = {
            'is_paginated':
                page.has_other_pages(),
            'next_page_url': next_url,
            'paginator':paginator,
            'previous_page_url': prev_url,
            'tag_list':page,
        }
        return render(
            request, self.template_name, context)


class TagDetail(DetailView):

    context_object_name = 'tag'
    model = Tag
    template_name = 'organizer/tag_detail.html'

class StartupDetail(DetailView):

    context_object_name = 'startup'
    model = Startup
    template_name = 'organizer/startup_detail.html'






















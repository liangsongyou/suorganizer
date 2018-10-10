from django.shortcuts import redirect, render, get_object_or_404
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import View
from .models import Startup, NewsLink




class PageLinksMixin:
    page_kwarg = 'page'

    def _page_urls(self, page_number):
        return "?{pkw}={n}".format(
            pkw=self.page_kwarg,
            n=page_number)

    def previous_page(self, page):
        if (page.has_previous() and page.number > 2):
            return self._page_urls(
                page.previous_page_number())
        return None

    def next_page(self, page):
        last_page = page.paginator.num_pages
        if (page.has_next() and page.number < last_page -1):
            return self._page_urls(
                page.next_page_number())
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context.get('page_obj')
        if page is not None:
            context.update({
                'first_page_url':
                    self.first_page(page),
                'previous_page_url':
                    self.previous_page(page),
                'next_page_url':
                    self.next_page(page),
                'last_page_url':
                    self.last_page(page),
            })
        return context

    def first_page(self, page):
        if page.number > 1:
            return self._page_urls(1)
        return None

    def last_page(self, page):
        last_page = page.paginator.num_pages
        if page.number < last_page:
            return self._page_urls(last_page)
        return None


class CreateView(View):
    form_class = None
    template_name = ''

    def get(self, request):
        return render(
            request,
            self.template_name,
            {'form': self.form_class()})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_object = bound_form.save()
            return redirect(new_object)
        else:
            return render(
                request,
                self.template_name,
                {'form': bound_form})


class ObjectUpdateMixin:
    form_class = None
    model = None
    template_name = ''

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        context = {
            'form': self.form_class(instance=obj),
            self.model.__name__.lower(): obj,

        }
        return render(request, self.template_name, context)

    def post(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        bound_form = self.form_class(request.POST, instance=obj)
        if bound_form.is_valid():
            new_object = bound_form.save()
            return redirect(new_object)
        else:
            context = {
                'form': bound_form,
                self.model.__name__.lower(): obj,
            }
            return render(request, self.template_name, context)


class ObjectDeleteMixin:
    model = None
    success_url = ''
    template_name = ''

    def get(self, request, slug):
        obj = get_object_or_404(
            self.model, slug__iexact=slug)
        context = {
            self.model.__name__.lower(): obj,
        }
        return render(
            request, self.template_name, context)

    def post(self, request, slug):
        obj = get_object_or_404(
            self.model, slug__iexact=slug)
        obj.delete()
        return HttpResponseRedirect(self.success_url)
            

class DetailView(View):
    context_object_name = ''
    model = None
    template_name = ''
    template_name_suffix = '_detail'

    def get(self, request, **kwargs):
        self.kwargs = kwargs
        self.object = self.get_object()
        template_name = self.get_template_names()
        context = self.get_context_data()
        return render(
            request,
            template_name,
            context)

    def get_context_object_name(self):
        if self.context_object_name:
            return self.context_object_name
        elif isinstance(self.object, Model):
            return self.object._meta.model_name
        else:
            return None

    def get_template_names(self):
        if self.template_name:
            return self.template_name
        return "{app}/{model}{suffix}.html".format(
            app=self.object._meta.app_label,
            model=self.object._meta.model_name,
            suffix=self.template_name_suffix)

    def get_context_data(self):
        context = {}
        if self.object:
            context_object_name = self.get_context_object_name()
            if context_object_name:
                context[context_object_name] = self.object
        return context

    def get_object(self):
        slug = self.kwargs.get('slug')
        if slug is None:
            raise AttributeError(
                "{c} expects {p} parameter "
                " from URL pattern.".format(
                    c=self.__class__.__name__,
                    p='slug'))

        if self.model:
            return get_object_or_404(self.model, slug__iexact=slug)
        else:
            raise ImproperlyConfigured(
                "{c} needs {a} attribute "
                " specified to work.".format(
                    c=self.__class__.__name__,
                    p='model'))


class NewsLinkGetObjectMixin():

    def get_object(self, queryset=None):
        startup_slug = self.kwargs.get(
            self.startup_slug_url_kwarg)
        newslink_slug = self.kwargs.get(
            self.slug_url_kwarg)
        return get_object_or_404(
            NewsLink,
            slug__iexact=newslink_slug,
            startup__slug__iexact=startup_slug)


class StartupContextMixin():
    startup_slug_url_kwarg = 'startup_slug'
    startup_context_object_name = 'startup'

    def get_context_data(self, **kwargs):
        if hasattr(self, 'startup'):
            context = {
                self.startup_context_object_name:
                    self.startup,
            }
        else:

            startup_slug = self.kwargs.get(self.startup_slug_url_kwarg)
            starup = get_object_or_404(
                Startup, slug__iexact=startup_slug)
            context = {
                self.startup_context_object_name:startup,
            }
        context.update(kwargs)
        return super().get_context_data(**context)


# class NewsLinkFormMixin():

#     def form_valid(self, form):
#         startup = get_object_or_404(
#             Startup,
#             slug__iexact=self.kwargs.get(
#                 self.startup_slug_url_kwarg))
#         self.object = form.save(
#             startup_obj=startup)
#         return HttpResponseRedirect(
#             self.get_success_url())

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         if self.request.method in ('POST', 'PUT'):
#             self.starup = get_object_or_404(Startup,
#                                             slug_iexact=self.kwargs.get(
#                                                 self.startup_slug_url_kwarg))
#             data = kwargs['data'].copy()
#             data.update({'startup':self.startup})
#             kwargs['data'] = data
#         return kwargs


































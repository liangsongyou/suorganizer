from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import HiddenInput

from .models import Tag, NewsLink, Startup


class SlugCleanMixin:

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError('Slug may not be "create"')
        return new_slug

class TagForm(SlugCleanMixin, forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

    def clean_name(self):
        return self.cleaned_data['name'].lower()
        

class NewsLinkForm(SlugCleanMixin, forms.ModelForm):
    class Meta:
        model = NewsLink
        fields = '__all__'
        widgets = {'starup':HiddenInput()}

    # def save(self, **kwargs):
    #     instance = super().save(commit=False)
    #     instance.startup = self.data.get('startup')
    #     instance.save()
    #     self.save_m2m()
    #     return instance

    # def clean(self):
    #     cleaned_data = super().claen()
    #     slug = cleaned_data.get('slug')
    #     startup_obj = self.data.get('startup')
    #     exists = (
    #         NewsLink.objects.filter(
    #             slug__iexact=slug,
    #             startup=startup_obj,
    #         ).exists())
    #     if exists:
    #         raise ValidationError(
    #             "News articles with this slug"
    #             "and Startup already exists.")
    #     else:
    #         return cleaned_data


class StartupForm(SlugCleanMixin, forms.ModelForm):
    class Meta:
        model = Startup
        fields = '__all__'
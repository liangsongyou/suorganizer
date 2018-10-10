from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.generic.dates import (
    DateMixin, MonthMixin as BaseMonthMixin,
    YearMixin as BaseYearMixin, _date_from_string)

from .models import Post


class AllowFuturePermissionMixin():

    def get_allow_future(self):
        return self.request.user.has_perm('blog.view_future_post')


class MonthMixin(BaseMonthMixin):
    month_format = '%m'
    month_query_kwarg = 'month'
    month_url_kwarg = 'month'

    def get_month(self):
        month = self.month
        if month is None:
            month = self.kwargs.get(
                self.month_url_kwarg,
                self.request.GET.get(
                    self.month_query_kwarg))
        if month is None:
            raise Http404("No month specified")
        return month
        

class YearMixin(BaseYearMixin):
    year_query_kwarg = 'year'
    year_url_kwarg = 'year'

    def get_year(self):
        year = self.year
        if year is None:
            year = self.kwargs.get(
                self.year_url_kwarg,
                self.request.GET.get(
                    self.year_query_kwarg))
        if year is None:
            raise Http404("No year specified")
        return year


class PostGetMixin:
    date_field = 'pub_date'
    model = Post
    month_url_kwarg = 'month'
    year_url_kwarg = 'year'
    slug_url_kwarg = 'slug'
    errors = {
        'url_kwargs':
            "Generic view {} must be called with "
            "year, month, and slug.",
        'not_exist':
            "No {} by that date and slug",
    }

    def get_object(self, queryset=None):
        year  = self.kwargs.get(self.year_url_kwarg)
        month = self.kwargs.get(self.month_url_kwarg)
        slug  = self.kwargs.get(self.slug_url_kwarg)
        if (year is None
                or month is None
                or slug is None):
            raise AttributeError(
                self.errors['url_kwargs'].format(self.__class__.__name__))
        date_field = self.date_field
        slug_field = self.get_slug_field()
        filter_dict = {
            date_field + '__year':year,
            date_field + '__month':month,
            slug_field:slug,
        }
        if queryset is None:
            queryset = self.get_queryset()
        queryset = queryset.filter(**filter_dict)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                self.errors['not_exist'].format(
                    queryset.model
                    ._meta.verbose_name))
        return obj


class DateObjectMixin(
        AllowFuturePermissionMixin,
        YearMixin, MonthMixin, DateMixin):

    def get_object(self, queryset=None):
        year = self.get_year()
        month = self.get_month()
        date = _date_from_string(
            year, self.get_year_format(),
            month, self.get_month_format(),
        )
        if queryset is None:
            queryset = self.get_queryset()
        if (not self.get_allow_future() 
                and date > date.today()):
            raise Http404(
                "Future {} not available because "
                "{}.allow_future is False."
                .format(
                    (queryset.model._meta.verbose_name_plural),
                    self.__class__.__name__))
        filter_dict = (
            self._make_single_date_lookup(date))
        queryset = queryset.filter(**filter_dict)
        return super().get_object(queryset=queryset)

    def _make_single_date_lookup(self, date):
        date_field = self.get_date_field()
        if self.uses_datetime_field:
            since = self._make_date_lookup_arg(date)
            until = self._make_date_lookup_arg(self._get_next_month(date))
            return {
                '%s__gte' % date_field: since,
                '%s__lt' % date_field: util
            }
        else:
            return {
                '%s__get' % date_field: date,
                '%s__lt' % date_field: self._get_next_month(date),
            }
































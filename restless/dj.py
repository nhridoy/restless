from django.conf import settings
from django.conf.urls import patterns, url
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .resources import Resource


class DjangoResource(Resource):
    # Because Django.
    @classmethod
    def as_list(self, *args, **kwargs):
        return csrf_exempt(super(DjangoResource, self).as_list(*args, **kwargs))

    @classmethod
    def as_detail(self, *args, **kwargs):
        return csrf_exempt(super(DjangoResource, self).as_detail(*args, **kwargs))

    def is_debug(self):
        # By default, Django-esque.
        return settings.DEBUG

    def build_response(self, data, status=200):
        # By default, Django-esque.
        resp = HttpResponse(data, content_type='application/json')
        resp.status_code = status
        return resp

    @classmethod
    def urls(cls, name_prefix=None):
        if name_prefix is None:
            name_prefix = 'api_{0}'.format(
                cls.__name__.replace('Resource', '').lower()
            )

        return patterns('',
            url(r'^$', cls.as_list(), name=name_prefix + '_list'),
            url(r'^(?P<pk>\d+)/$', cls.as_detail(), name=name_prefix + '_detail'),
        )

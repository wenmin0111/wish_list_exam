from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.main),
    url(r'^regist$', views.regist),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^create$', views.create),
    url(r'^update$', views.update),
    url(r'^items/(?P<id>\d+)$', views.show),
    url(r'^add/(?P<id>\d+)$', views.add),
    url(r'^remove/(?P<uID>\d+)/(?P<pID>\d+)$', views.remove),
    url(r'^delete/(?P<id>\d+)$', views.delete),
]

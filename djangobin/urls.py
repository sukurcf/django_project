from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
app_name='djangobin'
urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^user/(?P<username>[A-Za-z0-9]+)/$', views.profile, name='profile'),
    url('^trending/$', views.trending_snippets, name='trending_snippets'),
    url('^trending/(?P<language_slug>[\w]+)/$', views.trending_snippets, name='trending_snippets'),
    url('^(?P<snippet_slug>[\d.]+)/$', views.snippet_detail, name='snippet_detail'),
    url('^tag/(?P<tag>[\w-]+)/$', views.tag_list, name='tag_list'),
    url('^download/(?P<snippet_slug>[\d.]+)/$',views.download_snippet, name='download_snippet'),
    url('^raw/(?P<snippet_slug>[\d.]+)/$', views.raw_snippet, name='raw_snippet'),
    url('^contact/$', views.contact, name='contact'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^userdetails/$', views.user_details, name='user_details'),
    url(r'^signup/$', views.signup, name='signup')
]
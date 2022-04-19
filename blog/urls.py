from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<slug:slug>/edit', views.post_edit, name='post_edit'),
    path('post/about', views.post_about, name='post_about'),
    path('post/<slug:slug>/report', views.post_report, name='post_report'),
    path('post/<slug:slug>/approve', views.post_approve, name='post_approve'),
    path('post/<slug:slug>/delete', views.post_delete, name='post_delete'),
    path('post/<slug:slug>/show', views.post_show, name='post_show'),
    path('post/new-comment/<slug:slug>', views.new_comment, name='new_comment'),
    path('post/believer/<slug:slug>', views.post_believer, name='post_believer'),
    path('post/sceptic/<slug:slug>', views.post_sceptic, name='post_sceptic'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
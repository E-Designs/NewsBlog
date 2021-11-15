from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit', views.post_edit, name='post_edit'),
    path('post/about', views.post_about, name='post_about'),
    path('post/authors-posts/<int:find_author>', views.post_authors_posts, name='post_authors_posts'),
    path('post/<int:pk>/report', views.post_report, name='post_report'),
    path('post/<int:pk>/approve', views.post_approve, name='post_approve'),
    path('post/<int:pk>/delete', views.post_delete, name='post_delete'),
    path('post/<int:pk>/show', views.post_show, name='post_show'),
]
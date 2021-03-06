"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import imp
from django.contrib import admin
from django.urls import path, include, re_path
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from .sitemap import StaticSitemap, dynamicSitemap

from blog.models import Post

sitemaps = {'static': StaticSitemap, 'dynamic': dynamicSitemap}
#info_dict ={
   # 'queryset' : Post.objects.all(),

#}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register' ),
    path('profile/', user_views.profile, name='profile'),
    path('Terms-of-Use/', user_views.tou, name='tou'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/',
    auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'),
    name='password_reset'),
    path('path-reset/done/',
    auth_views.PasswordResetView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('password-reset-complete/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('', include('blog.urls')),
    path('', include('support.urls')),
    path('', include('games.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name ='django.contrib.sitemaps.views.sitemap', ),
    #re_path(r'^sitemap.xml$', cache_page(60)(sitemap_view), {'sitemaps': sitemaps }, name='cached-sitemap'),
    re_path(r'^robots\.txt', include('robots.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
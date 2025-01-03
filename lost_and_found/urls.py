"""
URL configuration for lost_and_found project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from items.views import home, report_lost, report_found, account
from django.contrib.auth import views as auth_views
from items import views as item_views
from django.contrib import messages

class CustomLogoutView(auth_views.LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'You have been successfully logged out.')
        return super().dispatch(request, *args, **kwargs)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('report-lost/', report_lost, name='report_lost'),
    path('report-found/', report_found, name='report_found'),
    path('register/', item_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='items/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(template_name='items/logout.html', next_page='home'), name='logout'),
    path('account/', account, name='account'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

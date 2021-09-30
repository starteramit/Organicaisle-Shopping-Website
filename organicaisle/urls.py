"""organicaisle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from organicaisleApp import views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('login/',views.login),
    path('loginPage/',views.loginPage),
    path('register/',views.register,name="register"),
    path('logout/',views.logout,name="logout"),
    path('AllProduct/',views.All_Product),
    path('productlist/',views.Single_Product),
    path('shipping_address/',views.shipping_address),
    path('search/',views.search,name="search"),
    path('myorder/',views.myorder,name="myorder"),
    path('cart/',views.cart,name="cart"),
    path('addtocart/',views.addtocart,name="addtocart"),
    path('remove/',views.remove),
    path('handlerequest/',views.handlerequest,name="handlerequest"),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name ="password_reset"),
    path('reset_password/done',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name="password_reset_confirm"),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name="password_reset_complete"),
]


urlpatterns=urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
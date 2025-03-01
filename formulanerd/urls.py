from rest_framework import routers
from django.contrib import admin
from django.urls import include, path 
from formulanerdapi.views import CircuitView
from formulanerdapi.views import NationView
from formulanerdapi.views import DriverView
from formulanerdapi.views import UserView
from formulanerdapi.views import RaceView
from formulanerdapi.views import ConstructorView
from formulanerdapi.views import DriverConstructorHistoryView
"""formulanerd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserView, 'user')
router.register(r'drivers', DriverView, 'driver')
router.register(r'circuits', CircuitView, 'circuit')
router.register(r'races', RaceView, 'race')
router.register(r'constructors', ConstructorView, 'constructor')
router.register(r'driver_constructor_histories', DriverConstructorHistoryView, 'driver_constructor_history')
router.register(r'nations', NationView, 'nation')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]

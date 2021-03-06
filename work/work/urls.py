"""work URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql", GraphQLView.as_view(graphiql=True)),
    path('api/projects/', include('projects.urls')),
    path('api/vendor/', include('vendor.urls')),
    path('api/procurement/', include('procurement.urls')),
    path('api/', get_schema_view(
        title="Work",
        description="API for all things …",
        version="0.0.1"
    ), name='openapi-schema'),
]

schema_view = get_schema_view(
    title='Server Monitoring API',
    url='https://localhost:8000/'
)

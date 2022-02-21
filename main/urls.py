from django.urls import path
from . import views
from graphene_django.views import GraphQLView
from .schema import schema
urlpatterns = [
    path('graphql', views.home,name='home'),
    path("", GraphQLView.as_view(graphiql=True, schema=schema)),

]
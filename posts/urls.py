from django.urls import path
from .views import PostListCreateView, PostDetailView

urlpatterns = [
    path("", PostListCreateView.as_view()),
    path("<slug:slug>/", PostDetailView.as_view()),
]
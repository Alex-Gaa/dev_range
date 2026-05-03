#C:\Users\Developer\PycharmProjects\devrange\posts\views.py
from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer


class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Post.objects.select_related("author").all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.select_related("author").all()
    lookup_field = "slug"
from django.db.models import Count
from rest_framework import generics, permissions, filters
from .models import Post
from .serializers import PostSerializer
from drf_api.permissions import IsOwnerOrReadOnly


class PostList(generics.ListCreateAPIView):

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = Post.objects.annotate(
        comments_count = Count('comment', distinct=True),
        likes_count = Count('likes', distinct=True)
    ).order_by('-created_at')
    serializer_class = PostSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = [
        'owner__username',
        'title',
        'content'
    ]
    ordering_fields = [
        'comments_count',
        'likes_count',
        'likes__created_at',
    ]
    

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count = Count('owner__comment', distinct=True),
        likes_count = Count('owner__like', distinct=True)
    ).order_by('-created_at')
    serializer_class = PostSerializer


# class PostList(APIView):

#     serializer_class = PostSerializer
#     permission_classes = [
#         permissions.IsAuthenticatedOrReadOnly
#         ]
    
#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(
#             posts, many=True, context={'request':request}
#         )
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = PostSerializer(
#             data = request.data, context={'request':request}
#         )
#         if serializer.is_valid():
#             serializer.save(owner=request.user)
#             return Response(
#                 serializer.data, status=status.HTTP_201_CREATED
#                 )
#         return Response(
#             serializer.errors, status=status.HTTP_400_BAD_REQUEST
#             )


# class PostDetail(APIView):
    
#     permission_classes = [IsOwnerOrReadOnly]
#     serializer_class = PostSerializer
    
#     def get_object(self, pk):
#         try:
#             post = Post.objects.get(pk=pk)
#             self.check_object_permissions(self.request, post)
#             return post
#         except Post.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         posts = self.get_object(pk)
#         serializer = PostSerializer(
#             posts, context={'request':request}
#         )
#         return Response(serializer.data)

#     def put(self, request, pk):
#         posts = self.get_object(pk)
#         serializer = PostSerializer(
#             posts, data=request.data, context={'request':request}
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(
#             status=status.HTTP_204_NO_CONTENT
#         )
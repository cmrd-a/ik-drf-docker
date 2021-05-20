from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response

from ik_drf.pagination import StandardResultsSetPagination
from .models import Entry, Like
from .serializers import EntrySerializer, EntryPrivateSerializer, LikeSerializer


class EntryView(generics.ListCreateAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = Entry.objects.all()
        page = self.paginate_queryset(queryset)
        serializer_class = EntrySerializer
        if request.user.is_superuser:
            serializer_class = EntryPrivateSerializer
        serializer = serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)


class EntryRetrieveView(generics.RetrieveAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        serializer_class = EntrySerializer
        if request.user.is_superuser:
            serializer_class = EntryPrivateSerializer
        entry = generics.get_object_or_404(queryset, pk=pk)
        serializer = serializer_class(entry)
        return Response(serializer.data)


class LikeView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class LikeRetrieveView(generics.RetrieveAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [AllowAny]

from rest_framework import viewsets

from .models import (
ArtWork
)

from .serializers import (
ArtWorkSerializer
)


class ArtsWorksViewSet(viewsets.ModelViewSet):
    queryset = ArtWork.objects.all()
    serializer_class = ArtWorkSerializer
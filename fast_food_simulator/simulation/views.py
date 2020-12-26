from .serializers import SimConfigSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets
from .tasks import start_simulator


class SimulatorViews(viewsets.ViewSet):
    """
    Start simulator API
    """

    def create(self, request):
        serializer = SimConfigSerializer(data=request.data)
        if serializer.is_valid():
            configs = serializer.data
            start_simulator.delay(**configs)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



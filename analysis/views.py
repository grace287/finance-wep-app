from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Analysis
from .serializers import AnalysisSerializer

class AnalysisListView(generics.ListAPIView):
    serializer_class = AnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Analysis.objects.filter(user=self.request.user)
        analysis_type = self.request.query_params.get('type', None)
        if analysis_type:
            queryset = queryset.filter(type=analysis_type)
        return queryset
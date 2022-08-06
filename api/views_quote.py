from rest_framework import generics, permissions
from .serializers_quote import QuoteSerializer, QuoteCreateSerializer
from quote.models import Quote as QuoteModel

class Quote(generics.ListAPIView):
    '''Employee view'''
    serializer_class = QuoteSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuoteModel.objects.filter(is_active=True).order_by('-number')

class QuoteCreate(generics.ListCreateAPIView):
    serializer_class = QuoteCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuoteModel.objects.all()
    
    def perform_create(self, serializer):
        number = self.request.POST['number']
        if QuoteModel.objects.filter(number=number).exists():
            return print('Project number already exist')
        else:
            serializer.save()

        

class QuoteRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuoteCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuoteModel.objects.all()

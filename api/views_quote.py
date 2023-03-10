from rest_framework import generics, permissions
from .serializers_quote import QuoteSerializer, QuoteCreateSerializer, QuoteToggleSerializer
from quote.models import Quote as QuoteModel
from project.models import ProjectCategory as ProjectCategoryModel
from project.models import ProjectType as ProjectTypeModel
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import time
from django.db.models import Sum

class Quote(generics.ListAPIView):
    '''Employee view'''
    serializer_class = QuoteSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuoteModel.objects.filter(is_active=True).order_by('-number')

class QuoteYear(generics.ListAPIView):
    '''Employee view'''
    serializer_class = QuoteSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        year = self.kwargs['year']

        return QuoteModel.objects.filter(is_active=True, created__year=year).order_by('-number')

class QuoteArchive(generics.ListAPIView):
    '''Employee view'''
    serializer_class = QuoteSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        year = self.kwargs['year']
        return QuoteModel.objects.filter(is_active=False, created__year=year).order_by('-number')

class QuoteToggleArchive(generics.UpdateAPIView):
    '''Toggle Archive'''
    serializer_class = QuoteToggleSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuoteModel.objects.all()
    
    def perform_update(self, serializer):
        serializer.instance.is_active=not(serializer.instance.is_active)
        serializer.save()

class QuoteCreate(generics.ListCreateAPIView):
    serializer_class = QuoteCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuoteModel.objects.all()
    
    def perform_create(self, serializer):
        # number = self.request.POST['number']
        # if QuoteModel.objects.filter(number=number).exists():
        #     return print('Project number already exist')
        # else:
            serializer.save()

class QuoteRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuoteCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuoteModel.objects.all()


@csrf_exempt
def NextQuoteNumber(request):
    '''Get the Next Quote Number'''
    year = time.strftime("%Y")[2:]
    if request.method == 'GET':
        #! what if its not sequential and we manually enter old quote?? 
        try:
            last_quote = model_to_dict(QuoteModel.objects.all().order_by('-number').first())  # omitted filter active. Might be an issue when DB gets large?
            
            last_quote_number = (last_quote['number'])
            current_quote_year = last_quote_number[1:3]

            if current_quote_year == year:
                next_number = int(last_quote_number[4:])+1
                for i in range(3):
                    if len(str(next_number)) < 3:
                        next_number = '0' + str(next_number)
                next_number_str = f'Q{current_quote_year}-{str(next_number)}'
            else:
                next_number = '001'
                next_number_str = f'Q{year}-{str(next_number)}'
        
        except AttributeError: 
            #if database is empty
            last_quote_number = None  #Doesn't exist, set to None
            next_number_str = f'Q{year}-001'

        return JsonResponse({'next_quote_number': str(next_number_str)}, status=201)

@csrf_exempt
def LastQuote(request):
    '''Get the Last Quote Number'''
    if request.method == 'GET':
        last_quote = model_to_dict(QuoteModel.objects.filter(is_active=True).order_by('-number').first())
        
        last_quote_id = (last_quote['id'])

        return JsonResponse({'last_quote_id': str(last_quote_id)}, status=201)

@csrf_exempt
def QuoteData(request, year):
    '''Get totals for project_category and project_type'''

    if request.method == 'GET':
        data = {'count': 0}
        # sum = QuoteModel.objects.aggregate(Sum('price'))
        # sum = QuoteModel.objects.aggregate(Sum('project_category'))

        quotes = QuoteModel.objects.filter(created__year=year).order_by('-number')
        category_object = ProjectCategoryModel.objects.all().values()
        type_object = ProjectTypeModel.objects.all().values()
        
        
        data['count'] = str(quotes.count())

        # print(category_object)
        # print(type_object)
        
        # category_object = ProjectCategoryModel.objects.all().values()

        # for i in category_object:
        #     print(i['id'], i['name'])
        
        # last_quote = model_to_dict(QuoteModel.objects.filter(is_active=True).order_by('-number').first())
        # last_quote_id = (last_quote['id'])
        return JsonResponse(data, status=201)


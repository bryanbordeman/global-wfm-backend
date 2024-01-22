from rest_framework import generics, permissions
from .serializers_quote import QuoteSerializer, QuoteCreateSerializer, QuoteToggleSerializer
from quote.models import Quote as QuoteModel
from project.models import Project as ProjectModel
from project.models import HSE as HSEModel
from project.models import Service as ServiceModel
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

        return QuoteModel.objects.filter(is_active=True, number__startswith=f'Q{str(year)[-2:]}').order_by('-number')

class QuoteArchive(generics.ListAPIView):
    '''Employee view'''
    serializer_class = QuoteSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        year = self.kwargs['year']
        return QuoteModel.objects.filter(is_active=False, number__startswith=f'Q{str(year)[-2:]}').order_by('-number')

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
            last_quote = model_to_dict(QuoteModel.objects.all().order_by('-number').first()) # omitted filter active. Might be an issue when DB gets large?

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
        data = {'quote_count': 0,
                'project_count': 0,
                'hse_count': 0,
                'service_count': 0,
                'outstanding_sales_sum': 0,
                'sold_sales_sum': 0,
                'projects_sold_sales_sum': 0,
                'hses_sold_sales_sum': 0,
                'services_sold_sales_sum': 0
                }

        # Calculate outstanding sales sum
        outstanding_sales_sum = QuoteModel.objects.filter(is_active=True, number__startswith=f'Q{str(year)[-2:]}').aggregate(Sum('price'))
        data['outstanding_sales_sum'] = round(outstanding_sales_sum['price__sum'] or 0, 2)

        hse_substring_to_check = "HSE" + str(year)[-2:]
        service_substring_to_check = "SVC" + str(year)[-2:]

        # Calculate sold sales sum
        projects_sold_sales_sum = ProjectModel.objects.filter(number__endswith=str(year)[-2:]).aggregate(Sum('price'))
        hses_sold_sales_sum = HSEModel.objects.filter(number__startswith=hse_substring_to_check).aggregate(Sum('price'))
        services_sold_sales_sum = ServiceModel.objects.filter(number__startswith=service_substring_to_check).aggregate(Sum('price'))

        sold_sales_sum = (float(projects_sold_sales_sum['price__sum'] or 0) +
                        float(hses_sold_sales_sum['price__sum'] or 0) +
                        float(services_sold_sales_sum['price__sum'] or 0))

        data['sold_sales_sum'] = round(sold_sales_sum, 2)
        data['projects_sold_sales_sum'] = projects_sold_sales_sum
        data['hses_sold_sales_sum'] = hses_sold_sales_sum
        data['services_sold_sales_sum'] = services_sold_sales_sum


        # Count quotes and projects
        quotes = QuoteModel.objects.filter(number__startswith=f'Q{str(year)[-2:]}').order_by('-number')
        projects = ProjectModel.objects.filter(number__endswith=str(year)[-2:]).order_by('-number')
        HSE = HSEModel.objects.filter(number__startswith=hse_substring_to_check).order_by('-number')
        service = ServiceModel.objects.filter(number__startswith=service_substring_to_check).order_by('-number')

        data['quote_count'] = quotes.count()
        data['project_count'] = projects.count() + HSE.count() + service.count()
        data['hse_count'] = HSE.count()
        data['service_count'] = service.count()

        return JsonResponse(data, status=200)
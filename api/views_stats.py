from django.http import JsonResponse
from quote.models import Quote as QuoteModel
from project.models import Project as ProjectModel
from project.models import Service as ServiceModel
from project.models import HSE as HSEModel
from project.models import ProjectCategory as ProjectCategoryModel
from project.models import ProjectType as ProjectTypeModel

from worksegment.models import WorkSegment, WorkType
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def Stats(request, year):
    '''Get statistics from DB'''

    if request.method == 'GET':
        try:
            # create variables

            qs_quotes = QuoteModel.objects.filter(created__year=year).order_by('-number')
            total_quotes = qs_quotes.count()

            qs_projects = ProjectModel.objects.filter(created__year=year).order_by('-number')
            total_projects = qs_projects.count()

            qs_services = ServiceModel.objects.filter(created__year=year).order_by('-number')
            total_services = qs_services.count()

            qs_hses = HSEModel.objects.filter(created__year=year).order_by('-number')
            total_hses = qs_hses.count()

            if(total_quotes > 0 and total_projects > 0): 
                total_sales_closed = round((total_projects + total_services + total_hses)/ total_quotes, 2)
            else:
                total_sales_closed = 0

            stats = {
                'total_quotes': total_quotes, 
                'total_projects': total_projects,
                'total_services': total_services,  
                'total_hses': total_hses, 
                'total_sales_closed': total_sales_closed 
            }

            #! Projects
            # total projects 
            # totals types of projects

            #! Quotes
            # total quotes
            # totals types of quotes
            # total sales closed (project total divided in quote total)

            #! Production
            # total OT hours

        except AttributeError: 
            #if database is empty
            stats ={}  #Doesn't exist, set to None

        return JsonResponse(stats, json_dumps_params={'indent': 2}, safe=False)
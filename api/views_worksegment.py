from rest_framework import generics, permissions
from .serializers_worksegment import WorkSegmentSerializer, WorkSegmentApprovedSerializer, WorkSegmentsWeekSerializer
from .serializers_worksegment import WorkTypeSerializer, PTOSerializer, PTOApprovedSerializer, PTOWeekSerializer, WorkSegmentDepthSerializer
from worksegment.models import WorkSegment, WorkType, PTO
from employee.models import Employee
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from collections import defaultdict

class PTOs(generics.ListAPIView):
    '''Employee view'''
    serializer_class = PTOSerializer

    def get_queryset(self):
        user = self.request.user
        return PTO.objects.filter(user=user).order_by('-date')

class PTOCreate(generics.ListCreateAPIView):
    serializer_class = PTOSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return PTO.objects.all()
        else:
            return PTO.objects.filter(user=user).order_by('-user')

    def perform_create(self, serializer):
        user_id = self.kwargs['user_id']
        user = User.objects.filter(id=user_id)[0]
        serializer.save(user=user)

class PTORetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PTOSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return PTO.objects.all()
        else:
            # user can only update =, delete own posts
            return PTO.objects.filter(user=user)

class PTOToggleApproved(generics.UpdateAPIView):
    '''Approve hours. Admin view only'''
    serializer_class = PTOApprovedSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PTO.objects.all()
    
    def perform_update(self, serializer):
        serializer.instance.is_approved=not(serializer.instance.is_approved)
        serializer.save()

class PTOWeek(generics.ListAPIView):
    '''get all PTO's for particular isoweek. Employee view'''
    serializer_class = PTOWeekSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        isoweek = self.kwargs['isoweek']
        return PTO.objects.filter(isoweek=isoweek, user=user).order_by('-date')

class AdminPTOWeek(generics.ListAPIView):
    '''get all PTOs for particular isoweek. Admin view only'''
    serializer_class = PTOWeekSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        isoweek = self.kwargs['isoweek']
        qs = PTO.objects.filter(isoweek=isoweek).order_by('-user', '-date')
        user = self.request.user
        return qs if user.is_staff else qs.filter(id=user.id)

##### Worksergments below #####

class WorkTypes(generics.ListAPIView):
    '''Employee view'''
    serializer_class = WorkTypeSerializer

    def get_queryset(self):
        return WorkType.objects.all()

class WorkSegments(generics.ListAPIView):
    '''Employee view'''
    serializer_class = WorkSegmentSerializer

    def get_queryset(self):
        user = self.request.user
        return WorkSegment.objects.filter(user=user).order_by('-date')

class WorkSegmentCreate(generics.ListCreateAPIView):
    serializer_class = WorkSegmentSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return WorkSegment.objects.all()
        else:
            return WorkSegment.objects.filter(user=user).order_by('-user')

    def perform_create(self, serializer):
        user_id = self.kwargs['user_id']
        user = User.objects.filter(id=user_id)[0]
        serializer.save(user=user)


class WorkSegmentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    # serializer_class = WorkSegmentSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            # Use serializer class for incoming data
            return WorkSegmentSerializer
        else:
            # Use serializer class for outgoing data
            return WorkSegmentDepthSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return WorkSegment.objects.all()
        else:
            # user can only update =, delete own posts
            return WorkSegment.objects.filter(user=user)

class WorkSegmentToggleApproved(generics.UpdateAPIView):
    '''Approve hours. Admin view only'''
    serializer_class = WorkSegmentApprovedSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # user = self.request.user
        # return WorkSegment.objects.filter(user=user)
        return WorkSegment.objects.all()
    
    def perform_update(self, serializer):
        serializer.instance.is_approved=not(serializer.instance.is_approved)
        serializer.save()

class WorkSegmentsWeek(generics.ListAPIView):
    '''get all worksegments for particular isoweek. Admin view only'''
    serializer_class = WorkSegmentsWeekSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        isoweek = self.kwargs['isoweek']
        return WorkSegment.objects.filter(isoweek=isoweek, user=user).order_by('-date','start_time')

class AdminWorkSegmentsWeek(generics.ListAPIView):
    '''get all worksegments for particular isoweek. Admin view only'''
    serializer_class = WorkSegmentsWeekSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        isoweek = self.kwargs['isoweek']
        qs = WorkSegment.objects.filter(isoweek=isoweek).order_by('-user', '-date')
        user = self.request.user
        return qs if user.is_staff else qs.filter(id=user.id)

class WorkSegmentsProject(generics.ListAPIView):
    '''Get total duration for each segment_type for a particular project.'''
    serializer_class = WorkSegmentsWeekSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        project_number = self.kwargs['project_number']

        if(project_number[:3] == 'SVC'):
            queryset = WorkSegment.objects.filter(service__number=project_number)
        elif(project_number[:3] == 'HSE'):
            queryset = WorkSegment.objects.filter(hse__number=project_number)
        else:
            queryset = WorkSegment.objects.filter(project__number=project_number)

        # Calculate total duration for each segment_type
        total_durations = defaultdict(float)
        for work_segment in queryset:
            segment_type_name = work_segment.segment_type.name
            duration = float(work_segment.duration)
            total_durations[segment_type_name] += duration

        # Return the total durations as a Response
        return Response(total_durations)
    
@csrf_exempt
def WorksegmentTotals(request, isoweek):
    '''Get total time for week'''
    if request.method == 'GET':
        try:
            # create variables
            total_list = []
            users = {}
            qs = WorkSegment.objects.filter(isoweek=isoweek).order_by('user__last_name', 'user__first_name')
            qs_pto = PTO.objects.filter(isoweek=isoweek).order_by('-user')

            qs_list = [i for i in qs]
            qs_pto_list = [i for i in qs_pto]

            for i in qs_list:
                users[f'{i.user.id}'] = {'user_name': f'{i.user.first_name} {i.user.last_name}','total_duration': 0, 'overtime': 0, 'regular': 0, 'travel': 0, 'sick': 0, 'vacation': 0, 'holiday': 0}

            # if no worksegments and PTO logged
            for item in qs_pto_list:
                if item.user.id in users:
                    continue
                else:
                    users[f'{item.user.id}'] = {'user_name': f'{item.user.first_name} {item.user.last_name}','total_duration': 0, 'overtime': 0, 'regular': 0, 'travel': 0, 'sick': 0, 'vacation': 0,'holiday': 0 }


            for item in qs_pto_list:
                for key in users:
                    if item.user.id == int(key) and item.PTO_type == 'Vacation':
                        users[f'{item.user.id}']['vacation'] += item.duration
                    elif item.user.id == int(key) and item.PTO_type == 'Sick':
                        users[f'{item.user.id}']['sick'] += item.duration
                    elif item.user.id == int(key) and item.PTO_type == 'Holiday':
                        users[f'{item.user.id}']['holiday'] += item.duration

            for item in qs_list:
                for key in users:
                    if item.user.id == int(key):
                        users[f'{item.user.id}']['total_duration'] += item.duration
                        if item.travel_duration:
                            users[f'{item.user.id}']['travel'] += item.travel_duration

            for k, v in users.items():
                v['regular'] = v['total_duration'] - v['travel']
                if v['regular'] > 40:
                    v['overtime'] = v['regular'] - 40
                    v['regular'] = float(40.00)
                if v['vacation'] > 0:
                    v['total_duration'] = v['total_duration'] + v['vacation']
                if v['sick'] > 0:
                    v['total_duration'] = v['total_duration'] + v['sick']
                if v['holiday'] > 0:
                    v['total_duration'] = v['total_duration'] + v['holiday']

                totals = {'user_id': k,
                        'user_name': str(v['user_name']),
                        'isoweek': isoweek,
                        'total_duration': str(v['total_duration']),
                        'regular': str("{:.2f}".format(v['regular'])),
                        'overtime' : str(v['overtime']),
                        'travel': str(v['travel']),
                        'sick': str(v['sick']),
                        'vacation': str(v['vacation']),
                        'holiday': str(v['holiday'])
                        }

                total_list.append(totals)

        except AttributeError:
            #if database is empty
            total_list = []  #Doesn't exist, set to None

        return JsonResponse(total_list, json_dumps_params={'indent': 2}, safe=False)

@csrf_exempt
def PayrollTotals(request, isoweek):
    '''Get total time for week'''
    if request.method == 'GET':
        try:
            projects_dict = {}
            user_hours = defaultdict(int)  # Dictionary to keep track of total hours worked by each user
            qs = WorkSegment.objects.filter(isoweek=isoweek, is_approved=True).order_by('user__last_name', 'date', 'user__id', 'project', 'service', 'quote', 'hse')

            for i in qs:
                if i.project:
                    if i.project.id not in projects_dict:
                        projects_dict[i.project.id] = {
                            'project_id': i.project.id,
                            'project_number': i.project.number,
                            'project_name': i.project.name,
                            'service_id': None,
                            'service_number': None,
                            'service_name': None,
                            'quote_id': None,
                            'quote_number': None,
                            'quote_name': None,
                            'hse_id': None,
                            'hse_number': None,
                            'hse_name': None,
                            'segments': [],
                            'prevailing_rate': i.project.prevailing_rate
                        }
                if i.service:
                    if i.service.id not in projects_dict:
                        projects_dict[i.service.id] = {
                            'project_id': None,
                            'project_number': None,
                            'project_name': None,
                            'service_id': i.service.id,
                            'service_number': i.service.number,
                            'service_name': i.service.name,
                            'quote_id': None,
                            'quote_number': None,
                            'quote_name': None,
                            'hse_id': None,
                            'hse_number': None,
                            'hse_name': None,
                            'segments': [],
                            'prevailing_rate': i.service.prevailing_rate
                        }
                if i.quote:
                    if i.quote.id not in projects_dict:
                        projects_dict[i.quote.id] = {
                            'project_id': None,
                            'project_number': None,
                            'project_name': None,
                            'service_id': None,
                            'service_number': None,
                            'service_name': None,
                            'quote_id': i.quote.id,
                            'quote_number': i.quote.number,
                            'quote_name': i.quote.name,
                            'hse_id': None,
                            'hse_number': None,
                            'hse_name': None,
                            'segments': [],
                            'prevailing_rate': False  # Update this as needed
                        }
                if i.hse:
                    if i.hse.id not in projects_dict:
                        projects_dict[i.hse.id] = {
                            'project_id': None,
                            'project_number': None,
                            'project_name': None,
                            'service_id': None,
                            'service_number': None,
                            'service_name': None,
                            'quote_id': None,
                            'quote_number': None,
                            'quote_name': None,
                            'hse_id': i.hse.id,
                            'hse_number': i.hse.number,
                            'hse_name': i.hse.name,
                            'segments': [],
                            'prevailing_rate': i.hse.prevailing_rate
                        }

                # Calculate total hours worked by the user excluding travel hours
                work_hours = i.duration - i.travel_duration
                user_hours[i.user.id] += work_hours


                prevailing_rate = False
                if i.project:
                    prevailing_rate = i.project.prevailing_rate
                elif i.service:
                    prevailing_rate = i.service.prevailing_rate
                elif i.quote:
                    prevailing_rate = i.quote.prevailing_rate
                elif i.hse:
                    prevailing_rate = i.hse.prevailing_rate

                # Initialize doubletime
                doubletime = 0
                # Determine if the hours are regular, overtime, or doubletime
                day_of_week = i.date.weekday()
                if prevailing_rate and i.segment_type_id == 2:
                    if work_hours > 8:
                        regular = 8
                        overtime = work_hours - 8
                    else:
                        regular = work_hours
                        overtime = 0
                    accumulated_regular += regular
                elif day_of_week == 5:  # Saturday
                    regular = 0
                    overtime = work_hours
                    accumulated_regular += regular
                elif day_of_week == 6:  # Sunday
                    regular = 0
                    overtime = 0
                    doubletime = work_hours
                else:
                    if user_hours[i.user.id] <= 40:
                        regular = work_hours
                        overtime = 0
                        accumulated_regular = user_hours[i.user.id]
                    else:
                        if user_hours[i.user.id] - work_hours < 40:
                            regular = 40 - (user_hours[i.user.id] - work_hours)
                            overtime = work_hours - regular
                            accumulated_regular = 40
                        else:
                            regular = 0
                            overtime = work_hours
                            accumulated_regular = user_hours[i.user.id]
                
                try:
                    employee = Employee.objects.get(user_id=i.user.id)
                    rate = employee.rate
                except ObjectDoesNotExist:
                    rate = None

                segment = {
                    'segment_type_id': i.segment_type.id,
                    'segment_type_name': i.segment_type.name,
                    'user_id': i.user.id,
                    'employee': f'{i.user.last_name}, {i.user.first_name}',
                    'date': i.date,
                    'start_time': i.start_time,
                    'end_time': i.end_time,
                    'lunch': i.lunch,
                    'travel_duration': i.travel_duration,
                    'total_duration': i.duration,
                    'regular': regular,
                    'overtime': overtime,
                    'doubletime': doubletime,
                    'accumulated_regular': accumulated_regular,
                    'notes': i.notes,
                    'prevailing_rate': prevailing_rate,
                    'rate': rate 
                }

                if i.project and i.project.id in projects_dict:
                    projects_dict[i.project.id]['segments'].append(segment)
                if i.service and i.service.id in projects_dict:
                    projects_dict[i.service.id]['segments'].append(segment)
                if i.quote and i.quote.id in projects_dict:
                    projects_dict[i.quote.id]['segments'].append(segment)
                if i.hse and i.hse.id in projects_dict:
                    projects_dict[i.hse.id]['segments'].append(segment)

        except AttributeError:
            projects_dict = {}

        # Condense segments for each project
        for project in projects_dict.values():
            project['segments'] = condense_segments(project['segments'])

        return JsonResponse(list(projects_dict.values()), json_dumps_params={'indent': 2}, safe=False)

def condense_segments(segments):
    condensed_segments = defaultdict(lambda: {'user_id': None, 'segment_type_name': None, 'segment_type_id': None, 'employee': None, 'regular': 0, 'overtime': 0, 'doubletime': 0, 'travel_duration': 0})

    for segment in segments:
        user_id = segment['user_id']
        segment_type_id = segment['segment_type_id']
        segment_type_name = segment['segment_type_name']
        key = (user_id, segment_type_id)  # Group by both user_id and segment_type_id

        condensed_segments[key]['user_id'] = user_id
        condensed_segments[key]['segment_type_id'] = segment_type_id
        condensed_segments[key]['segment_type_name'] = segment_type_name
        condensed_segments[key]['employee'] = segment['employee']
        condensed_segments[key]['regular'] += float(segment['regular'])
        condensed_segments[key]['overtime'] += float(segment['overtime'])
        condensed_segments[key]['doubletime'] += float(segment['doubletime'])
        condensed_segments[key]['travel_duration'] += float(segment['travel_duration'])
        condensed_segments[key]['prevailing_rate'] = segment_type_id == 2 and segment['prevailing_rate']
        condensed_segments[key]['base_rate'] = segment['rate']
        condensed_segments[key]['pr_rate'] = segment['rate'] if segment_type_id == 2 and segment['prevailing_rate'] else None

    return list(condensed_segments.values())
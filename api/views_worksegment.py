from rest_framework import generics, permissions
from .serializers_worksegment import WorkSegmentSerializer, WorkSegmentApprovedSerializer, WorkSegmentsWeekSerializer
from .serializers_worksegment import WorkTypeSerializer, PTOSerializer, PTOApprovedSerializer, PTOWeekSerializer, WorkSegmentDepthSerializer
from worksegment.models import WorkSegment, WorkType, PTO
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def WorksegmentTotals(request, isoweek):
    '''Get total time for week'''
    if request.method == 'GET':
        try:
            # create variables
            total_list = []
            users = {}
            qs = WorkSegment.objects.filter(isoweek=isoweek).order_by('user__last_name')
            qs_pto = PTO.objects.filter(isoweek=isoweek).order_by('-user')

            qs_list = [i for i in qs]
            qs_pto_list = [i for i in qs_pto]

            for i in qs_list:
                users[f'{i.user.id}'] = {'user_name': f'{i.user.first_name} {i.user.last_name}','total_duration': 0, 'overtime': 0, 'regular': 0, 'travel': 0, 'sick': 0, 'vacation': 0}

            # if no worksegments and PTO logged
            for item in qs_pto_list:
                if item.user.id in users:
                    continue
                else:
                    users[f'{item.user.id}'] = {'user_name': f'{item.user.first_name} {item.user.last_name}','total_duration': 0, 'overtime': 0, 'regular': 0, 'travel': 0, 'sick': 0, 'vacation': 0}


            for item in qs_pto_list:
                for key in users:
                    if item.user.id == int(key) and item.PTO_type == 'Vacation':
                        users[f'{item.user.id}']['vacation'] += item.duration
                    elif item.user.id == int(key) and item.PTO_type == 'Sick':
                        users[f'{item.user.id}']['sick'] += item.duration

            for item in qs_list:
                for key in users:
                    if item.user.id == int(key):
                        users[f'{item.user.id}']['total_duration'] += item.duration
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

                totals = {'user_id': k,
                        'user_name': str(v['user_name']),
                        'isoweek': isoweek,
                        'total_duration': str(v['total_duration']),
                        'regular': str("{:.2f}".format(v['regular'])),
                        'overtime' : str(v['overtime']),
                        'travel': str(v['travel']),
                        'sick': str(v['sick']),
                        'vacation': str(v['vacation'])}

                total_list.append(totals)

        except AttributeError:
            #if database is empty
            total_list = []  #Doesn't exist, set to None

        return JsonResponse(total_list, json_dumps_params={'indent': 2}, safe=False)
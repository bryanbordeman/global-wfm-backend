from rest_framework import generics, permissions
from .serializers_worksegment import WorkSegmentSerializer, WorkSegmentApprovedSerializer, WorkSegmentsWeekSerializer
from worksegment.models import WorkSegment
from django.contrib.auth.models import User

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
    serializer_class = WorkSegmentSerializer
    permissions_classes = [permissions.IsAuthenticated]

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
        return WorkSegment.objects.filter(isoweek=isoweek, user=user).order_by('-start_time', '-date')

class AdminWorkSegmentsWeek(generics.ListAPIView):
    '''get all worksegments for particular isoweek. Admin view only'''
    serializer_class = WorkSegmentsWeekSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        isoweek = self.kwargs['isoweek']
        qs = WorkSegment.objects.filter(isoweek=isoweek).order_by('-user')
        
        qs_list = [i for i in qs]
        users = {}
        for i in qs_list:
            users[f'{i.user.username}'] = {'total_duration': 0, 'overtime': 0, 'regular': 0, 'travel': 0}
        
        for item in qs_list:
            for key in users:
                if item.user.username == key:
                    users[f'{item.user.username}']['total_duration'] += item.duration
                    users[f'{item.user.username}']['travel'] += item.travel_duration
                    # print(item)
        for k, v in users.items():
            v['regular'] = v['total_duration'] - v['travel']
            if v['regular'] > 40:
                v['overtime'] = v['regular'] - 40
                v['regular'] = 40
            print(k, v['total_duration'], v['regular'],v['overtime'],v['travel'])
    
        user = self.request.user
        return qs if user.is_staff else qs.filter(id=user.id)

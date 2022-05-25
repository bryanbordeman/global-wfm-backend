from rest_framework import generics, permissions
from .serializers import WorkSegmentSerializer, WorkSegmentApprovedSerializer, WorkSegmentsWeekSerializer
from .serializers import AnnouncementSerializer
from worksegment.models import WorkSegment
from announcement.models import Announcement as AnnouncementModel
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
import json

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
        user = self.request.user
        if user.is_staff:
            user_id = self.kwargs['user_id']
            user = User.objects.filter(id=user_id)[0]
            serializer.save(user=user)
        else:
            user = self.request.user
            serializer.save(user=self.request.user)

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
        return WorkSegment.objects.filter(isoweek=isoweek, user=user).order_by('-date', '-start_time')

    # def get_queryset(self):
    #     isoweek = self.kwargs['isoweek']
    #     qs = WorkSegment.objects.filter(isoweek=isoweek).order_by('-user')

    #     user = self.request.user
    #     return qs if user.is_superuser else qs.filter(id=user.id)

class AdminWorkSegmentsWeek(generics.ListAPIView):
    '''get all worksegments for particular isoweek. Admin view only'''
    serializer_class = WorkSegmentsWeekSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        isoweek = self.kwargs['isoweek']
        qs = WorkSegment.objects.filter(isoweek=isoweek).order_by('-user')

        user = self.request.user
        return qs if user.is_staff else qs.filter(id=user.id)

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request) # data is a dictionary
            user = User.objects.create_user(
                username=data['username'],
                password=data['password']
            )
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token' : str(token)}, status=201)
        except IntegrityError:
            return JsonResponse(
                {'error' : 'username taken. Choose another username'}, status=400
            )

@csrf_exempt
def login(request):
    if request.method == 'POST':
            data = JSONParser().parse(request) # data is a dictionary
            user = authenticate(
                request,
                username=data['username'],
                password=data['password']
            )
            if user is None:
                return JsonResponse(
                {'error' : 'unable to login. check username and password'}, status=400
            )
            else: #return user token
                try:
                    token = Token.objects.get(user=user)
                    user_information = User.objects.get(id=user.id)
                    all_users_object = User.objects.all()

                    users = {}

                    for item in all_users_object:
                        users[f'{item.first_name} {item.last_name}'] = {'id': item.id, 
                        'username': item.username,
                        'email': item.email,
                        'first_name': item.first_name,
                        'last_name': item.last_name,
                        'is_staff': item.is_staff}
                    
                    users_json_object = json.dumps(users, indent = 4)
                    
                except: #if token not in db, create a new one
                    token = Token.objects.create(user=user)
            if user.is_staff:
                print(all_users_object)
                return JsonResponse({'token' : str(token), 
                                    'user' : str(user_information.username),
                                    'user_email' : str(user_information.email),
                                    'user_first_name' : str(user_information.first_name),
                                    'user_last_name' : str(user_information.last_name),
                                    'user_is_staff' : str(user_information.is_staff),
                                    'users' : users_json_object
                                    }, status=201)
            else:
                print('not staff')
                return JsonResponse({'token' : str(token), 
                                    'user' : str(user_information.username),
                                    'user_email' : str(user_information.email),
                                    'user_first_name' : str(user_information.first_name),
                                    'user_last_name' : str(user_information.last_name),
                                    'user_is_staff' : str(user_information.is_staff),
                                    }, status=201)

class Announcement(generics.ListAPIView):
    '''Employee view'''
    serializer_class = AnnouncementSerializer

    def get_queryset(self):
        return AnnouncementModel.objects.filter(is_active=True).order_by('-created')
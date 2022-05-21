from rest_framework import generics, permissions
from .serializers import WorkSegmentSerializer, WorkSegmentApprovedSerializer, WorkSegmentsWeekSerializer
from worksegment.models import WorkSegment
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

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
        return WorkSegment.objects.filter(user=user).order_by('-user')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WorkSegmentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkSegmentSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # user can only update =, delete own posts
        return WorkSegment.objects.filter(user=user)

class WorkSegmentToggleApproved(generics.UpdateAPIView):
    '''Approve hours. Admin view only'''
    serializer_class = WorkSegmentApprovedSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return WorkSegment.objects.filter(user=user)
    
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
        return WorkSegment.objects.filter(isoweek=isoweek, user=user).order_by('-date')

    # def get_queryset(self):
    #     isoweek = self.kwargs['isoweek']
    #     qs = WorkSegment.objects.filter(isoweek=isoweek).order_by('-user')

    #     user = self.request.user
    #     return qs if user.is_superuser else qs.filter(id=user.id)

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
                    print(str(user_information.is_staff))
                except: #if token not in db, create a new one
                    token = Token.objects.create(user=user)
            return JsonResponse({'token' : str(token), 
                                'user' : str(user_information.username),
                                'user_email' : str(user_information.email),
                                'user_first_name' : str(user_information.first_name),
                                'user_last_name' : str(user_information.last_name),
                                'user_is_staff' : str(user_information.is_staff),
                                }, status=201)
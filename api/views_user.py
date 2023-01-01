from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
import json
from django.forms.models import model_to_dict

from rest_framework import generics, permissions
from .serializers_user import UserSerializer
from django.contrib.auth.models import User

class UserView(generics.ListAPIView):
    '''Employee view'''
    serializer_class = UserSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(is_active=True).all().order_by('first_name')

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
                    # user_information = User.objects.get(id=user.id)
                    dict_obj = model_to_dict( User.objects.get(id=user.id) )
                    keys = ['id', 'username', 'first_name', 'last_name', 'is_staff', 'email', 'groups']
                    filtered = dict(zip(keys, [dict_obj[k] for k in keys]))
                    jsonObject = json.dumps(filtered, default=lambda o: o.__dict__, sort_keys=True, indent=2)
                    # print(jsonObject)
                    
                    
                except: #if token not in db, create a new one
                    token = Token.objects.create(user=user)

            return JsonResponse({'token' : str(token), 
                                'userObject' : str(jsonObject),
                                # 'user' : str(user_information.username),
                                # 'user_email' : str(user_information.email),
                                # 'user_first_name' : str(user_information.first_name),
                                # 'user_last_name' : str(user_information.last_name),
                                # 'user_is_staff' : str(user_information.is_staff),
                                }, status=201)

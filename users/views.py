import re
import jwt
import json
import bcrypt
import logging
from json.decoder import JSONDecodeError
from django.http  import JsonResponse
from django.views import View
from users.models import User
from my_settings import SECRET_KEY, ALGORITHM



logger = logging.getLogger('django')
class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            name = data['name']
            email = data['email']
            password = data['password']

            if not re.match('^[a-zA-Z가-힣]{2,30}$', name):
                return JsonResponse({'MESSAGE' : 'WRONG NAME FORMAT'}, status = 400)
            
            if not re.match('^[a-zA-Z\d+-.]+@[a-zA-Z\d+-.]+\.[a-zA-Z]{2,3}$', email):
                return JsonResponse({'MESSAGE' : 'WRONG EMAIL FORMAT'}, status=400)

            if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{10,20}$',password):
                return JsonResponse({'MESSAGE' : 'WRONG PASSWORD FORMAT'}, status = 400)

            if User.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE':'EMAIL ALREADY EXISTS'}, status = 400)

            decoded_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            User.objects.create(
                name     = name,
                email    = email,
                password = decoded_password,
            )
            
            return JsonResponse({'MESSAGE':'SUCCESSFULLY REGISTERED'}, status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status = 400)

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "EMAIL_DOES_NOT_EXISTS"}, status=403)
            
            current_user = User.objects.get(email=data['email'])
            
            if not bcrypt.checkpw(data['password'].encode(), current_user.password.encode()):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=403)
                
            token = jwt.encode({"id": current_user.id}, SECRET_KEY, algorithm=ALGORITHM)
            
            return JsonResponse({
                "MESSAGE"   : "SUCCESS",
                "user_name" : current_user.name,
                "auth_token": token,
            }, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"MESSAGE": "VALUE_ERROR"}, status=400)
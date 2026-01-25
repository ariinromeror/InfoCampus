from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Esta es la que faltaba y causaba el error
def home(request):
    return HttpResponse("Servidor de Info Campus Funcionando")

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                return JsonResponse({
                    'status': 'success',
                    'nombre': f"{user.first_name} {user.last_name}" or user.username,
                    'rol': getattr(user, 'rol', 'Estudiante')
                }, status=200)
            
            return JsonResponse({'status': 'error', 'message': 'Credenciales incorrectas'}, status=401)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
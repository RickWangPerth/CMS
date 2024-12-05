# /backend/backend/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .utils import get_cognito_login_url, get_cognito_logout_url, exchange_code_for_tokens


@api_view(['GET'])
def send_test_data(request):
    return Response({
        "data": "Hello from django backend"
    })


def cognito_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'Missing code parameter'}, status=400)

    try:
        tokens = exchange_code_for_tokens(code)
        request.session['access_token'] = tokens.get('access_token')
        request.session['id_token'] = tokens.get('id_token')
        return JsonResponse(tokens)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def cognito_logout(request):
    request.session.flush()
    return JsonResponse({'message': 'Successfully logged out'})

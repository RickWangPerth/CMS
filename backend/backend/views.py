# /backend/backend/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .utils import get_cognito_login_url, get_cognito_logout_url, exchange_code_for_tokens
from backend.middleware.decorators import cognito_auth_required
from django.shortcuts import redirect


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

@api_view(['GET'])
@cognito_auth_required
def protected_route(request):
    # request.cognito_user 包含已验证的用户信息
    return Response({
        "message": "Protected route",
        "user": request.cognito_user
    })

@api_view(['GET'])
def public_route(request):
    return Response({
        "message": "Public route"
    })

@api_view(['GET'])
def login(request):
    login_url = get_cognito_login_url()
    return redirect(login_url)